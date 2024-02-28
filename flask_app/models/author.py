from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book

class Author:

    DB = "books_schema"

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.liked_books = []

    # CREATE
    @classmethod
    def create(cls, data):
        query = """
                INSERT INTO users (name)
                VALUES (%(name)s)
                """
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results 
    
    @classmethod
    def add_favorite(cls, data):
        query = """
                INSERT INTO favorites (user_id, book_id)
                VALUES (%(user_id)s, %(book_id)s)
                """
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results

    # READ
    @classmethod
    def get_all(cls):
        query = """ SELECT * FROM users """
        results = connectToMySQL(cls.DB).query_db(query)
        authors = []
        for author in results:
            authors.append(cls(author))
        return authors

    @classmethod
    def get_one(cls, author_id):
        query = """SELECT * FROM users LEFT JOIN favorites ON favorites.user_id = users.id
                LEFT JOIN books ON favorites.book_id = books.id
                WHERE users.id = %(id)s; """
        data = {
            'id': author_id
        }
        results = connectToMySQL(cls.DB).query_db(query, data)
        author = cls(results[0])
        for row in results:
            book_data = {
                'id': row['books.id'],
                'title': row['title'],
                'num_of_pages': row['num_of_pages'],
                'created_at': row['books.created_at'],
                'updated_at': row['books.updated_at']
            }
            author.liked_books.append(book.Book(book_data))
        return author