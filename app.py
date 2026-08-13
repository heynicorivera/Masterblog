import json

from flask import Flask, redirect, render_template, request, url_for
from pylint.checkers.utils import is_registered_in_singledispatch_function

app = Flask(__name__)

STORAGE_FILE = "posts.json"


def load_posts():
    """Read all blog posts from the JSON storage file."""
    with open(STORAGE_FILE, "r") as fileobj:
        return json.load(fileobj)


def save_posts(posts):
    """Write the given list of blog posts to the JSON storage file."""
    with open(STORAGE_FILE, "w") as fileobj:
        json.dump(posts, fileobj, indent=4)


def generate_id(posts):
    """Return a new unique id: one higher than the highest existing id."""
    highest_id = 0
    for post in posts:
        if post["id"] > highest_id:
            highest_id = post["id"]
    return highest_id + 1


def fetch_post_by_id(post_id):
    """Return the blog post with the given id, or None if it does not exist."""
    blog_posts = load_posts()
    for post in blog_posts:
        if post["id"] == post_id:
            return post
    return None


@app.route('/')
def index():
    """Show the home page with all blog posts."""
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Show the add form (GET) or save a new blog post (POST)."""
    if request.method == 'POST':
        blog_posts = load_posts()
        new_post = {
            "id": generate_id(blog_posts),
            "author": request.form.get("author"),
            "title": request.form.get("title"),
            "content": request.form.get("content"),
        }
        blog_posts.append(new_post)
        save_posts(blog_posts)
        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """Delete the blog post with the given id and go back home."""
    blog_posts = load_posts()
    for post in blog_posts:
        if post["id"] == post_id:
            blog_posts.remove(post)
            break
    save_posts(blog_posts)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Show the update form (GET) or save changes to a post (POST)."""
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        blog_posts = load_posts()
        for existing_post in blog_posts:
            if existing_post["id"] == post_id:
                existing_post["author"] = request.form.get("author")
                existing_post["title"] = request.form.get("title")
                existing_post["content"] = request.form.get("content")
                break
        save_posts(blog_posts)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

