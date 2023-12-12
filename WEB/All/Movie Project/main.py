from flask import Flask, render_template, redirect, url_for, request
from db import *
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, NumberRange
import requests

API_KEY = 'e7135fb5de3849ee41182075446441a7'
POSTER_URL = 'https://image.tmdb.org/t/p/original'

class EditForm(FlaskForm):
    new_rating = FloatField('Your Rating Out of 10 e.g. 7.5', validators=[DataRequired(), NumberRange(min=0, max=10, message=f'Min: 0, Max: 10')])
    new_review = StringField('Your Review', validators=[DataRequired()])
    submit = SubmitField('Done')
    
class AddForm(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])
    submit = SubmitField('Done')

@app.before_first_request
def create_db():
    db.create_all()

@app.route("/")
def home(): 
    all_movies = Movie.query.order_by(Movie.rating).all()
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()
    return render_template("index.html", movies=all_movies)

@app.route("/add", methods=['GET', 'POST'])
def add(): 
    form = AddForm()
    if form.validate_on_submit():
        response = requests.get(f'https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={request.form.get("title")}').json()['results']
        return render_template("select.html", movies=response)
    return render_template("add.html", form=form)

@app.route("/select")
def select(): 
    id = request.args.get('id')
    response = requests.get(f'https://api.themoviedb.org/3/movie/{id}?api_key={API_KEY}').json()
    new_movie = Movie(title=response['original_title'], img_url=f"{POSTER_URL}{response['poster_path']}", year=response['release_date'].split('-')[0], description=response['overview'])
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for('edit', id=new_movie.id))

@app.route("/edit", methods=['GET', 'POST'])
def edit(): 
    id = request.args.get('id')
    movie = Movie.query.get(id)
    form = EditForm()
    if form.validate_on_submit():
        movie.rating = request.form.get('new_rating')
        movie.review = request.form.get('new_review')
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", movie=movie, form=form)

@app.route('/delete')
def delete():
    id = request.args.get('id')
    movie = Movie.query.get(id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()
