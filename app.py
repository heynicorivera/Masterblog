import json

from flask import Flask, render_template

app = Flask(__name__)

STORAGE_FILE = "posts.json"


def load_posts():
    """Read all blog posts from the JSON storage file."""
    with open(STORAGE_FILE, "r") as fileobj:
        return json.load(fileobj)


@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)