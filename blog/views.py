#views.py
from flask import render_template

from blog import app
from database import session
from models import Post

import mistune
from flask import request, redirect, url_for

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
def add_post_get():
    return render_template("add_post.html")

@app.route("/post/add", methods=["POST"])
def add_post_post():
    post = Post(
        title=request.form["title"],
        content=mistune.markdown(request.form["content"]),
    )
    session.add(post)
    session.commit()
    return redirect(url_for("posts"))

@app.route("/post/<int:blogid>/edit", methods=["GET"])
def edit_post_get(blogid=1):
    post = session.query(Post).filter(Post.id==blogid).first()
    content = post.content
    title = post.title
    print 'post.content:',content
    print 'post.title:',title
    return render_template("edit_post.html",content=content,title=title)
    # post = Post(
    #     title=request.form["title"],
    #     content=mistune.markdown(request.form["content"]),
    # )
    # session.add(post)
    # session.commit()
    # return redirect(url_for("posts"))

