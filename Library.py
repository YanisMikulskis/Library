from Book import make_books
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
            personal_number INTEGER NOT NULL,
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

        db_library.cursor.execute('''PRAGMA foreign_keys = ON;''')  # проверка существования id пользователя !!!
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

    @staticmethod
    def number_extraction():
        db_library.cursor.execute('''SELECT personal_number FROM Library_db;''')
        all_personal_numbers = list(map(lambda number_tuple: number_tuple[0], db_library.cursor.fetchall()))
        return all_personal_numbers

    def add_book(self):
        def query_insert(data):
            self.DB.cursor.execute('''INSERT INTO Library_db
                                                    (title, author, year, is_checked_out, personal_number, user_book_id)
                                                    VALUES(?, ?, ?, ?, ?, null);''', data)
            self.DB.connection.commit()

        choice = int(input('Добавить случайную книгу из сети - нажмите 1\n'
                           'Ввести вручную данные - нажмите 2\n'
                           'Вернуться в главное меню программы - нажмите 3\n'))
        if choice == 1:
            quantity = int(input('Сколько случайных книг нужно добавить?'))
            all_book_data = make_books(quantity=quantity)
            for insert in range(quantity):
                all_data = [*all_book_data[insert], 0, self.number_extraction()[-1] + 1]
                query_insert(data=all_data)

        elif choice == 2:
            title = input('Введите название книги')
            author = input('Введите автора книги')
            year = input('Введите год издания')
            personal_number = self.number_extraction()[-1] + 1
            all_data = [title, author, year, 0, personal_number]
            query_insert(data=all_data)
        elif choice == 3:
            main()

        else:
            print(f'Ошибка! введите 1 или 2')
            self.add_book()

    def remove_book(self):
        id_remove_book = int(input(f'Какую книгу нужно удалить? введите ID'))
        self.DB.cursor.execute('''DELETE FROM Library_db WHERE id=:id;''', dict(id=id_remove_book))
        self.DB.cursor.execute('''UPDATE sqlite_sequence set seq = 0 WHERE name = 'Library_db';''')
        self.DB.connection.commit()

    def find_book(self):
        title = input(f'Введите название книги, которую нужно найти')
        self.DB.cursor.execute('''SELECT * FROM Library_db WHERE title=:title;''', dict(title=title))
        find_books = self.DB.cursor.fetchall()
        print(find_books)
        for book in find_books:
            availability = f'Есть' if not book[4] else f'На руках'
            print(f'id: {book[0]}\n'
                  f'Название: {book[1]}\n'
                  f'Автор: {book[2]}\n'
                  f'Год издания: {book[3]}\n'
                  f'Наличие: {availability}\n'
                  f'Индивидуальный номер: {book[5]}\n'
                  f'У кого книга {book[6]}')
            if book[6]:
                self.DB.cursor.execute('''SELECT Users_db.name
                                       FROM Library_db
                                       JOIN Users_db ON Users_db.id = Library_db.user_book_id;''')
                print(self.DB.cursor.fetchall())



    def register_user(self, *user_data):
        name, email = user_data
        self.DB.cursor.execute('''INSERT INTO Users_db(name, email) VALUES(?, ?);''', (name, email))
        self.DB.connection.commit()

    def checkout_book(self):
        user_id = user_id
        personal_number = 32532
        self.DB.cursor.execute('''UPDATE Library_db SET user_book_id = (SELECT id FROM Users_db WHERE id=:id)
                                    WHERE personal_number=:personal_number ;''',
                               dict(id=user_id, personal_number=personal_number))
        self.DB.connection.commit()

        # self.cursor.execute('''UPDATE Library_db SET user_book_id = (SELECT id FROM Users_db WHERE name='ivan')
        #                                 WHERE personal_number = 3532;''')

    def return_book(self):
        self.DB.cursor.execute('''UPDATE Library_db SET user_book_id = null WHERE user_book_id = 4;''')
        self.DB.connection.commit()

    def checkout_report(self):
        print(f'PASS')

    def return_report(self):
        ...

    def general_report(self):
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
    1: lambda: lib.add_book(),
    2: lambda: lib.remove_book(),
    3: lambda: lib.find_book(),
    4: lambda: lib.register_user(),
    5: lambda: lib.checkout_book(),
    6: lambda: lib.return_book(),
    7: lambda: lib.checkout_report(),
    8: lambda: lib.return_report(),
    9: lambda: lib.general_report()
}


def main():
    while 1:
        start_app = int(input('Что хотите сделать? Введите соответсвующую цифру!\n'
                              '1 - Добавить книгу в библиотеку\n'
                              '2 - Удалить книгу из библиотеки по ID\n'
                              '3 - Найти книгу в библиотеке по ID\n'
                              '4 - Зарегистрировать нового читателя\n'
                              '5 - Выдать читателю книгу\n'
                              '6 - Оформить возврата книги читателем\n'
                              '7 - Составить отчет о книгах на руках\n'
                              '8 - Составить отчет о книгах в библиотеке\n'
                              '9 - Составить общий отчет о состоянии библиотеки\n'))

        commands[start_app]()


main()
# lib.add_book('Капитанская дочка', 'А.С.Пушкин', 1836, 0, random.randint(1000,9999))
# lib.remove_book(3)
# lib.register_book('VASYA', 'VAS@ail.ru')
# lib.checkout_book(1)
# lib.return_book()
