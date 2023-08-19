import re
from typing import Iterable

from prettytable import PrettyTable


class Table:
    """
    Класс описывающий табличное представление данных.
    Содержит методы для построения таблицы и фильтрации записей для таблицы.
    """
    template_headers = ['#']

    @classmethod
    def build(cls, headers: list, records: Iterable, **kwargs) -> PrettyTable:
        """
        Метод для построения новой таблицы на основании переданных заголовков и строк данных.
        :param headers: Заголовки для новой таблицы
        :param records: Записи для новой таблицы
        :param kwargs: Дополнительный аргументы которые могут быть переданы для корректировки работы методов.
        :return: PrettyTable: Обьект таблицы
        """
        if not isinstance(records, list):
            records = list(records)
        if not isinstance(records[0], list):
            records = [records]

        cls.template_headers.extend(headers)
        table = PrettyTable(cls.template_headers)

        for num, row in enumerate(records, kwargs.get('num', 1)):

            if kwargs.get('patterns'):
                if not cls.row_filter(row, kwargs.get('patterns')):
                    continue
            template_row = [num]
            template_row.extend(row)
            table.add_row(template_row)

        cls.template_headers = ['#']

        return table

    @classmethod
    def row_filter(cls, row: list, patterns: str) -> bool:
        """
        Метод применяет переданный паттерн к переданной записи и возвращает результат.
        :param row: Список данных для новой строки таблицы.
        :param patterns: Шаблон для фильтра.
        :return: bool
        """
        row = str(row).lower()
        if re.findall(r'{}'.format(patterns), row):
            return True



