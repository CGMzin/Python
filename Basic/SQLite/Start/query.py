from db import *

with app.app_context():
    """ db.drop_all()
    db.create_all()
    harry_poter = Books(id=1, title="Harry Potter", author="J. K. Rowling", rating=9.3)
    db.session.add(harry_poter)
    db.session.commit() """
    all_books = db.session.query(Books).all
    print(all_books)