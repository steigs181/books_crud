from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.book import Book
from flask_app.models.author import Author

# GET
@app.route('/books')
def all_books():
    all_books = Book.get_all_books()
    return render_template('books.html', all_books = all_books)

@app.route('/books/<int:book_id>')
def get_book_by_id(book_id):
    books = Book.get_one_book(book_id)
    all_authors = Author.get_all()
    return render_template('books_show.html', books = books, all_authors = all_authors) 




# POST
@app.route('/books/new', methods=["POST"])
def save_book():
    Book.save_book(request.form)
    return redirect('/books')

@app.route('/add/favorite_book', methods=["POST"])
def add_favorite_book():
    print(request.form)
    favorite = {
        "user_id": request.form["author.id"],
        "book_id": request.form['books.id']
    }
    Author.add_favorite(favorite)
    return redirect(f'/books/{request.form["books.id"]}')