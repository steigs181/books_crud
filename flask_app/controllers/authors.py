from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.author import Author
from flask_app.models.book import Book


# GETTER
@app.route('/')
def index():
    return redirect('/authors')

@app.route('/authors')
def get_authors():
    all_authors = Author.get_all()
    return render_template('authors.html', all_authors = all_authors)

@app.route('/authors/<int:author_id>')
def get_one_author(author_id):
    author = Author.get_one(author_id)
    books = Book.get_all_books()
    return render_template('authors_show.html', author = author, books = books)




# POST
@app.route('/authors/new', methods=["POST"])
def create():
    Author.create(request.form)
    return redirect('/authors')

@app.route('/add/favorite', methods=["POST"])
def add_favorite_author():
    favorite = {
        "user_id": request.form["author.id"],
        "book_id": request.form['title']
    }
    Author.add_favorite(favorite)
    return redirect(f'/authors/{request.form["author.id"]}')