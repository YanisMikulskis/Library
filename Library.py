from Book import Book
from User import User
import sqlite3

class library_DB:
    def __init__(self, name_database):
        self.name_database = name_database
        self.connection = sqlite3.connect(self.name_database)
        self.cursor = self.connection.cursor()
    def create_database(self):
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS Library_db
            (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(150) NOT NULL,
            author VARCHAR(100) NOT NULL,
            year VARCHAR(4) NOT NULL, 
            is_checked_out BOO INTEGER NOT NULL,
            personal_number INTEGER NOT NULL UNIQUE
            )
            '''
        )


class Library:
    def __init__(self):
        pass
    def add_book(self, book:Book):
        ...
    def remove_book(self, book_id: int):
        ...
    def find_book(sel, book_id: int):
        ...
    def register_book(self, user):
        ...
    def checkout_book(self, book_id, user_id):
        ...
    def return_book(self, book_id, user_id):
        ...
    def generate_report(self):
        ...


