from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author

class Book:

    DB = 'books_schema'

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.authors_favs = []

    # CREATE
    @classmethod
    def save_book(cls, data):
        query = """
                INSERT INTO books (title, num_of_pages, created_at, updated_at)
                VALUES (%(title)s, %(num_of_pages)s, NOW(), NOW())
                """
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results

    # READ
    @classmethod
    def get_all_books(cls):
        query = """
                SELECT * FROM books;
                """
        result = connectToMySQL(cls.DB).query_db(query)
        all_books = []
        for book in result:
            all_books.append(book)
        return result
    
    @classmethod
    def get_one_book(cls, book_id):
        query = """
                SELECT * FROM books LEFT JOIN favorites ON favorites.book_id = books.id
                LEFT JOIN users ON favorites.user_id = users.id
                WHERE books.id = %(id)s
                """
        data = {
            'id': book_id
        }
        results = connectToMySQL(cls.DB).query_db(query, data)
        book = cls(results[0])
        for row in results:
            author_data = {
                'id': row['users.id'],
                'name': row['name'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            print(author_data)
            book.authors_favs.append(author.Author(author_data))
        return book