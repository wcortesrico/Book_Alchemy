from flask import Flask, request, redirect, url_for, render_template
from data_models import db, Author, Book
from cover_fetch import get_cover


app = Flask(__name__)

"""
To create the connection between flask and the database,
used to establish connection between application and the 
database management system (DBMS) 
"""

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.sqlite'
#connecting the Flask app to the Flask-sqlalchemy code
db.init_app(app)

'''
The two functions "sort_func_title" and "sort_func_author" are made for 
returning the respective book either for title or author to apply the 
sort function for future.
'''
def sort_func_title(book):
    return book["title"]

def sort_func_author(book):
    return book["author"]

@app.route('/', methods=['GET', 'POST'])
# This route defines the home function for the home page and display the books
def home():
    books = []
    try:
        books = Book.query.all()
    except IOError as e:
        print("An IO error occurred: ", str(e))
    books_list = []
    for book in books:
        books_list.append({
            'title': book.title,
            'author': book.author.name,
            'cover_image_url': get_cover(book.isbn),
            'id': book.id
        })
    if request.method == 'POST':
        sort_type = request.form['sort']# posting the sort selection form from home page
        if sort_type == "title":
            books_list.sort(key=sort_func_title)
        elif sort_type == "author":
            books_list.sort(key=sort_func_author)

    return render_template('home.html', books=books_list)# rendering for books

@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    #function to add an author getting data from the add_author.html
    if request.method == 'POST':
        author = Author(
            name=request.form["name"],
            birth_date=request.form["birthdate"],
            date_of_death=request.form["date_of_death"],

        )
        db.session.add(author) #using the flask-sqlalchemy functions to adding to the database
        db.session.commit()# using this function to upload the modifications to database
        return redirect(url_for('home'))
    return render_template('add_author.html')

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    #function to add a new book to data base
    authors_list = []
    authors = Author.query.all()
    id_author = None
    for author in authors:
        authors_list.append(author.name)
    if request.method == 'POST':
        author_name = request.form['author']
        for author in authors:
            if author_name == author.name:
                id_author = author.id # here we define the author_id from the author.id in authors table
        book = Book(
            title=request.form['title'],
            isbn=request.form['isbn'],
            publication_year=int(request.form['publication_year']),
            author_id=id_author
        )
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('home'))


    return render_template('add_book.html', authors=authors_list)

@app.route('/search')
def search():
    #the search function searches for a string in title or author from the books info
    searched_query = request.args.get("search").lower()# with lower function there is not case sensitive
    books = Book.query.all()
    searched_books = [] #this list will contain the books that match the criteria with the searched string
    for book in books:
        if searched_query in book.title.lower() or searched_query in book.author.name.lower():
            searched_books.append({
                'title': book.title,
                'author': book.author.name,
                'cover_image_url': get_cover(book.isbn),
                'id': book.id
            })
    if len(searched_books) == 0:
         return "No such books found"
    return render_template('search.html', books=searched_books)

@app.route('/delete/<int:book_id>', methods=['GET', 'POST'])
def delete(book_id):
    '''
    function to delete the book using the book_id as reference,
    and deletes the author if doesn't has any other book on data base
    '''
    if request.method == 'POST':
        #  retrieve the book with the given id
        book = Book.query.filter_by(id=book_id).first()
        if book:
            #  getting the author from the book
            author = book.author
            db.session.delete(book)
            db.session.commit()
            #  check if the author is in another books
            other_books = Book.query.filter_by(author_id=author.id).all()

            if not other_books:
                #  if there are not more books of the author, proceed to the deletion of the author
                db.session.delete(author)
                db.session.commit()

        return redirect(url_for('home'))
    return render_template('confirm_delete.html', book_id=book_id)


if __name__ == "__main__":
    app.run()


'''
with app.app_context():
    db.create_all()
'''
