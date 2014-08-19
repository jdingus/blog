#views.py
from flask import render_template

from blog import app
from database import session
from models import Post

import mistune
from flask import request, redirect, url_for

from flask import flash
from flask.ext.login import login_user,logout_user
from werkzeug.security import check_password_hash
from models import User

from flask.ext.login import login_required, current_user
from login import load_user

@app.route("/")
@app.route("/page/<int:page>")
def posts(page=1, paginate_by=10):
    # Zero-indexed page
    page_index = page - 1

    count = session.query(Post).count()

    start = page_index * paginate_by
    end = start + paginate_by

    total_pages = (count - 1) / paginate_by + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0

    posts = session.query(Post)
    posts = posts.order_by(Post.datetime.desc())
    posts = posts[start:end]

    return render_template("posts.html",
        posts=posts,
        has_next=has_next,
        has_prev=has_prev,
        page=page,
        total_pages=total_pages
    )

@app.route("/singlepost/<int:blogid>")
def singlepost(blogid=1):
    posts = session.query(Post).filter(Post.id==blogid).first()
    return render_template("singlepost.html",posts=posts)

@app.route("/post/add", methods=["GET"])
@login_required
def add_post_get():
    return render_template("add_post.html")

@app.route("/post/add", methods=["POST"])
@login_required
def add_post_post():
    post = Post(
        title=request.form["title"],
        content=mistune.markdown(request.form["content"]),
    )
    session.add(post)
    session.commit()
    return redirect(url_for("posts"))

@app.route("/post/<int:blogid>/edit", methods=["GET"])
@login_required
def edit_post_get(blogid=1):
    post = session.query(Post).filter(Post.id==blogid).first()
    content = post.content
    title = post.title
    return render_template("edit_post.html",content=content,title=title,post=post)

@app.route("/post/<int:blogid>/edit", methods=["POST"])
@login_required
def edit_post_post(blogid=1):
    post = session.query(Post).filter(Post.id==blogid).first()
    post.title = request.form["title"]
    post.content = mistune.markdown(request.form["content"])
    print 'post.title',post.title
    print 'post.content',post.content
    session.add(post)
    session.commit()
    return redirect(url_for("posts"))

@app.route("/post/<int:blogid>/delete", methods=["GET"])
@login_required
def delete_post_get(blogid=1):
    session.query(Post).filter(Post.id==blogid).delete()
    session.commit()
    return redirect(url_for("posts"))

@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(User).filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))

    login_user(user)
    current_name = current_user.name
    flash(current_name + ' is Logged In')
    return redirect(request.args.get('next') or url_for("posts"))

@app.route("/logout")
@login_required
def logout():
    current_name = current_user.name
    logout_user()
    if current_user:
        flash(current_name + ' is Logged Out')
    return redirect(url_for('posts'))

@app.route("/about")
def about_me():
    return render_template("about.html")