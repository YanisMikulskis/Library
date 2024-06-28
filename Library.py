from Book import make_books
from User import User
from typing import Union, Callable
import sqlite3
import random
import re


class library_DB:
    def __init__(self, name_database: str):
        self.name_database: str = name_database
        self.connection = sqlite3.connect(self.name_database)
        self.cursor = self.connection.cursor()

    def create_tables(self) -> None:
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


db_library = library_DB('Library_Database')
db_library.create_tables()
print(type(library_DB('Library_Database')))
db_library.cursor.execute('''UPDATE Library_db SET is_checked_out = 0 WHERE user_book_id NOT NULL;''')
db_library.connection.commit()


# db_cont.cursor.execute('''UPDATE Contacts_list SET name=:name, number_phone=:number,email=:email
# WHERE id=:id;'''
class Library:
    def __init__(self):
        self.DB: library_DB = db_library

    @staticmethod
    def last_number() -> Union[bool, int]:
        db_library.cursor.execute('''SELECT personal_number FROM Library_db;''')
        all_personal_numbers = list(map(lambda number_tuple: number_tuple[0], db_library.cursor.fetchall()))
        if not all_personal_numbers:
            return False
        else:
            return all_personal_numbers[-1] + 1

    def add_book(self) -> Callable:
        def query_insert(data) -> None:
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
                personal_number = 1000 if not self.last_number() else self.last_number()
                all_data = [*all_book_data[insert], 1, personal_number]
                return query_insert(data=all_data)

        elif choice == 2:
            title = input('Введите название книги')
            author = input('Введите автора книги')
            year = input('Введите год издания')
            personal_number = self.number_extraction()[-1] + 1
            all_data = [title, author, year, 1, personal_number]
            return query_insert(data=all_data)
        elif choice == 3:
            return main()

        else:
            print(f'Ошибка! введите 1 или 2')
            return self.add_book()

    def remove_book(self) -> None:
        id_remove_book = int(input(f'Какую книгу нужно удалить? введите ID'))
        self.DB.cursor.execute('''DELETE FROM Library_db WHERE id=:id;''', dict(id=id_remove_book))
        self.DB.cursor.execute('''UPDATE sqlite_sequence set seq = 0 WHERE name = 'Library_db';''')
        self.DB.connection.commit()

    def find_book(self) -> None:
        title = input(f'Введите название книги, которую нужно найти')
        print(f'Введенное название книги: {title}')
        self.DB.cursor.execute('''SELECT * FROM Library_db WHERE title=:title;''', dict(title=title))
        find_books = self.DB.cursor.fetchall()
        if not find_books:  # если в названии книги прогрузилось с лишним пробелом после названия
            self.DB.cursor.execute('''SELECT * FROM Library_db WHERE title=:title;''', dict(title=title + ' '))
            find_books = self.DB.cursor.fetchall()
            if not find_books:  # если книги такой вообще нет
                print(f'Такой книги в библиотеке нет! Попробуйте ввести что-нибудь другое')
                return self.find_book()

        for book in find_books:
            availability = f'Есть' if not book[4] else f'На руках'

            def exam_book() -> Union[tuple, str]:  # Выводим данные юзера у кого книга, иначе ничего
                if book[6]:
                    self.DB.cursor.execute('''SELECT Users_db.id, Users_db.name, Users_db.email
                                                    FROM Library_db
                                                    JOIN Users_db ON Users_db.id=:foreight_key;''',
                                           dict(foreight_key=book[6]))

                    data_user = self.DB.cursor.fetchall()[0]
                    return (f'id пользователя: {data_user[0]}\n'
                            f'Имя пользователя: {data_user[1]}\n'
                            f'Почта для связи: {data_user[2]}')
                else:
                    return f'Книга в библиотеке'

            print(f'id: {book[0]}\n'
                  f'Название: {book[1]}\n'
                  f'Автор: {book[2]}\n'
                  f'Год издания: {book[3]}\n'
                  f'Наличие: {availability}\n'
                  f'Индивидуальный номер: {book[5]}\n'
                  f'Местоположение книги:\n{exam_book()}\n')

    def register_user(self) -> Union[None, Callable]:
        print(f'Регистрация нового пользователя')
        print('###################')
        name = input(f'Введите имя пользователя: ')
        email = input(f'Введите электроную почту пользователя')
        email_domain = re.findall(r'@+\S+', email)[0]
        domains = ['@mail.ru', '@gmail.com', '@rambler.ru', '@yahoo.com', '@yandex.ru']
        if email_domain in domains:
            self.DB.cursor.execute('''INSERT INTO Users_db(name, email) VALUES(?, ?);''', (name, email))
            return self.DB.connection.commit()
        else:
            print(f'Введите правильный формат почты')
            return self.register_user()

    def checkout_book(self) -> None:
        user_id = int(input(f'Какому пользователю нужно выдать книгу? Введите его id'))
        self.DB.cursor.execute('''SELECT name FROM users_db WHERE id=:id;''', dict(id=user_id))
        name_user = self.DB.cursor.fetchall()[0][0]
        personal_number = int(input(f'Какую книгу вы хотите выдать пользователю {name_user}? '
                                    f'Введите персональный номер книги\n'))

        self.DB.cursor.execute('''UPDATE Library_db SET user_book_id = (SELECT id FROM Users_db WHERE id=:user_id)
                                    WHERE personal_number=:personal_number;''',
                               dict(user_id=user_id, personal_number=personal_number))
        return self.DB.connection.commit()

    def return_book(self) -> str:
        user_id = int(input(f'Какой пользователь возвращает книгу? Введите id'))
        self.DB.cursor.execute('''SELECT name FROM Users_db WHERE id=:id;''', dict(id=user_id))
        user_name = self.DB.cursor.fetchall()[0][0]
        title = input(f'Какую книгу он возвращает? Введите название')
        print(list(title))
        print(title[-1])
        return f'Пользователь {user_name} вернул книгу {title}'

    def checkout_report(self, *for_return) -> str:
        self.DB.cursor.execute('''SELECT * FROM Library_db;''')
        all_books = self.DB.cursor.fetchall()
        book_on_hands = [book for book in all_books if book[-1] is not None]
        if not for_return:
            return f'На руках находится {len(book_on_hands)}/{len(all_books)} книг.'
        else:
            return f'В библиотеке находится книг: {len(all_books) - len(book_on_hands)} шт.'

    def return_report(self) -> Callable:
        return self.checkout_report(True)

    def general_report(self) -> None:

        self.checkout_report(True)
        self.checkout_report()

        self.DB.cursor.execute('''SELECT * FROM Users_db;''')
        library_users, number_user = self.DB.cursor.fetchall(), 1
        print(f'Список всех пользователей библиотеки:')
        for user in library_users:
            print(f'{number_user}. Имя: {user[1]}\nПочта: {user[2]}')
            number_user += 1
            print()

        self.DB.cursor.execute('''SELECT Library_db.id, Library_db.title, Library_db.personal_number, Users_db.name
                                    FROM Library_db
                                    JOIN Users_db ON Users_db.id=Library_db.user_book_id;''')
        users_book = self.DB.cursor.fetchall()
        print(f'Список пользователей, которые взяли хотя бы одну книгу.')
        users_book_dict = {val[-1]: [] for val in users_book}
        for data in users_book:
            if not users_book_dict[data[-1]]:
                number = 1
            else:
                number = int(users_book_dict[data[-1]][-1][0]) + 1
            users_book_dict[data[-1]].append(f'{number}.{data[1]}')

        for user, books in users_book_dict.items():
            books = '\n'.join(books)
            print(f'Пользователь {user} взял книги:\n{books}')
            print()


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
# lib.return_book(
