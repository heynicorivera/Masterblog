import json

from flask import Flask, redirect, render_template, request, url_for

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


@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
