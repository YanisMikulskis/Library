import functools
import sqlite3

from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import jsonify
from flask import flash

# from sqlalchemy import create_engine, Column, Integer, String,Boolean, select, MetaData, ForeignKey
# from sqlalchemy.inspection import inspect
# from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship

from createDB import *

app = Flask(__name__)
app.secret_key = 'my_library'


@app.route('/')
def book():
    print('запущено')
    return f'{user_have_books}'


@app.route('/home')
def home():
    return render_template('hello.html')


@app.errorhandler(404)
def error404(error):
    return render_template('error404.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username:
            return redirect(url_for('home'))
        else:
            return error404(404)
    return render_template('login.html')


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


@app.route('/books_in_library')
def books_in_library():
    all_books = db_session.query(Library_Flask).filter(Library_Flask.user_book_id == None).all()
    books = [book for book in all_books]
    books_dict = {
        'Общая база книг в библиотеке': []
    }

    for book in books:
        dict_book = {
            'personal_number': book.personal_number,
            'title': book.title,
            'author': book.author,
            'year': book.year,
            'count': db_session.query(func.count(Library_Flask.id).filter(Library_Flask.title == book.title)).scalar()
        }
        books_dict['Общая база книг в библиотеке'].append(dict_book)

    print(books_dict)

    return render_template('books_in_library.html', books_dict=books_dict)


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
