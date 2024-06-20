from Book import Book
from User import User
class Library:
    def __init__(self):
        pass
    def add_book(self, book:Book):
        ...
    def remove_book(self, book_id: int):
        ...
    def find_book(sel, book_id: int):
        ...
    def register_book(self, user):
        ...
    def checkout_book(self, book_id, user_id):
        ...
    def return_book(self, book_id, user_id):
        ...
    def generate_report(self)::
    ...

add_book(book: Book) - добавление книги.
remove_book(book_id: int) - удаление книги по ID.
find_book(book_id: int) - поиск книги по ID.
register_user(user: User) - регистрация пользователя.
checkout_book(book_id: int, user_id: int) - выдача книги пользователю.
return_book(book_id: int, user_id: int) - возврат книги пользователем.

