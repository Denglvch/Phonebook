import sys

from phonebook.data.data import PhoneBook
from phonebook.data.models import RecordModelValidate, FieldError
from phonebook.app.table_view import Table
from phonebook.config import ConfigData


class Handlers:
    """
    Класс обработчик. Содержит в себе обработчики команд пользователя, и вспомогательные методы.
    """

    def __init__(self, handler_number: str) -> None:
        """
        Конструктор. Создает словарь обьектов методов класса,
        которые будут получены по ключу и вызваны после получения
        :param  handler_number: Номер команды для запуска обработчика
        """
        self.handlers_data: dict = {
            '1': self.show_records,
            '2': self.add_record,
            '3': self.search_record_for_edit,
            '4': self.search,
            '+': self.settings,
            '0': sys.exit
        }
        self.handlers_data[handler_number]()

    @staticmethod
    def settings() -> None:
        """
        Метод для изменения количества отображаемых записей на странице.
        Количество сохраняется до нового изменения.
        :return: None
        """
        data = ConfigData()
        print(f"Изменение количества записей для страницы."
              f"Текущее количество: {data.config_data.get('page_size')}")
        count = input('Сколько записей показывать на странице: ')
        while True:
            if count.isdigit() and int(count) > 1:
                ConfigData().write_config(count)
                break
            else:
                print('Должно быть цело положительно число')

    @staticmethod
    def search() -> None:
        """
        Метод-обработчик.
        Создает кейс поиска, запрашивает данные у пользователя и предоставляет ответ.
        :return: None
        """
        print('Для поиска записей можно вводить разные группы данных разделяя их пробелом.\n'
              'Поиск идет по полному или частичному совпадению с введенными данными.'
              'Пример: Иванов Петров Александрович 1234')
        search_data = input('Введите данные для поиска: ').lower()
        data = PhoneBook()
        patterns: str = '|'.join(
            [
                f'(?:{template})'
                for template
                in search_data.split()
            ]
        )
        table = Table.build(data.fb_headers, data.fb_list, patterns=patterns)
        if table.rows:
            print(f'Найдены записи:\n'
                  f'{table}')
            input('Для возврата в меню нажмите Enter')
        else:
            print('Записей с такими данными не найдено')

    @staticmethod
    def search_record_for_edit() -> None:
        """
        Метод-обработчик. Производит поиск записи по ее номеру
        и предоставляет интерфейс для редактирования или удаления записи
        :return: None
        """
        data = PhoneBook()
        while True:
            record_number = input("Введите номер записи для редактирования. Для выхода в меню введите '0': ")
            if record_number.isdigit() and int(record_number) > 0:
                record_number = int(record_number)
                if record_number >= len(data.fb_list):
                    print('Запись с таким номером не найдена')
                else:
                    print('Найдена запись')
                    break
            elif record_number == '0':
                return
            else:
                print('Номер записи - целое число больше 0')

        record = data.fb_list[record_number - 1]
        table = Table.build(data.fb_headers, record, num=record_number)
        print(table)
        while True:
            user_input = input("1 - Редактировать запись\n"
                               "2 - Удалить запись\n"
                               "Для выхода в меню введите '0'")
            if user_input in ('0', '1', '2'):
                if user_input == '1':
                    Handlers._edit_record(data, record, record_number, table)
                elif user_input == '2':
                    Handlers._delete_record(data, record_number)
                break
            print('Ошибка ввода')

    @staticmethod
    def _delete_record(data: PhoneBook, record_number: int):
        """
        Вспомогательный метод. Производит удаление записи из списка записей,
        а так же вызывает метод сохранения изменений
        :param data: Обьект справочника
        :param record_number: Номер записи для удаления
        :return: None
        """
        data.fb_list.pop(record_number - 1)
        data.save()
        print('Запись удалена\n')

    @staticmethod
    def _edit_record(data: PhoneBook, record: list, record_number: int, table: "PrettyTable") -> None:
        """
        Метод-обработчик. Создает кейс редактирования/удаления, запрашивает номер строки для редактирования,
        предоставляет интерфес редактирования/удаления записи.
        :return: None
        """
        print('Редактирование записи.\n'
              'Введите новые данные для нужного поля. Если поле изменять не нужно нажмите Enter без ввода данных.')

        old_record_form = {
            field: data
            for field, data
            in zip(RecordModelValidate().model_dump().keys(), record)
        }
        data = PhoneBook()
        new_form = Handlers._create_record(old_record_form, data)
        new_record = new_form.values()
        new_table = Table.build(data.fb_headers, new_record)
        print(f'Будет обновлена следующая запись:\n'
              f'{table}\n'
              f'{new_table}')
        check = input('Продолжить? (Y/N)')
        if check.lower() == 'n':
            print('Операция отменена')
            return
        data.fb_list[record_number - 1] = list(new_record)
        data.save()
        print('Запись успешно обновлена\n')

    @staticmethod
    def _create_record(form: dict, phonebook: PhoneBook) -> dict:
        """
        Вспомогательный метод. Запрашивает данные у пользователя, передает на валидацию,
        и возвращает заполненную форму
        :param form: Обьект формы для заполнения и передачи на валидацию
        :param phonebook: Обьект телефонной книги
        :return: form: Заполненная валидными данными форма
        """
        for verbose_field_name, table_field_name in zip(phonebook.fb_headers, form.keys()):
            while True:
                field_input = input(f"Введите данные для поля '{verbose_field_name}': ")
                if field_input:
                    form[table_field_name] = field_input
                    print('test', form)
                    try:
                        RecordModelValidate(**form)
                        break
                    except FieldError as ex:
                        print(ex)
                else:
                    break
        return form

    @staticmethod
    def add_record() -> None:
        """
        Метод-обработчик. Создает кейс добавления новой записи,
        использует вспомогательный метод для получения формы с валидными данными для новой записи,
        и передает эти данные на запись.
        :return: None
        """
        print('Создание новой записи')
        print('Чтобы зполнить поле введите данные и нажмите Enter')

        record_form = RecordModelValidate().model_dump()
        data = PhoneBook()
        new_form = Handlers._create_record(record_form, data)

        new_record = new_form.values()
        table = Table.build(data.fb_headers, new_record)
        print(f'Будет создана новая запись:\n'
              f'{table}')
        check = input('Продолжить? (Y/N)')
        if check.lower() == 'n':
            print('Операция отменена')
            return
        data.write(new_record)
        print('Новая запись успешно создана\n')

    @staticmethod
    def show_records() -> None:
        """
        Метод-обработчик. Создает кейс постраничного отображения всех имеющихся записей.
        :return: None
        """
        data = PhoneBook()
        config_data = ConfigData()
        page_size = config_data.config_data.get('page_size')
        pages = [
            data.fb_list[row_index + 1: page_size + row_index + 1]
            for row_index
            in range(-1, len(data.fb_list), page_size)
            if data.fb_list[row_index + 1: page_size + row_index + 1]
        ]
        current_page = 0
        record_number = 1

        while True:

            table = Table.build(data.fb_headers, pages[current_page], num=record_number)

            print(f'Стр. {current_page + 1}\n'
                  f'{table}\n'
                  f'Стр. {current_page + 1}\n')
            while True:
                user_input = input("Стр след/пред '+'/'-'. Вернуться в меню '0'")
                if user_input == '0':
                    return

                record_number, current_page, status = Handlers._pagination(
                    user_input,
                    current_page,
                    len(pages),
                    page_size,
                    record_number
                )
                if status:
                    break
                print('Ошибка ввода')

    @staticmethod
    def _pagination(
            user_input: str,
            current_page: int,
            pages_length: int,
            page_size: int,
            record_number: int,
    ) -> tuple[int, int, bool]:
        """
        Вспомогательный метод для перехода между страницами вывода.
        Производит проверку возможности перехода на новую страницу,
        и, если это возможно, обновляет данные для перехода.
        :param user_input: Флаг для переключения введенный пользователем
        :param current_page: Номер теккущей страницы
        :param pages_length: Общее количество страниц
        :param page_size: Количество записей на странице
        :param record_number: Номер первой записи на текущей странице
        :return: tuple: record_number: Содержит: Номер первой записи на следующей странице
                        current_page: Номер следующей страницы
                        status: Возвращает True при успешном вычислении след страницы
        """
        status = False
        if user_input == '+':
            if current_page + 1 < pages_length:
                current_page += 1
                record_number += page_size
            status = True

        elif user_input == '-':
            if current_page:
                current_page -= 1
                record_number -= page_size
            status = True
        return record_number, current_page, status
