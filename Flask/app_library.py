import functools
import sqlite3

import sqlalchemy.orm.collections
import werkzeug.exceptions
import hashlib
from flask import Flask, render_template, redirect, url_for, request, jsonify, flash
from Book_for_flask import make_books
import re
from createDB import *
from typing import Callable, Union

app = Flask(__name__)
app.secret_key = 'my_library'
InstrumentedList: type = sqlalchemy.orm.collections.InstrumentedList


@app.route('/')
def start_page() -> Callable:
    """
    Стартовая страница
    """
    return render_template('start_page.html')


@app.errorhandler(404)
def error404(error) -> Callable:
    """
    Ошибка 404
    """
    return render_template('error404.html')


@app.route('/personal_area')
def personal_area() -> Callable:
    """
    Личный кабинет читателя
    """
    username: str = request.args.get('username')
    email_form: str = request.args.get('email_form')
    return render_template('personal_area.html', username=username, email_form=email_form)


@app.route('/login', methods=['GET', 'POST'])
def login() -> Callable:
    """
    Авторизация читателя
    """
    if request.method == 'POST':
        email_form: str = request.form['email']
        password_form: str = request.form['password']
        username: str = db_session.query(User_Flask).filter(User_Flask.email == email_form).first().name

        password: Union[str, None] = (db_session.query(User_Flask).
                                      filter(User_Flask.email == email_form).
                                      first().password)
        if password is not None:
            if hashlib.sha256(password_form.encode('utf-8')).hexdigest() == password:
                return redirect(url_for('personal_area',
                                        username=username,
                                        email_form=email_form))
            else:
                flash(f'Неправильный пароль!')
        else:
            if username:
                return redirect(url_for('personal_area',
                                        username=username,
                                        email_form=email_form))
            else:
                flash(f'Нет такого пользователя!')
    return render_template('login.html')


@app.route('/my_book')
def my_book() -> Callable:
    """
    Книги читателя
    """
    email_form: str = request.args.get('email_form')

    try:
        book_username: InstrumentedList = (db_session.query(User_Flask).
                                           filter(User_Flask.email == email_form).
                                           first().books)
    except AttributeError:  # Если мы хотим посмотреть список книг, но пока не залогинились
        return redirect(error404)
    else:
        if not book_username:
            message_not_books: str = f'Вам пока не выдавали книги! Приходите в библиотеку'
            return render_template('my_book.html', message_not_books=message_not_books)
        else:
            return render_template('my_book.html', book_username=book_username)


@app.route('/menu')
def menu() -> Callable:
    """
    Главное меню библиотеки
    """
    return render_template('menu.html')


@app.route('/add_book', methods=['POST', 'GET'])
def add_book() -> Callable:
    """
    Добавление книги в библиотеку
    """
    if request.method == 'POST':
        def get_number_book() -> int:
            number_book: int = (db_session.query(Library_Flask)
                                .order_by(Library_Flask.personal_number.desc())
                                .first().personal_number) + 1
            return number_book

        try:

            title_book: str = request.form['title_book']
            author_book: str = request.form['author_book']
            year_book: str = request.form['year_book']
            new_book: Library_Flask = Library_Flask(title=title_book,
                                                    author=author_book,
                                                    year=year_book,
                                                    is_checked_out=1,
                                                    personal_number=get_number_book(),
                                                    user_book_id=None)
            flash(message='Книга добавлена!')
            data_book: list = [title_book, author_book, year_book]
            if all(data_book):
                db_session.add_all([new_book])
                db_session.commit()

        except werkzeug.exceptions.BadRequestKeyError:
            count_book: str = request.form['count_book']
            if count_book.isdigit():
                books_network: list = make_books(int(count_book))
            else:
                flash(message='Введите цифру!')
                return render_template('add_book_ordinary.html')

            for data_book in books_network:
                title_book: str = data_book[0]
                author_book: str = data_book[1]
                year_book: str = data_book[2]
                new_book: Library_Flask = Library_Flask(title=title_book,
                                                        author=author_book,
                                                        year=year_book,
                                                        is_checked_out=1,
                                                        personal_number=get_number_book(),
                                                        user_book_id=None)
                db_session.add_all([new_book])
                db_session.commit()
                flash(message=f'Книга \'{title_book}\' из Сети добавлена!')

                return render_template('add_book_ordinary.html', stop=True)

    return render_template('add_book_ordinary.html', stop=False)


@app.route('/remove_book', methods=['POST', 'GET'])
def remove_book() -> Callable:
    """
    Удаление книги из библиотеки
    """
    if request.method == 'POST':
        try:
            one_book_id_from_form: str = request.form['one_book_remove']
            some_book_id_from_form: NoneType = None

        except werkzeug.exceptions.BadRequestKeyError:
            one_book_id_from_form: NoneType = None
            some_book_id_from_form: str = request.form['some_book_remove']

        if one_book_id_from_form:
            book_deleted: Library_Flask = (db_session.query(Library_Flask).
                                           filter(Library_Flask.id == one_book_id_from_form).first())
            if book_deleted is None:
                flash('Нет книги с таким id')
            else:
                db_session.delete(book_deleted)
                db_session.commit()
                flash('Книга удалена!')
        else:
            if ',' not in some_book_id_from_form:
                flash(message=f'Введите данные через запятую!')
            else:
                form_list_data: list = some_book_id_from_form.split(',')
                all_id: list = list(map(lambda x: str(x[0]), db_session.query(Library_Flask.id).all()))
                id_check: list = []
                for i in form_list_data:
                    id_check.append(True) if i in all_id else id_check.append(False)

                if not all(id_check):
                    flash('Один или несколько введенных id нет в таблице книг!')
                else:
                    for book_id in form_list_data:
                        book_deleted: list = (db_session.query(Library_Flask).
                                              filter(Library_Flask.id == book_id).first())
                        db_session.delete(book_deleted)
                        db_session.commit()
                    flash('Книги удалены!')
    return render_template('remove_book_ordinary.html')


@app.route('/search_book', methods=['POST', 'GET'])
def search_book() -> Callable:
    """
    Поиск книги в библиотеке
    """
    if request.method == 'POST':
        result_search: str = request.form['search_book']
        result_book: Library_Flask = db_session.query(Library_Flask).filter(Library_Flask.id == result_search).first()
        if result_book is not None:
            if result_book.user_book_id is None:
                availability: str = f'В библиотеке'
            else:
                info: str = f'Книга у читателя'
                name_reader: str = (db_session.query(User_Flask).
                                    filter(User_Flask.id == result_book.user_book_id).first().name)
                availability: str = f'{info}: {name_reader}'
            data_book: dict = {'Уникальный номер книги': result_book.personal_number,
                               'Название': f'\'{result_book.title}\'',
                               'Автор': result_book.author,
                               'Год написания': result_book.year,
                               'Наличие книги': availability
                               }
            for explanation, data in data_book.items():
                flash(f'{explanation}: {data}')
        else:
            flash(f'Нет книги с таким id!')
    return render_template('search_book.html')


@app.route(f'/new_reader', methods=['POST', 'GET'])
def new_reader() -> Callable:
    """
    Регистрация нового читателя
    """
    if request.method == 'POST':
        name_reader: str = request.form['name_reader']
        email_reader: str = request.form['email_reader']
        email_domain: str = re.findall(r'@+\S+', email_reader)[0]
        domains: list = ['@mail.ru', '@gmail.com', '@rambler.ru', '@yahoo.com', '@yandex.ru']

        password_reader: str = request.form['password_reader']
        if not password_reader:
            hashed_password: NoneType = None
        else:
            hashed_password: str = hashlib.sha256(password_reader.encode('utf-8')).hexdigest()

        if email_domain in domains:
            new_user: User_Flask = User_Flask(name=name_reader,
                                              email=email_reader,
                                              password=hashed_password)
            db_session.add_all([new_user])
            db_session.commit()
            db_session.rollback()
            flash(f'Читатель зарегистрирован')
        else:
            flash(f'Неправильный ввод почты!')
    return render_template('new_reader.html')


@app.route('/checkout_book', methods=['POST', 'GET'])
def checkout_book():
    """
    Выдача книги читателю
    """
    if request.method == 'POST':
        select_reader_id: str = request.form['id_reader']
        select_book_number: str = request.form['number_book']
        reader: User_Flask = (db_session.query(User_Flask).
                              filter(User_Flask.id == select_reader_id).first())

        book: Library_Flask = (db_session.query(Library_Flask).
                               filter(Library_Flask.personal_number == select_book_number).first())
        if reader and book:
            if book.user_book_id is None:
                reader.books.extend([book])
                db_session.commit()
                db_session.rollback()
                flash(f'Книга \'{book.title}\' выдана пользователю {reader.name}')
            else:
                flash(f'Эта книга уже на руках!')
        else:
            flash(f'Пользователя и/или книги с такими данными не найдено!')
    return render_template('checkout_book.html')


@app.route('/return_book', methods=['POST', 'GET'])
def return_book() -> Callable:
    """
    Возврат книги читателем
    """
    if request.method == 'POST':
        input_reader_id: str = request.form['id_reader']
        input_book_number: str = request.form['number_return_book']

        reader: User_Flask = (db_session.query(User_Flask).
                              filter(User_Flask.id == input_reader_id).first())

        book: Library_Flask = (db_session.query(Library_Flask).
                               filter(Library_Flask.personal_number == input_book_number).first())

        if reader and book:
            if book.user_book_id is not None:
                book.user_book_id = None
                db_session.commit()
                flash(f'Книга {book.title} возвращена в библиотеку читателем {reader.name}!')
            else:
                flash(f'Эта книга уже в библиотеке!')
        else:
            flash(f'Пользователя и/или книги с такими данными не найдено!')
    return render_template('return_book.html')


def books_sorted_func(hand: bool) -> list:
    """
    Сортировка книг по алфавиту (на руках или в библиотеке)
    """
    books_sorted: list = (db_session.query(Library_Flask).
                          filter(Library_Flask.user_book_id.__ne__(None) if hand else Library_Flask.user_book_id).all())
    return books_sorted


@app.route('/books_on_hand')
def books_on_hand() -> Callable:
    """
    Книги на руках. Отчет
    """
    books_dict = {
        f'Книги на руках и читатели': []
    }

    books_sorted: list = books_sorted_func(hand=True)
    for book in books_sorted:
        name_reader: str = db_session.query(User_Flask).filter(User_Flask.id == book.user_book_id).first().name
        email_reader: str = db_session.query(User_Flask).filter(User_Flask.id == book.user_book_id).first().email
        book_data: dict = {
            'title': f'\'{book.title}\'',
            'personal_number': book.personal_number,
            'reader': name_reader,
            'email_reader': email_reader
        }
        books_dict[f'Книги на руках и читатели'].append(book_data)

    return render_template('books_on_hand.html', books_dict=books_dict)


@app.route('/books_in_library')
def books_in_library() -> Callable:
    """
    Книги в библиотеке. Отчет
    """
    books_sorted: list = books_sorted_func(hand=False)
    books_dict: dict = {
        'Общая база книг в библиотеке': []
    }

    for book in books_sorted:
        dict_book: dict = {
            'personal_number': book.personal_number,
            'title': f'\'{book.title}\'',
            'author': book.author,
            'year': book.year,
            'count': db_session.query(func.count(Library_Flask.id).filter(Library_Flask.title == book.title)).scalar()
        }
        books_dict['Общая база книг в библиотеке'].append(dict_book)

    return render_template('books_in_library.html', books_dict=books_dict)


@app.route('/general_report')
def general_report() -> Callable:
    """
    Полный отчет о состоянии библиотеки
    """
    count_books: int = db_session.query(func.count(Library_Flask.id)).scalar()

    # Общее количество книг в библиотеке

    all_books_sorted: list = db_session.query(Library_Flask).order_by(Library_Flask.title).all()
    all_books_dict: dict = {  # !
        f'Список всех книг:': []
    }

    for book in all_books_sorted:
        book_dict: dict = {
            'title': f'\'{book.title}\'',
            'author': book.author,
            'year': book.year,
            'universal_number': book.personal_number,
            'count': db_session.query(func.count(Library_Flask.id).filter(Library_Flask.title == book.title)).scalar(),
            'hand': f'В библиотеке' if book.user_book_id is None else
            f'Книга у читателя:{db_session.query(User_Flask).filter(User_Flask.id == book.user_book_id).first().name}'

        }
        all_books_dict[f'Список всех книг:'].append(book_dict)

    hand_books: int = len(books_sorted_func(hand=True))  # Количество на руках #1
    library_books: int = len(books_sorted_func(hand=False))  # Количество в библиотеке #1

    readers_count: int = db_session.query(func.count(User_Flask.id)).scalar()  # Количество читателей #1
    readers: list = db_session.query(User_Flask).all()
    # -----------------
    all_readers: dict = {
        'Читатели:': []
    }

    for reader in readers:
        reader_dict: dict = {
            'name': reader.name,
            'email': reader.email,
            'books': len(reader.books)
        }
        all_readers['Читатели:'].append(reader_dict)

    readers_active: list = db_session.query(User_Flask).filter(
        User_Flask.books.__ne__(None)).all()  # Список читателей которые взяли хотя бы одну книгу #!
    readers_active: list = [reader.name for reader in readers_active]

    return render_template('general_report.html',
                           count_books=count_books,
                           all_books_dict=all_books_dict,
                           hand_books=hand_books,
                           library_books=library_books,
                           readers_count=readers_count,
                           all_readers=all_readers,
                           readers_active=readers_active)


if __name__ == '__main__':
    app.run(debug=True)
