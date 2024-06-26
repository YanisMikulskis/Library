# from selenium import webdriver
#
#
#
# driver = webdriver.Safari()
# driver.get('https://readly.ru/books/i_am_lucky/?show=1')
# element = driver.find_element_by_css_selector('<button class="btn-orange-big-20">Мне повезет</button>')
# element.click()


from random import randint
import webbrowser
from bs4 import BeautifulSoup
import requests
import re
# create webdriver object
# driver = webdriver.Safari()

# get lambdatest
# driver.get("https://readly.ru/books/i_am_lucky/?show=1")
# for i in range(3):
#     url = "https://readly.ru/books/i_am_lucky/?show=1"
#     webbrowser.open_new(url)
# url = "https://readly.ru/books/i_am_lucky/?show=1"
# for i in range(3):
#     request_html = requests.get(url)
#     soup = BeautifulSoup(request_html.text, 'html.parser')
#
#     name_book = re.findall(r'>(.+)</a>', str(soup.find_all(class_='blvi__title')))
#     author_book = re.search(r'>([а-яА-Я ]+)<', str(soup.find_all(class_='blvi__book_info')))
#     year_book = [i for i in book_info.split() if len(i) == 4 and i.isdigit()]

class Book:
    def __init__(self):
        self.title = None
        self.author = None
        self.year = None
        self.is_checked_out = None
        self.personal_number = None
    def generic_data(self):
        url = "https://readly.ru/books/i_am_lucky/?show=1"
        request_html = requests.get(url)
        soup = BeautifulSoup(request_html.text, 'html.parser')
        self.title = re.findall(r'>(.+)</a>', str(soup.find_all(class_='blvi__title')))[0]
        book_info =  str(soup.find_all(class_='blvi__book_info'))
        self.author = re.findall(r'>([а-яА-Я ]+)<', book_info)[0]
        try: #если поле года каким то образом оказалось пустым
            self.year = [i for i in book_info.split() if len(i) == 4 and i.isdigit()][0]
        except IndexError:
            self.year = 0000
        # self.personal_number = randint(10000, 99999)
        # self.all_data = [self.title, self.author, self.year, self.is_checked_out, self.personal_number]
        self.book_data = [self.title, self.author, self.year]
    def __str__(self):
        return (f'{self.title}\n'
                f'{self.author}\n'
                f'{self.year}\n'
                f'{self.is_checked_out}\n'
                f'{self.personal_number}')

def make_books(quantity):
    all_book_dates = []
    book = Book()
    for i in range(quantity):
        book.generic_data()
        print(book.book_data)
        all_book_dates.append(book.book_data)
    print(f'all book datessss {all_book_dates}')
    return all_book_dates