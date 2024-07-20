import os

from sqlalchemy import create_engine, Column, Integer, String,Boolean, select, MetaData, ForeignKey
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship
from sqlalchemy import desc, func
import os
engine = create_engine('sqlite:///Library_FLASK_DB')
metadata = MetaData()

class Base(DeclarativeBase):
    pass

class Library_Flask(Base):
    __tablename__ = 'Library_table_flask'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(150), nullable=False)
    author = Column(String(100), nullable=False)
    year = Column(String(4), nullable=False)
    is_checked_out = Column(Boolean, nullable=False)
    personal_number = Column(Integer, nullable=False)
    user_book_id = Column(Integer, ForeignKey('Users_table_flask.id'))

    users = relationship('User_Flask', back_populates='books')
    def __repr__(self):
        return f'number: %r\npk: %r\ntitle: %r\nauthor: %r\nyear: %r\n' % (self.personal_number, self.id, self.title, self.author, self.year)


class User_Flask(Base):
    __tablename__ = 'Users_table_flask'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)

    books = relationship('Library_Flask', back_populates='users')
    def __repr__(self):
        return f'name: %r\nemail: %r\nbooks: %r\n' % (self.name, self.email, self.books)
Base.metadata.create_all(bind=engine)
session = sessionmaker(autoflush=False, bind=engine)
db_session = session()
#вывести название книги по id в условии (может варьироваться)
book_test = db_session.query(Library_Flask).filter(Library_Flask.id==78).first().title

user_test = db_session.query(User_Flask).filter(User_Flask.id==6).first()

user_have_books = db_session.query(User_Flask).filter(User_Flask.name=='Виктория').first().name
# print(user_have_books)
book_in_library = db_session.query(Library_Flask).filter(Library_Flask.user_book_id==0).all()

#Какие книги находятся у Виктории?
book_vik = db_session.query(User_Flask).filter(User_Flask.name=='Виктория').first().books
#Выдадим Виктории книгу Стивена Кинга
# book_vik_add = db_session.query(User_Flask).filter(User_Flask.name=='Виктория').first() #Виктория
# King = db_session.query(Library_Flask).filter(Library_Flask.author=='Стивен Кинг').first() #Кинг
# book_vik_add.books.extend([King]) if King.user_book_id is None else ...#Выдаем
# db_session.commit() #Сохраняем изменения в БД


#Какие книги в библиотеке?
all_books = db_session.query(Library_Flask).filter(Library_Flask.user_book_id==None).all()


#Каких в библиотеке нет?

# not_books = [book.user_book_id for book in db_session.query(Library_Flask).all()]
not_books = db_session.query(Library_Flask).filter(Library_Flask.user_book_id==None).all()
# print(f'В библиотеке сейчас следущие книги:\n')
# for book in not_books:
#     print(book.title)
#Какие читатели взяли хотя бы одну книгу?



#добавить кингу в библиотеку
last_number = db_session.query(Library_Flask).order_by(Library_Flask.id.desc()).all()[0].personal_number
print(last_number)
# выше обратная сортировка таблицы(order_by(Library_Flask.id.desc())), вывод списка всех результатов, дальше индекс а потом атрибут

test_book = Library_Flask(title='title test',
                          author='title author',
                          year='title year',
                          is_checked_out=1,
                          personal_number = last_number + 1,
                          user_book_id = None) # создаем книгу
# db_session.add_all([test_book]) # добавляем в бд
# db_session.commit()# коммитим
counts = {

}
#пожсчет элементов в таблицу по элементу столбца "в данном случае по названию книги"
lines_title = db_session.query(func.count(Library_Flask.id).filter(Library_Flask.title == 'Джон Картер на Марсе')).scalar()

#порядковый номер последнего элемента
last_number = db_session.query(Library_Flask).order_by(Library_Flask.personal_number.desc()).first().personal_number

bookkk = db_session.query(Library_Flask).filter(Library_Flask.id==-1).first()
#выбор всех id и приведение их к нормальному виду
all_id = list(map(lambda id_book: str(list(id_book)[0]), db_session.query(Library_Flask.id).all()))


# books = db_session.query(Library_Flask).all()
#
# users = db_sessionquery(User_Flask).all()
# for i in users:
#     print(i)

