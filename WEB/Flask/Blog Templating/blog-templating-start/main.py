from flask import Flask, render_template
from post import Post
import requests


app = Flask(__name__)
all_blogs = requests.get('https://api.npoint.io/3c540308a25f171fc745').json()
posts = [Post(post['id'], post['title'], post['subtitle'], post['body']) for post in all_blogs]

@app.route('/')
def home():
    return render_template("index.html", posts=posts)

@app.route('/post/<blog_id>')
def get_post(blog_id):
    return render_template("post.html", id=int(blog_id), posts=posts)

if __name__ == "__main__":
    app.run()
