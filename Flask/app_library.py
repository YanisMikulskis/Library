import functools
import sqlite3

import werkzeug.exceptions
import hashlib
from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import jsonify
from flask import flash
import re

# from sqlalchemy import create_engine, Column, Integer, String,Boolean, select, MetaData, ForeignKey
# from sqlalchemy.inspection import inspect
# from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship

from createDB import *

app = Flask(__name__)
app.secret_key = 'my_library'


@app.route('/')
def book():
    print('запущено')
    return render_template('start_page.html')




@app.route('/home')
def home():
    return render_template('hello.html')


@app.errorhandler(404)
def error404(error):
    return render_template('error404.html')



def user_active(username):
    return username
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_form = request.form['email']
        password_form = request.form['password']
        username = db_session.query(User_Flask).filter(User_Flask.email==email_form).first().name
        password = db_session.query(User_Flask).filter(User_Flask.email==email_form).first().password
        if password is not None:
            if hashlib.sha256(password_form.encode('utf-8')).hexdigest() == password:
                return render_template('hello.html', username=username, email=email_form)
            else:
                flash(f'Неправильный пароль!')
        else:
            if username:
                return render_template('hello.html', username=username, email=email_form)
            else:
                flash(f'Нет такого пользователя!')
    return render_template('login.html')

@app.route('/my_book')
def my_book():
    email = request.args.get('email')
    book_username = db_session.query(User_Flask).filter(User_Flask.email==email).first().books
    if not book_username:
        message_not_books = f'Вам пока не выдавали книги! Приходите в библиотеку'
        return render_template('my_book.html', message_not_books = message_not_books)
    else:

        return render_template('my_book.html', book_username=book_username, email=email)





@app.route('/menu')
def menu():
    return render_template('menu.html')


@app.route('/add_book', methods=['POST', 'GET'])
def add_book():
    if request.method == 'POST':
        title_book = request.form['title_book']
        author_book = request.form['author_book']
        year_book = request.form['year_book']
        number_book = (db_session.query(Library_Flask)
                       .order_by(Library_Flask.personal_number.desc())
                       .first().personal_number) + 1
        new_book = Library_Flask(title=title_book,
                                 author=author_book,
                                 year=year_book,
                                 is_checked_out=1,
                                 personal_number=number_book,
                                 user_book_id=None)
        flash(message='Книга добавлена!')
        data_book = [title_book, author_book, year_book]
        if all(data_book):
            db_session.add_all([new_book])
            db_session.commit()

    else:
        flash(message='Введите данные')
    return render_template('add_book_ordinary.html')

@app.route('/remove_book', methods = ['POST', 'GET'])
def remove_book():
    if request.method == 'POST':
        # тут мы отлавливаем ошибку werkzeug.exceptions.BadRequestKeyError
        # эта ошибка связана с отсутствием формы в шаблоне. Такая ситуация происходит с формой ввода ОДНОГО id тогда и только
        # тогда (в данном случае) когда мы нажимаем кнопку all (т.е. хотим ввести НЕСКОЛЬКО id для удаления книг, а не одно). Также происходит и наоборот
        # В шаблоне на JS я реализовал механизм нахождения на странице только одной формы, тобиш если мы хотим удалить
        # одну книгу, то появляется соответствующая форма, а форма для ввода нескольких id исчезает (и наоборот)
        try:
            one_book_id_from_form = request.form['one_book_remove']
            some_book_id_from_form = None
        except werkzeug.exceptions.BadRequestKeyError:
            one_book_id_from_form = None
            some_book_id_from_form = request.form['some_book_remove']

        if one_book_id_from_form:
            remove_book = (db_session.query(Library_Flask).
                           filter(Library_Flask.id == one_book_id_from_form).first())
            if remove_book is None:
                flash('Нет книги с таким id')
            else:
                db_session.delete(remove_book)
                db_session.commit()
                flash('Книга удалена!')
        else:
            form_list_data = some_book_id_from_form.split(',')
            form_list_data = [''.join([s for s in num if s.isdigit()]) for num in form_list_data]#введенные id приведенные к норм виду
            all_id = list(map(lambda i: str(i[0]), db_session.query(Library_Flask.id).all())) #все id таблицы
            id_check = []
            for i in form_list_data:
                id_check.append(True) if i in all_id else id_check.append(False)

            if not all(id_check):
                flash('Один или несколько введенных id нет в таблице книг!')
            else:
                for book_id in form_list_data:
                    remove_book = (db_session.query(Library_Flask).
                                   filter(Library_Flask.id == book_id).first())
                    db_session.delete(remove_book)
                    db_session.commit()
                flash('Книги удалены!')
    return render_template('remove_book_ordinary.html')
@app.route('/search_book', methods = ['POST', 'GET'])
def search_book():
    found_book = {
    }
    if request.method == 'POST':
        result_search = request.form['search_book']
        result_book = db_session.query(Library_Flask).filter(Library_Flask.id==result_search).first()
        if result_book is not None:
            if 'Результат' not in found_book:
                found_book.setdefault(f'Результат', [])
            data_book = {'Уникальный номер книги': result_book.personal_number,
                         'Название': result_book.title,
                         'Автор': result_book.author,
                         'Год написания': result_book.year,
                         'Наличие книги': f'В библиотеке' if result_book.user_book_id is None
                                        else f'Книга у читателя:{db_session.query(User_Flask).filter(User_Flask.id==result_book.user_book_id).first().name}'
                         }

            for explanation, data in data_book.items():
                flash(f'{explanation}: {data}')
        else:
            flash(f'Нет книги с таким id!')
    return render_template('search_book.html', found_book=found_book)


@app.route(f'/new_reader', methods = ['POST', 'GET'])
def new_reader():
    if request.method == 'POST':
        name_reader = request.form['name_reader']

        email_reader = request.form['email_reader']
        email_domain = re.findall(r'@+\S+', email_reader)[0]
        domains = ['@mail.ru', '@gmail.com', '@rambler.ru', '@yahoo.com', '@yandex.ru']

        password_reader = request.form['password_reader']
        hashed_password = None if not password_reader else hashlib.sha256(password_reader.encode('utf-8')).hexdigest()

        if email_domain in domains:
            new_reader = User_Flask(name=name_reader,
                                    email=email_reader,
                                    password = hashed_password)
            db_session.add_all([new_reader])
            db_session.commit()
            flash(f'Читатель зарегистрирован')
        else:
            flash(f'Неправильный ввод почты!')
    return render_template('new_reader.html')

@app.route('/checkout_book', methods=['POST', 'GET'])
def checkout_book():
    if request.method == 'POST':
        select_reader_id = request.form['id_reader']
        select_book_number = request.form['number_book']
        reader = (db_session.query(User_Flask).
                  filter(User_Flask.id==select_reader_id).first())
        book = (db_session.query(Library_Flask).
                filter(Library_Flask.personal_number==select_book_number).first())
        if reader and book:
            if book.user_book_id is None:
                reader.books.extend([book])
                db_session.commit()
                flash(f'Книга выдана пользователю {reader.name}')
            else:
                flash(f'Эта книга уже на руках!')
        else:
            flash(f'Пользователя и/или книги с такими данными не найдено!')
    return render_template('checkout_book.html')

@app.route('/return_book', methods = ['POST', 'GET'])
def return_book():
    if request.method == 'POST':
        input_reader_id = request.form['id_reader']
        input_book_number = request.form['number_return_book']

        reader = (db_session.query(User_Flask).
                  filter(User_Flask.id==input_reader_id).first())

        book = (db_session.query(Library_Flask).
                filter(Library_Flask.personal_number==input_book_number).first())

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





def books_sorted_func(hand:bool) -> list:
    books_sorted = (db_session.query(Library_Flask).
                    filter(Library_Flask.user_book_id != None if hand else Library_Flask.user_book_id == None).
                    order_by(Library_Flask.title).all())
    return books_sorted

@app.route('/books_on_hand')
def books_on_hand():
    books_dict = {
    f'Книги на руках и читатели':[]
    }

    books_sorted = books_sorted_func(hand=True)
    for book in books_sorted:
        name_reader = db_session.query(User_Flask).filter(User_Flask.id == book.user_book_id).first().name
        email_reader = db_session.query(User_Flask).filter(User_Flask.id == book.user_book_id).first().email
        book_data = {
            'title': book.title,
            'personal_number': book.personal_number,
            'reader': name_reader,
            'email_reader': email_reader
        }
        books_dict[f'Книги на руках и читатели'].append(book_data)


    return render_template('books_on_hand.html', books_dict=books_dict)

@app.route('/books_in_library')
def books_in_library():

    books_sorted = books_sorted_func(hand=False)
    books_dict = {
        'Общая база книг в библиотеке': []
    }

    for book in books_sorted:
        dict_book = {
            'personal_number': book.personal_number,
            'title': book.title,
            'author': book.author,
            'year': book.year,
            'count': db_session.query(func.count(Library_Flask.id).filter(Library_Flask.title == book.title)).scalar()
        }
        books_dict['Общая база книг в библиотеке'].append(dict_book)



    return render_template('books_in_library.html', books_dict=books_dict)

@app.route('/general_report')
def general_report():
    count_books = db_session.query(func.count(Library_Flask.id)).scalar()
     #Общее количество книг в библиотеке

    all_books_sorted = db_session.query(Library_Flask).order_by(Library_Flask.title).all()
    all_books_dict = { #!
        f'Список всех книг:': []
    }

    for book in all_books_sorted:
        book_dict = {
            'title': book.title,
            'author': book.author,
            'year': book.year,
            'universal_number': book.personal_number,
            'count': db_session.query(func.count(Library_Flask.id).filter(Library_Flask.title==book.title)).scalar(),
            'hand': f'В библиотеке' if book.user_book_id is None else
                    f'Книга у читателя:{db_session.query(User_Flask).filter(User_Flask.id==book.user_book_id).first().name}'

        }
        all_books_dict[f'Список всех книг:'].append(book_dict)

    hand_books = len(books_sorted_func(hand=True))#Количество на руках #1
    library_books = len(books_sorted_func(hand=False))# Количество в библиотеке #1

    readers_count = db_session.query(func.count(User_Flask.id)).scalar()# Количество читателей #1
    readers = db_session.query(User_Flask).all()
    #-----------------
    all_readers = {
        'Читатели:': []
    }

    for reader in readers:
        reader_dict = {
            'name': reader.name,
            'email': reader.email,
            'books': len(reader.books)
        }
        all_readers['Читатели:'].append(reader_dict)

    # -----------------
    # Список читателей (всех)

    readers_active = db_session.query(User_Flask).filter(User_Flask.books != None).all() # Список читателей которые взяли хотя бы одну книгу #!
    readers_active = [reader.name for reader in readers_active]

    return render_template('general_report.html',
                           count_books = count_books,
                           all_books_dict=all_books_dict,
                           hand_books=hand_books,
                           library_books=library_books,
                           readers_count=readers_count,
                           all_readers=all_readers,
                           readers_active=readers_active)


# @app.route('\personal_area')
# def personal_area():


    # return render_template('personal_area.html')
# @app.route('/login', methods=['POST', 'GET'])
# def login():

# def connect_db():
#     connection = sqlite3.connect('Library_FLASK_DB')
#     connection.row_factory = sqlite3.Row
#     return connection
# @app.route('/')
# def hello_library():
#     # connection = connect_db()
#     # cursor = connection.cursor()
#     # cursor.execute('''SELECT * FROM Library_table_flask;''')
#     # books = '\n'.join(list(map(str, list(map(dict, cursor.fetchall())))))
#     #
#     # print(books)
#
#     return f'Hello, Library!'
#
#
# @app.errorhandler(404)
# def error404(error):
#     return render_template('error404.html')
#
# @app.route('/home')
# def home():
#     return render_template('menu.html')
#
#
#
#
# if __name__ == '__main__':
#     app.run(debug=True)


# @app.route('/')
# def hello_world():
#     return 'Hello, world'
#
# @app.route('/about') # маршрут
# def about(): # функция действия в конце маршрута
#     return f'This is about page' #то что будет на странице, когда перейдем по маршруту
#
# @app.route('/user/<username>')
# def show_user_profile(username):
#     return f' User {username}'
#
# @app.route('/hello/<name>')
# def hello(name):
#     surname = 'смирнов'
#     return render_template('hello.html', name=name, surname=surname)
#
# @app.route('/greet/<username>')
# def greet(username):
#     return f'Hello, dear {username}!!'
#
#
#
# @app.route('/submit', methods = ['POST', 'GET'])
# def submit():
#
#     if request.method == 'POST': #если нажимаем кнопку submit (тут POST означает именно ОТПРАВКУ данных)
#
#         name = request.form.get('name') #забираем имя которое мы ввели ранее в форме
#         surname = request.form.get('surname')
#         return f'hello, forms and {len(name)}  {surname}!!'
#
#     return render_template('menu.html') #при переходе по маршруту сразу генерится форма
#
#     # return render_template('menu.html')
#
#
# @app.route('/data')
# def data():
#     return jsonify({'key':'value'})
#
#
#
#
#
# #подключение к БД
#
#
#
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
# db = SQLAlchemy(app)
#
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True,nullable=False)
#     email = db.Column(db.String(120), unique=True,nullable=False)
#
#     def __repr__(self):
#         return f'<User {self.username}>'
#
#
# new_user = User(username='newuser',email='newuser@mail.ru')
# db.session.add(new_user)
# db.session.commit()
#
if __name__ == '__main__':
    app.run(debug=True)
