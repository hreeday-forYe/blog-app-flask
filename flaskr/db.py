# import sqlite3
# from datetime import datetime

# import click
# from flask import current_app, g


# def get_db():
#     if 'db' not in g:
#         g.db = sqlite3.connect(
#             current_app.config['DATABASE'],
#             detect_types=sqlite3.PARSE_DECLTYPES
#         )
#         g.db.row_factory = sqlite3.Row

#     return g.db


# def close_db(e=None):
#     db = g.pop('db', None)

#     if db is not None:
#         db.close()



# def init_db():
#     db = get_db()

#     with current_app.open_resource('schema.sql') as f:
#         db.executescript(f.read().decode('utf8'))


# @click.command('init-db')
# def init_db_command():
#     """Clear the existing data and create new tables."""
#     init_db()
#     click.echo('Initialized the database.')


# sqlite3.register_converter(
#     "timestamp", lambda v: datetime.fromisoformat(v.decode())
# )

# def init_app(app):
#     app.teardown_appcontext(close_db)
#     app.cli.add_command(init_db_command)



# # from flask import Flask
# # from flask_sqlalchemy import SQLAlchemy
# # from flask.cli import with_appcontext
# # import click

# # db = SQLAlchemy()

# # def init_app(app):
# #     """
# #     Initialize the app with the SQLAlchemy database.
# #     """
# #     # Bind the SQLAlchemy instance to the Flask app
# #     db.init_app(app)

# #     # Register CLI command for initializing the database
# #     app.cli.add_command(init_db_command)


# # @click.command('init-db')
# # @with_appcontext
# # def init_db_command():
# #     """
# #     Clear the existing data and c
    
# #     reate new tables.
# #     """
# #     # Drop all tables and recreate them
# #     db.drop_all()
# #     db.create_all()
# #     click.echo('Initialized the database.')
from flask_sqlalchemy import SQLAlchemy
from flask import current_app
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

def init_db():
    db.create_all()

def init_app(app):
    db.init_app(app)
    app.cli.add_command(init_db_command)

def get_db():
    return db

# Create the Flask CLI command for database initialization
import click
from flask.cli import with_appcontext

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

