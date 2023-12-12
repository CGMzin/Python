from flask import Flask, render_template, request, redirect, url_for
from db import *


@app.before_first_request
def create_database():
    db.create_all()

@app.route('/')
def home():
    all_books = Books.query.all()
    return render_template('index.html', books=all_books)

@app.route('/edit/<id>', methods=["POST", "GET"])
def edit(id):
    book = Books.query.get(int(id))
    if request.method == "POST":
        new_rating = request.form.get('rating')
        book.rating = new_rating
        db.session.commit()
        all_books = Books.query.all()
        return render_template('index.html', books=all_books)
    return render_template('edit_rating.html', book=book)

@app.route('/delete')
def delete():
    id = request.args.get('id')
    book = Books.query.get(int(id))
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        book = Books(title=request.form.get('name'), author=request.form.get('author'), rating=request.form.get('rating'))
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')


if __name__ == "__main__":
    app.run()

