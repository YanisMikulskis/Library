import sqlite3

from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

# from sqlalchemy import create_engine, Column, Integer, String,Boolean, select, MetaData, ForeignKey
# from sqlalchemy.inspection import inspect
# from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship

from createDB import *
app = Flask(__name__)
@app.route('/')
def book():
    return f'{user_have_books}'

@app.route('/home')
def home():
    return render_template('hello.html')
#
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
#     return render_template('reg.html')
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
#     return render_template('reg.html') #при переходе по маршруту сразу генерится форма
#
#     # return render_template('reg.html')
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






