import sqlite3
import os
import subprocess







connection = sqlite3.connect('Library_FLASK_DB')
cursor = connection.cursor()



cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS Users_table_Flask
            (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE
            )
            '''
        )
cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS Library_table_flask
            (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(150) NOT NULL,
            author VARCHAR(100) NOT NULL,
            year VARCHAR(4) NOT NULL,
            is_checked_out BLOB NOT NULL,
            personal_number INTEGER NOT NULL UNIQUE,
            user_book_id INTEGER,
            FOREIGN KEY(user_book_id) REFERENCES User_table_flask(id)
            )
            '''
               )


