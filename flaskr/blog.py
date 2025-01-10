
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