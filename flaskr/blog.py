# from flask import (
#     Blueprint, flash, g, redirect, render_template, request, url_for
# )
# from werkzeug.exceptions import abort

# from flaskr.auth import login_required
# from flaskr.db import get_db

# bp = Blueprint('blog', __name__)

# POST_PER_PAGE = 3

# @bp.route('/')
# def index():
#     db = get_db()

#     # Get the current page number from the query parameter (default is 1)
#     page = request.args.get('page', 1, type=int)

#     offset = (page - 1) * POST_PER_PAGE
#     posts = db.execute(
#         '''SELECT p.id, title, body, created, author_id, username
#         FROM post p JOIN user u ON p.author_id = u.id
#         ORDER BY created DESC  LIMIT ? OFFSET ?''', (POST_PER_PAGE, offset)
#     ).fetchall()


#     total_posts = db.execute(
#         'SELECT COUNT(*) FROM post'
#     ).fetchone()[0]

#     total_pages = (total_posts + POST_PER_PAGE - 1) // POST_PER_PAGE

#     return render_template('blog/index.html', posts=posts, page=page,
#         total_pages=total_pages)


# @bp.route('/create', methods=('GET', 'POST'))
# @login_required
# def create():
#     if request.method == 'POST':
#         title = request.form['title']
#         body = request.form['body']
#         error = None

#         if not title:
#             error = 'Title is required.'

#         if error is not None:
#             flash(error)
#         else:
#             db = get_db()
#             db.execute(
#                 'INSERT INTO post (title, body, author_id)'
#                 ' VALUES (?, ?, ?)',
#                 (title, body, g.user['id'])
#             )
#             db.commit()
#             return redirect(url_for('blog.index'))

#     return render_template('blog/create.html')

# def get_post(id):
#     post = get_db().execute(
#         'SELECT p.id, title, body, created, author_id, username'
#         ' FROM post p JOIN user u ON p.author_id = u.id'
#         ' WHERE p.id = ?',
#         (id,)
#     ).fetchone()

#     if post is None:
#         abort(404, f"Post id {id} doesn't exist.")

#     return post


# @bp.route('/post/<int:id>', methods=('GET','POST'))
# def singlePost(id):
#     post = get_post(id)
#     return render_template('blog/singlepost.html', post=post)


# @bp.route('/<int:id>/update', methods=('GET', 'POST'))
# @login_required
# def update(id,  check_author=True):
#     post = get_post(id)

#     if request.method == 'POST':
#         title = request.form['title']
#         body = request.form['body']
#         error = None

#         if not title:
#             error = 'Title is required.'

#         if error is not None:
#             flash(error)
#         else:
#             db = get_db()
#             db.execute(
#                 'UPDATE post SET title = ?, body = ?'
#                 ' WHERE id = ?',
#                 (title, body, id)
#             )
#             db.commit()
#             return redirect(url_for('blog.index'))
#         if check_author and post['author_id'] != g.user['id']:
#             abort(403)

#     return render_template('blog/update.html', post=post)


# @bp.route('/<int:id>/delete', methods=('POST',))
# @login_required
# def delete(id):
#     get_post(id)
#     db = get_db()
#     db.execute('DELETE FROM post WHERE id = ?', (id,))
#     db.commit()
#     return redirect(url_for('blog.index'))


from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import db, Post, User

bp = Blueprint('blog', __name__)

POST_PER_PAGE = 3

@bp.route('/')
def index():
    # Get the current page number from the query parameter (default is 1)
    page = request.args.get('page', 1, type=int)
    
    # Use SQLAlchemy's pagination
    pagination = db.session.query(Post, User).join(User).order_by(Post.created.desc())\
        .paginate(page=page, per_page=POST_PER_PAGE, error_out=False)
    
    posts = [{
        'id': post.id,
        'title': post.title,
        'body': post.body,
        'created': post.created,
        'author_id': post.author_id,
        'username': user.username
    } for post, user in pagination.items]

    return render_template('blog/index.html', 
                        posts=posts, 
                        page=page,
                        total_pages=pagination.pages)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post = Post(title=title, body=body, author_id=g.user.id)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id):
    post = db.session.query(Post, User.username)\
        .join(User)\
        .filter(Post.id == id)\
        .first()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    return {
        'id': post[0].id,
        'title': post[0].title,
        'body': post[0].body,
        'created': post[0].created,
        'author_id': post[0].author_id,
        'username': post[1]
    }

@bp.route('/post/<int:id>', methods=('GET','POST'))
def singlePost(id):
    post = get_post(id)
    return render_template('blog/singlepost.html', post=post)

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id, check_author=True):
    post = get_post(id)
    
    if check_author and post['author_id'] != g.user.id:
        abort(403)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post_obj = Post.query.get(id)
            post_obj.title = title
            post_obj.body = body
            db.session.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = Post.query.get_or_404(id)
    if post.author_id != g.user.id:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blog.index'))