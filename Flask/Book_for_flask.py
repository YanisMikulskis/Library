from random import randint
import webbrowser
from bs4 import BeautifulSoup
import requests
import re


class Book:
    def __init__(self):
        self.book_data: list = None
        self.title: str = None
        self.author: str = None
        self.year: str = None


    def generic_data(self) -> None:
        url: str = "https://readly.ru/books/i_am_lucky/?show=1"
        request_html = requests.get(url)

        soup = BeautifulSoup(request_html.text, 'html.parser')
        self.title = re.findall(r'>(.+)</a>', str(soup.find_all(class_='blvi__title')))[0]
        self.title = self.title[:-1] if self.title[-1] == ' ' else self.title
        book_info = str(soup.find_all(class_='blvi__book_info'))
        self.author = re.findall(r'>([а-яА-Я ]+)<', book_info)[0]
        try:  # если поле года каким то образом оказалось пустым
            self.year = [i for i in book_info.split() if len(i) == 4 and i.isdigit()][0]
        except IndexError:
            self.year = 0
        self.book_data = [self.title, self.author, self.year]


def make_books(quantity):
    all_book_data = []
    book = Book()
    for i in range(quantity):
        book.generic_data()
        all_book_data.append(book.book_data)
    return all_book_data


make_books(1)
