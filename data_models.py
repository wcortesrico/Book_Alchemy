from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()# crating the object from SQLAlchemy to be main object

class Author(db.Model):
    #creating the Author class
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    birth_date = db.Column(db.Text, nullable=True)
    date_of_death = db.Column(db.Text, nullable=True)
    books = db.relationship('Book', backref='author', lazy=True)
    #creating the relationship between the books table and the authors table

    def __str__(self):
        return f"Author name: {self.name} born in: {self.birth_date}"

    def __repr__(self):
        return f"Author(author_id = {self.id} author_name = {self.name}"


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    isbn = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String, nullable=False)
    publication_year = db.Column(db.Integer, nullable=True)

    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    #defining the foreing key using the author_id from authors table

    def __str__(self):
        return (f"Book title: {self.title} ISBN: {self.isbn}")

    def __repr__(self):
        return f"Book(book_title = {self.title} book_isbn = {self.isbn}"
