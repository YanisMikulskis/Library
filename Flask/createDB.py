import os

from sqlalchemy import create_engine, Column, Integer, String, Boolean, select, MetaData, ForeignKey
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship
from sqlalchemy import desc, func
from Book_for_flask import make_books
from faker import Faker
import sqlite3

import os

connect = sqlite3.connect('Library_Database_Flask')

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



