from Library import Library

library = Library()
print(f'Добро пожаловать в онлайн библиотеку!')
commands = {
    1: lambda: library.add_book(),
    2: lambda: library.remove_book(),
    3: lambda: library.find_book(),
    4: lambda: library.register_user(),
    5: lambda: library.checkout_book(),
    6: lambda: library.return_book(),
    7: lambda: library.checkout_report(False),
    8: lambda: library.return_report(),
    9: lambda: library.general_report(),
    10: lambda: library.close()
}


def main() -> None:  # Функция запуска словаря лямбда функций с вызовами методов класса Library
    while 1:
        start_app = int(input('Что хотите сделать? Введите соответсвующую цифру!\n'
                              '1 - Добавить книгу в библиотеку\n'
                              '2 - Удалить книгу из библиотеки по ID\n'
                              '3 - Найти книгу в библиотеке по ID\n'
                              '4 - Зарегистрировать нового читателя\n'
                              '5 - Выдать читателю книгу\n'
                              '6 - Оформить возврата книги читателем\n'
                              '7 - Составить отчет о книгах на руках\n'
                              '8 - Составить отчет о книгах в библиотеке\n'
                              '9 - Составить общий отчет о состоянии библиотеки\n'
                              '10 - Выйти из программы\n'))
        if start_app in list(range(1, 11)):
            commands[start_app]()
        else:
            print(f'Нет такого номера команды!')
if __name__ == '__main__':
    main()