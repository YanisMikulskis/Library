import os

from sqlalchemy import create_engine, Column, Integer, String,Boolean, select, MetaData, ForeignKey
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship
from sqlalchemy import desc, func
from Book_for_flask import make_books
from faker import Faker
import sqlite3

import os

connect = sqlite3.connect('Library_Database_Flask')
# cursor = connect.cursor()
# cursor.execute('''
#             CREATE TABLE IF NOT EXISTS Flask_Table_Users
#             (
#             id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#             name VARCHAR(100) NOT NULL,
#             email VARCHAR(100) NOT NULL UNIQUE
#             )'''
#         )
#
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS Flask_Table_Library
#         (
#         id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#         title VARCHAR(150) NOT NULL,
#         author VARCHAR(100) NOT NULL,
#         year VARCHAR(4) NOT NULL,
#         is_checked_out INTEGER NOT NULL,
#         personal_number INTEGER NOT NULL UNIQUE,
#         user_book_id INTEGER,
#         FOREIGN KEY(user_book_id) REFERENCES Flask_Table_Users(id)
#         )
# ''')
engine = create_engine('sqlite:///Library_Database_Flask')
metadata = MetaData()

class Base(DeclarativeBase):
    pass

class Library_Flask(Base):
    __tablename__ = 'Flask_Table_Library'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(String(150), nullable=False)
    author = Column(String(100), nullable=False)
    year = Column(String(4), nullable=False)
    is_checked_out = Column(Integer, nullable=False)
    personal_number = Column(Integer, nullable=False, unique=True)
    user_book_id = Column(Integer, ForeignKey('Flask_Table_Users.id'))

    users = relationship('User_Flask', back_populates='books')
    def __repr__(self):
        return f'number: %r\npk: %r\ntitle: %r\nauthor: %r\nyear: %r\n' % (self.personal_number, self.id, self.title, self.author, self.year)


class User_Flask(Base):
    __tablename__ = 'Flask_Table_Users'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(64), nullable=True, unique=False)
    books = relationship('Library_Flask', back_populates='users')
    def __repr__(self):
        return f'name: %r\nemail: %r\nbooks: %r\n' % (self.name, self.email, self.books)
Base.metadata.create_all(bind=engine)
session = sessionmaker(autoflush=False, bind=engine)
db_session = session()


# book = ['Влюбленные в книги не спят в одиночестве', 'Современная зарубежная литература', '2015']
# title_book = book[0]
# author_book = book[1]
# year = book[2]
#
#
# new_book = Library_Flask(title=title_book,
#                          author=author_book,
#                          year=year,
#                          is_checked_out=1,
#                          personal_number=1000,
#                          user_book_id=None)
#
# db_session.add_all([new_book])
faker_ = Faker('ru-RU')
# for user in range(2):
# new_user = User_Flask(
#     name=faker_.first_name_male(),
#     email=faker_.ascii_free_email()
# )
#
# db_session.add_all([new_user])
# db_session.commit()



# #вывести название книги по id в условии (может варьироваться)
# book_test = db_session.query(Library_Flask).filter(Library_Flask.id==78).first().title
#
# user_test = db_session.query(User_Flask).filter(User_Flask.id==6).first()
#
# user_have_books = db_session.query(User_Flask).filter(User_Flask.name=='Виктория').first().name
# # print(user_have_books)
# book_in_library = db_session.query(Library_Flask).filter(Library_Flask.user_book_id==0).all()
#
# #Какие книги находятся у Виктории?
# book_vik = db_session.query(User_Flask).filter(User_Flask.name=='Виктория').first().books
# #Выдадим Виктории книгу Стивена Кинга
# # book_vik_add = db_session.query(User_Flask).filter(User_Flask.name=='Виктория').first() #Виктория
# # King = db_session.query(Library_Flask).filter(Library_Flask.author=='Стивен Кинг').first() #Кинг
# # book_vik_add.books.extend([King]) if King.user_book_id is None else ...#Выдаем
# # db_session.commit() #Сохраняем изменения в БД
#
#
# #Какие книги в библиотеке?
# all_books = db_session.query(Library_Flask).filter(Library_Flask.user_book_id==None).all()
#
#
# #Каких в библиотеке нет?
#
# # not_books = [book.user_book_id for book in db_session.query(Library_Flask).all()]
# not_books = db_session.query(Library_Flask).filter(Library_Flask.user_book_id==None).all()
# # print(f'В библиотеке сейчас следущие книги:\n')
# # for book in not_books:
# #     print(book.title)
# #Какие читатели взяли хотя бы одну книгу?
#
#
#
# #добавить кингу в библиотеку
# last_number = db_session.query(Library_Flask).order_by(Library_Flask.id.desc()).all()[0].personal_number
# print(last_number)
# # выше обратная сортировка таблицы(order_by(Library_Flask.id.desc())), вывод списка всех результатов, дальше индекс а потом атрибут
#
# test_book = Library_Flask(title='title test',
#                           author='title author',
#                           year='title year',
#                           is_checked_out=1,
#                           personal_number = last_number + 1,
#                           user_book_id = None) # создаем книгу
# # db_session.add_all([test_book]) # добавляем в бд
# # db_session.commit()# коммитим
# counts = {
#
# }
# #пожсчет элементов в таблицу по элементу столбца "в данном случае по названию книги"
# lines_title = db_session.query(func.count(Library_Flask.id).filter(Library_Flask.title == 'Джон Картер на Марсе')).scalar()
#
# #порядковый номер последнего элемента
# last_number = db_session.query(Library_Flask).order_by(Library_Flask.personal_number.desc()).first().personal_number
#
# bookkk = db_session.query(Library_Flask).filter(Library_Flask.id==-1).first()
# #выбор всех id и приведение их к нормальному виду
# all_id = list(map(lambda id_book: str(list(id_book)[0]), db_session.query(Library_Flask.id).all()))
#
#
#
# book_on_hand = db_session.query(Library_Flask).filter(Library_Flask.personal_number==58900).first()
# print(book_on_hand)
# # books = db_session.query(Library_Flask).all()
# #
# # users = db_sessionquery(User_Flask).all()
# # for i in users:
# #     print(i)





#АЛЕМБИК. Чтобы эта дичь нормально работала делаем следующее:

#1. Если мы базу еще не создали. Базу мы создаем с помощью питоновского sqlite
#Прописываем connect = sqlite3.connect('Library_Database_Flask')
#            cursor = connect.cursor() или что то аналогичное



#2. Дальше работаем уже только с помощью sqlalchemy. Подключаемся к созданной базе, делаем движок и тд(выше пример)
#   Прописываем таблицы через ООП. Каждая таблица - это модель. Прописываем все настройки.
# Если база уже была создана, то мы делаем тоже самое, только классы таблиц будут уже не создавать таблицы, а иметь только
# информационную пользу и будут юзаться алембиком для создания миграций. В любом случае, в них мы всегда должны описывать таблицу





# 3.Устанавливаем алембик PIP

# 4. Создаем файлик session. Из нашего модуля с таблицами SQLalchemy импортируем туда класс Base
# Затем создаем функцию, импортируем оставшиеся модели из модуля с таблицами SQLAlchemy и возвращаем Base


#5. В файле env.py (который установился вместе с алембиком) прописываем:
#Переходим в директорию с файликом session
#Импортируем функцию, которая возвращает Base
# target_metadata = наша функция().metadata
# и больше ничего не трогаем.


#6. В файле alembic.ini устанавливаем путь к нашей БД и прописываем настройки:
# script_location = src/migrations -- создает папку для миграций
# prepend_sys_path = . src --- переходит в созданную папку src для взаимодействия со script.py.mako и env.py
# sqlalchemy.url = sqlite:///Library_Database_Flask -- путь к бд SQLITE3


#7.alembic revision --message='initial' --autogenerate -- запуск тестовой миграции
# Если в ПЕРВОЙ миграции в upgrade и downgrade везде None значит все ок
#alembic upgrade (downgrade) head -- применить самую новую(самую старую) миграции. Если нужна определенная - то вместо
# head пишем ее номер без(_сообщения в ней)


