import os

from sqlalchemy import create_engine, Column, Integer, String,Boolean, select, MetaData, ForeignKey
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship
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
book_test = db_session.query(Library_Flask).filter(Library_Flask.id==78).first()
user_test = db_session.query(User_Flask).filter(User_Flask.id==6).first()

user_have_books = db_session.query(User_Flask).filter(User_Flask.name=='Виктория').first().name
print(user_have_books)



book_test.users=user_test
db_session.commit()



# books = db_session.query(Library_Flask).all()
#
# users = db_sessionquery(User_Flask).all()
# for i in users:
#     print(i)

