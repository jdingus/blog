#manage.py
import os
from flask.ext.script import Manager

from blog import app
from blog.models import Post
from blog.database import session

import getpass
from werkzeug.security import generate_password_hash
from blog.models import User

manager = Manager(app)

@manager.command
def run():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='localhost', port=port)
    # app.run(host='10.11.1.175', port=port)
    # app.run(host='0.0.0.0', port=port)

@manager.command
def seed():
    
    content = """Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""

    for i in range(25):
        post = Post(
            title="Test Post #{}".format(i),
            content=content
        )
        session.add(post)
    session.commit()

@manager.command
def adduser():
    name = raw_input("Name: ")
    email = raw_input("Email: ")
    if session.query(User).filter_by(email=email).first():
        print "User with that email address already exists"
        return

    password = ""
    password_2 = ""
    while not (password and password_2) or password != password_2:
        password = raw_input("Password: ")
        password_2 = raw_input("Re-enter password: ")
        # break
    user = User(name=name, email=email,
                password=generate_password_hash(password))
    session.add(user)
    session.commit()

if __name__ == "__main__":
    manager.run()