## Getting Started

This is the simple blog we application made using flask a lightweight python library to create REST APIs. The database used for this project is sqllite and ORM used is SQLAlchemy.
**The feature of the project includes**

- User authentication (registration, login, logout)
- Create, read, update, and delete blog posts
- Display a list of all blog posts on the homepage
- Display a single blog post on a separate page
- Include pagination API for displaying multiple blog posts

### Installation Guidelines

You need to have Python and Git installed in your system.

1. Clone the project

```
git clone https://github.com/hreeday-forYe/blog-app-flask.git
```

2. Install package Pipenv
   <small>_This project is managed in virtual environment so it uses pipenv for installing the requiring dependencies_</small>
   `pip install pipenv`
   <br>
3. Navigate to the project location using cd Command
   `cd "location of the project where you have clonned"`
   <br>
4. Install the dependencies
   `pipenv install`
   <br>
5. Activate the Virtual Environement
   `pipenv shell`
   <br>
6. Initialize the database

```
 flask --app flaskr init-db
```

7. Run the Application

```
flask --app flaskr run --debug
```

NOTES

- You can access the application at http://127.0.0.1:5000 after running the server.
