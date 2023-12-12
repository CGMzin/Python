from flask import Flask
from flask import render_template
import time, requests

app = Flask(__name__)

@app.route('/')
def start():
    year = time.gmtime()[0]
    return render_template('index.html', year=year)

@app.route('/guess/<name>')
def guess(name):
    years = requests.get(f'https://api.agify.io?name={name}').json()["age"]
    sex = requests.get(f'https://api.genderize.io?name={name}').json()["gender"]
    return render_template('guess.html', years=years, sex=sex, name=name)

@app.route('/blog')
def get_blog():
    all_blogs = requests.get('https://api.npoint.io/3c540308a25f171fc745').json()
    return render_template("blog.html", posts=all_blogs)

if __name__ == "__main__":
    app.run()