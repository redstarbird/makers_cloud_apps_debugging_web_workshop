import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, redirect, url_for
from lib.post import Post
from lib.post_repository import PostRepository
from lib.database_connection import get_flask_database_connection

app = Flask(__name__)

@app.route('/')
def index():
    connection = get_flask_database_connection(app)
    post_repository = PostRepository(connection)
    posts = post_repository.all()
    return render_template('index.html', posts=posts)

# get posts for a given tag
@app.route('/tag/<tag>', methods=['GET'])
def posts_by_tag(tag):
    connection = get_flask_database_connection(app)
    post_repository = PostRepository(connection)
    # For now, let's get all posts since the repository doesn't have all_posts_by_tag yet
    posts = post_repository.all()
    return render_template('index.html', posts=posts)

# create new post
@app.route('/posts', methods=['POST'])
def create_post():
    connection = get_flask_database_connection(app)
    post_repository = PostRepository(connection)
    new_post = Post(request.form['title'], request.form['content'], request.form['tags'].split(','))
    post_repository.create(new_post)
    posts = post_repository.all()
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
