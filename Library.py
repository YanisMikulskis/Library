from Book import Book
from User import User
import sqlite3
import random
class library_DB:
    def __init__(self, name_database):
        self.name_database = name_database
        self.connection = sqlite3.connect(self.name_database)
        self.cursor = self.connection.cursor()
    def create_tables(self):
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS Users_db
            (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE
            )
            '''
        )

        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS Library_db
            (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(150) NOT NULL,
            author VARCHAR(100) NOT NULL,
            year VARCHAR(4) NOT NULL, 
            is_checked_out BLOB NOT NULL,
            personal_number INTEGER NOT NULL UNIQUE,
            user_book_id INTEGER,
            FOREIGN KEY(user_book_id) REFERENCES Users_db(id)
            )
            '''
        )
    def drop(self):
        self.cursor.execute('''DROP TABLE IF EXISTS Library_db;''')
        # self.cursor.execute('''DROP TABLE IF EXISTS Users_db;''')

    def into(self):
        # name = 'sergey'
        # email = 'serg.ru'
        # self.cursor.execute('''INSERT INTO Users_db
        #                              (name, email)
        #                             VALUES(?, ?);''', (name, email))
        # self.connection.commit()
        title_var = 'Война и мир'
        author_var = 'Толстой'
        year_var = '1867'
        is_checked_out_var = 5
        personal_number_var = 353832467

        db_library.cursor.execute('''PRAGMA foreign_keys = ON;''') # проверка существования id пользователя !!!
        db_library.cursor.execute('''INSERT INTO Library_db
                                     (title, author, year, is_checked_out, personal_number, user_book_id)
                                     VALUES('sdsgsd', 'fdsgsdg', '3223', 5, 352, null);''')


        self.connection.commit()

    def foreight(self):
        self.cursor.execute('''UPDATE Library_db SET user_book_id=:user_book_id WHERE id=:id;''',
                               dict(user_book_id=5, id=1))
        self.connection.commit()
    def select(self):
        self.cursor.execute('''SELECT Library_db.title, Library_db.user_book_id, Users_db.name
                                FROM Library_db
                                JOIN Users_db ON Users_db.id = Library_db.user_book_id AND Users_db.name = 'sergey';''')
        print(self.cursor.fetchall())

    def into_fore(self):
        title_var = 'Казаки'
        author_var = 'Украина'
        year_var = '187'
        is_checked_out_var = 5
        personal_number_var = random.randint(1000, 9999)

        db_library.cursor.execute('''INSERT INTO Library_db
                                             (title, author, year, is_checked_out, personal_number, user_book_id)
                                             VALUES('Казаки', 'Толстой', '1867', 5, 43, (SELECT id FROM Users_db WHERE name='sergey'));''')
        self.connection.commit()

    def update(self):
        self.cursor.execute('''UPDATE Library_db SET user_book_id = (SELECT id FROM Users_db WHERE name='ivan') 
                                WHERE personal_number = 3532;''')
        self.connection.commit()
db_library = library_DB('Library_Database')
db_library.create_tables()


# db_library.update()
# db_library.select()
# db_library.select()
# title_var = 'Война и мир'
# author_var = 'Толстой'
# year_var = '1867'
# is_checked_out_var = 5
# personal_number_var = 3337
# db_library.cursor.execute('''INSERT INTO Library_db
#                             (title, author, year, is_checked_out, personal_number)
#                             VALUES(?, ?, ?, ?, ?);''', (title_var, author_var,
#                                                         year_var,
#                                                         is_checked_out_var,
#                                                         personal_number_var))
# db_library.connection.commit()
class Library:
    def __init__(self):
        self.DB = db_library
    def add_book(self, *args):
        title, author, year, is_checked_out, personal_number = args
        self.DB.cursor.execute('''INSERT INTO Library_db
                                (title, author, year, is_checked_out, personal_number, user_book_id)
                                VALUES(?, ?, ?, ?, ?, null);''', [title,
                                                                            author,
                                                                            year,
                                                                            is_checked_out,
                                                                            personal_number])

        self.DB.connection.commit()
    def remove_book(self, id_book):
        self.DB.cursor.execute('''DELETE FROM Library_db WHERE id=:id;''', dict(id=id_book))
        self.DB.cursor.execute('''UPDATE sqlite_sequence set seq = 0 WHERE name = 'Library_db';''')
        self.DB.connection.commit()
    def find_book(self):
        self.DB.cursor.execute('''SELECT * FROM Library_db WHERE title=:title;''', dict(title='Война и мир'))
        print(self.DB.cursor.fetchall())
    def register_user(self, *user_data):
        name, email = user_data
        self.DB.cursor.execute('''INSERT INTO Users_db(name, email) VALUES(?, ?);''', (name, email))
        self.DB.connection.commit()

    def checkout_book(self, user_id):

        user_id = user_id
        personal_number = 32532
        self.DB.cursor.execute('''UPDATE Library_db SET user_book_id = (SELECT id FROM Users_db WHERE id=:id)
                                    WHERE personal_number=:personal_number ;''', dict(id=user_id, personal_number=personal_number))
        self.DB.connection.commit()

        # self.cursor.execute('''UPDATE Library_db SET user_book_id = (SELECT id FROM Users_db WHERE name='ivan')
        #                                 WHERE personal_number = 3532;''')
    def return_book(self):
        self.DB.cursor.execute('''UPDATE Library_db SET user_book_id = null WHERE user_book_id = 4;''')
        self.DB.connection.commit()
    def generate_report(self):
        name = 'VASYA'
        # self.DB.cursor.execute('''SELECT Library_db.title, Library_db.user_book_id, Users_db.name
        #                         FROM Library_db
        #                         JOIN Users_db ON Users_db.id = Library_db.user_book_id AND Users_db.name = :name;''',
        #                        dict(name=name))
        #
        # self.DB.cursor.execute('''SELECT Library_db.title, Library_db.user_book_id, Users_db.name
        #                         FROM Library_db
        #                         JOIN Users_db;''',
        #                        dict(name=name))
        self.DB.cursor.execute('''SELECT * FROM Library_db;''')
        all_books = self.DB.cursor.fetchall()
        book_in_library = [book for book in all_books if book[6] is None]


        self.DB.cursor.execute('''SELECT Library_db.id, Library_db.title, Library_db.user_book_id, Users_db.name
                                    FROM Library_db
                                    JOIN Users_db ON Users_db.id=Library_db.user_book_id;''')
        book_use = self.DB.cursor.fetchall()


lib = Library()
print(f'Добро пожаловать в онлайн библиотеку!')
commands = {
    1:
    2:
    3:
    4:
    5:
}
while 1:
    # Добавление, удаление
    # и
    # поиск
    # книг
    # в
    # библиотеке.

    # Регистрация
    # пользователей
    # библиотеки.

    # Взятие
    # и
    # возврат
    # книг
    # пользователями.

    # Ведение
    # учета
    # выдачи
    # книг
    # и
    # возвратов.

    # Генерация
    # отчетов
    # о
    # текущем
    # состоянии
    # библиотеки.

    start_app = int(input('Что хотите сделать? Введите соответсвующую цифру!\n'
                          '1 - Добавить книгу в библиотеку'
                          '2 - Удалить книгу из библиотеки'
                          ''))
# lib.add_book('Капитанская дочка', 'А.С.Пушкин', 1836, 0, random.randint(1000,9999))
# lib.remove_book(3)
#lib.register_book('VASYA', 'VAS@ail.ru')
# lib.checkout_book(1)
# lib.return_book()
