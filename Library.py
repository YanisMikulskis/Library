from Book import make_books
from User import User
from typing import Union, Callable
import sqlite3
import random
import re


class library_DB:  # Класс создания БД
    def __init__(self, name_database: str):
        self.name_database: str = name_database
        self.connection = sqlite3.connect(self.name_database)
        self.cursor = self.connection.cursor()

    def create_tables(self) -> None:  # Метод создания таблиц библиотеки и зареганных пользователей
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


class Library:  # Основной класс приложения
    def __init__(self):
        self.DB: library_DB = db_library

    @staticmethod
    def last_number() -> Union[bool, int]:  # Стат. метод извлечения последнего уникального номера книги
        db_library.cursor.execute('''SELECT personal_number FROM Library_db;''')
        all_personal_numbers = list(map(lambda number_tuple: number_tuple[0], db_library.cursor.fetchall()))
        if not all_personal_numbers:
            return False
        else:
            return all_personal_numbers[-1] + 1

    def add_book(self) -> None:  # Метод добавления новой книги в библиотеку
        def query_insert(data) -> Callable:  # Доп. функция для вставки данных в табл. (чтобы не было code duplication)
            self.DB.cursor.execute('''INSERT INTO Library_db
                                                    (title, author, year, is_checked_out, personal_number, user_book_id)
                                                    VALUES(?, ?, ?, ?, ?, null);''', data)
            return self.DB.connection.commit()

        choice = int(input('Добавить случайную книгу из сети - нажмите 1\n'
                           'Ввести вручную данные - нажмите 2\n'
                           'Вернуться в главное меню программы - нажмите 3\n'))
        if choice == 1:  # команда добавления случайных книг из Сети
            quantity = int(input('Сколько случайных книг нужно добавить?'))
            all_book_data = make_books(quantity=quantity)
            for insert in range(quantity):
                personal_number = 1000 if not self.last_number() else self.last_number()
                all_data = [*all_book_data[insert], 1, personal_number]
                query_insert(data=all_data)

        elif choice == 2:  # команда ручного добавления книги
            title = input('Введите название книги')
            author = input('Введите автора книги')
            year = input('Введите год издания')
            personal_number = 1000 if not self.last_number() else self.last_number()
            all_data = [title, author, year, 1, personal_number]
            query_insert(data=all_data)
        elif choice == 3:  # команда возврата к командам
            main()

        else:  # иначе перезапускаем данный метод
            print(f'Ошибка! введите 1,2 или 3')
            self.add_book()

    def remove_book(self) -> None:  # метод удаления книги из библиотеки
        id_remove_book = int(input(f'Какую книгу нужно удалить? введите ID'))
        self.DB.cursor.execute('''DELETE FROM Library_db WHERE id=:id;''', dict(id=id_remove_book))
        self.DB.cursor.execute('''UPDATE sqlite_sequence set seq = 0 WHERE name = 'Library_db';''')
        self.DB.connection.commit()

    def find_book(self) -> None:  # метод поиска книги в библиотеке по названию
        title = input(f'Введите название книги, которую нужно найти')
        print(f'Введенное название книги: {title}')
        self.DB.cursor.execute('''SELECT * FROM Library_db WHERE title=:title;''', dict(title=title))
        find_books = self.DB.cursor.fetchall()
        if not find_books:  # если в названии книги прогрузилось с лишним пробелом после названия
            self.DB.cursor.execute('''SELECT * FROM Library_db WHERE title=:title;''', dict(title=title + ' '))
            find_books = self.DB.cursor.fetchall()
            if not find_books:  # если книги такой вообще нет
                print(f'Такой книги в библиотеке нет! Попробуйте ввести что-нибудь другое')
                self.find_book()

        for book in find_books:
            availability = f'Есть' if not book[4] else f'На руках'

            def exam_book() -> Union[tuple, str]:
                """
                Функция вывода пользователя, если они брали книгу, иначе - сообщение о том, что книга в библиотеке
                """
                if book[6]:
                    self.DB.cursor.execute('''SELECT Users_db.id, Users_db.name, Users_db.email
                                                    FROM Library_db
                                                    JOIN Users_db ON Users_db.id=:foreight_key;''',
                                           dict(foreight_key=book[6]))

                    data_user = self.DB.cursor.fetchall()[0]
                    print(f'id пользователя: {data_user[0]}\n'
                          f'Имя пользователя: {data_user[1]}\n'
                          f'Почта для связи: {data_user[2]}')
                else:
                    print(f'Книга в библиотеке')

            print(f'id: {book[0]}\n'
                  f'Название: {book[1]}\n'
                  f'Автор: {book[2]}\n'
                  f'Год издания: {book[3]}\n'
                  f'Наличие: {availability}\n'
                  f'Индивидуальный номер: {book[5]}\n'
                  f'Местоположение книги:\n{exam_book()}\n')

    def register_user(self) -> None:  # метод регистрации нового пользователя библиотеки
        print(f'Регистрация нового пользователя')
        print('###################')
        name = input(f'Введите имя пользователя: ')
        email = input(f'Введите электронную почту пользователя')
        email_domain = re.findall(r'@+\S+', email)[0]
        domains = ['@mail.ru', '@gmail.com', '@rambler.ru', '@yahoo.com', '@yandex.ru']
        if email_domain in domains:
            self.DB.cursor.execute('''INSERT INTO Users_db(name, email) VALUES(?, ?);''', (name, email))
            self.DB.connection.commit()
        else:
            print(f'Введите правильный формат почты')
            self.register_user()

    def checkout_book(self) -> None:  # Метод выдачи книги выбранному пользователю
        user_id = int(input(f'Какому пользователю нужно выдать книгу? Введите его id\n'))
        self.DB.cursor.execute('''SELECT name FROM users_db WHERE id=:id;''', dict(id=user_id))
        name_user = self.DB.cursor.fetchall()[0][0]
        personal_number = int(input(f'Какую книгу вы хотите выдать пользователю {name_user}? '
                                    f'Введите уникальный номер книги\n'))
        self.DB.cursor.execute('''SELECT user_book_id FROM Library_db WHERE personal_number=:personal_number;''',
                               dict(personal_number=personal_number))

        user_book_id = self.DB.cursor.fetchall()[0][0]

        if user_book_id:
            print(f'Книга уже выдана другому пользователю! Введите номер другой книги')
            self.checkout_book()
        else:
            self.DB.cursor.execute('''UPDATE Library_db SET user_book_id = (SELECT id FROM Users_db WHERE id=:user_id)
                                        WHERE personal_number=:personal_number;''',
                                   dict(user_id=user_id, personal_number=personal_number))
            self.DB.connection.commit()

    def return_book(self) -> None:  # Метод возврата книги в библиотеку от пользователя
        user_id = int(input(f'Какой пользователь возвращает книгу? Введите id'))  # Вопрос юзеру
        self.DB.cursor.execute('''SELECT name, id FROM Users_db 
                                        WHERE id=:id;''',
                               dict(id=user_id))  # выбираем данные (имя, id) пользователя, id которого ввели

        user_data = self.DB.cursor.fetchall()[0]  # выводим эти данные в отдельный список

        self.DB.cursor.execute('''SELECT Library_db.id, Library_db.title, Library_db.personal_number 
                                        FROM Library_db
                                        WHERE user_book_id=:user_id;''',
                               dict(user_id=user_data[1]))  # выбираем все книги, которые взял пользователь

        user_books = self.DB.cursor.fetchall()  # выводим эти книги в список
        user_books_numbers = [book[-1] for book in user_books]  # выводим в отдельный список уникальные номера этих книг
        return_book_number = int(input(f'Какую книгу возвращает {user_data[0]}? '
                                       f'Введите ее уникальный номер\n'))

        # если веденного номера нет среди номеров книг, которые у пользователя
        if return_book_number not in user_books_numbers:
            print(f'Пользователь {user_data[0]} не брал такой книги! Введите правильный номер')
            self.return_book()  # перезапускаем метод
        # иначе
        else:
            # в следующем коде превращаем значение поля Foreign key в null у книги, уникальный номер которой
            # мы сохранили в return_book_number
            self.DB.cursor.execute('''UPDATE Library_db SET user_book_id=null 
                                            WHERE personal_number=:personal_number;''',
                                   dict(personal_number=return_book_number))  #
            self.DB.connection.commit()
            # выводим название книги из общего списка книг пользователя в отдельную строку по уникальному номеру книги
            title_return_book = ''.join([book[1] for book in user_books if book[-1] == return_book_number])
            print(f'Пользователь {user_data[0]} вернул книгу <{title_return_book}> в библиотеку! Молодец!')

    def checkout_report(self, for_return: bool) -> None:  # Метод создания отчета о книгах на руках
        self.DB.cursor.execute('''SELECT * FROM Library_db;''')  # Выбираем все книги таблицы
        all_books = self.DB.cursor.fetchall()  # Выводим их в отдельный список
        book_on_hands = [book for book in all_books if book[-1] is not None]  # список книг, которые на руках
        if not for_return:  # если данный метод запускается не для книг, которые в библиотеке
            print(f'На руках находится {len(book_on_hands)}/{len(all_books)} книг.')
        else:  # иначе
            print(f'В библиотеке находится книг: {len(all_books) - len(book_on_hands)} шт.')

    def return_report(self) -> Callable:  # Метод создания отчета о книгах библиотеке
        return self.checkout_report(for_return=True)  # запускаем предыдущий метод с параметром for_return

    def general_report(self) -> None:  # Метод создания общего главного отчета о состоянии библиотеки и пользователях
        print(self.checkout_report(for_return=True))  # Книги в библиотеке
        print(self.checkout_report(for_return=False))  # Книги на руках

        self.DB.cursor.execute('''SELECT * FROM Users_db;''')  # Все пользователя библиотеки
        library_users, number_user = self.DB.cursor.fetchall(), 1
        print(f'ПОЛЬЗОВАТЕЛИ:')
        print(f'######################')
        print(f'Список всех пользователей библиотеки:')
        for user in library_users:  # Красивый вывод всех пользователей библиотеки
            print(f'{number_user}. Имя: {user[1]}\nПочта: {user[2]}')
            number_user += 1
            print()

        self.DB.cursor.execute('''SELECT Library_db.id, Library_db.title, Library_db.personal_number, Users_db.name
                                    FROM Library_db
                                    JOIN Users_db ON Users_db.id=Library_db.user_book_id;''')
        users_book = self.DB.cursor.fetchall()  # выше sqlite запрос, а здесь вывод в список пользователей с книгами
        print(f'user book {users_book}')
        print(f'Список пользователей, которые взяли хотя бы одну книгу.')
        users_book_dict = {val[-1]: [] for val in users_book}
        print(users_book_dict)
        for data in users_book:  # создаем словарь из пользователей и списка книг, которые у них на руках
            if not users_book_dict[data[-1]]:
                number = 1
            else:
                number = int(users_book_dict[data[-1]][-1][0]) + 1
            users_book_dict[data[-1]].append(f'{number}.{data[1]}')

        for user, books in users_book_dict.items():  # выводим этот словарь
            books = '\n'.join(books)
            print(f'Пользователь {user} взял книги:\n{books}')
            print()
        print(f'######################')
        print(f'КНИГИ:')
        print(f'######################')
        print(f'Все книги:')
        self.DB.cursor.execute('''SELECT * FROM Library_db;''')
        all_books = list(map(list, self.DB.cursor.fetchall()))

        for book in all_books:  # делаем удобночитаемый вывод всех книг, которые есть в библиотеке и на руках

            if book[-1]:
                self.DB.cursor.execute('''SELECT name FROM Users_db WHERE id=:id;''', dict(id=book[-1]))
                book_location = f'Книга у {self.DB.cursor.fetchall()[0][0]}'
            else:
                book_location = f'В библиотеке'
            book[-1] = book_location
            print(' | '.join(list(map(str, book))))


lib = Library()
print(f'Добро пожаловать в онлайн библиотеку!')
commands = {
    1: lambda: lib.add_book(),
    2: lambda: lib.remove_book(),
    3: lambda: lib.find_book(),
    4: lambda: lib.register_user(),
    5: lambda: lib.checkout_book(),
    6: lambda: lib.return_book(),
    7: lambda: lib.checkout_report(False),
    8: lambda: lib.return_report(),
    9: lambda: lib.general_report()
}


def main() -> None:  # Функция запуска словаря лямбда функций с вызовами методов класса Library
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
        if start_app in list(range(1, 10)):
            commands[start_app]()
        else:
            print(f'Нет такого номера команды!')


if __name__ == '__main__':
    main()
