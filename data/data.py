import csv


class PhoneBook:
    """
    Класс-предсталение для телефонной книги.
    При вызове создается экземпляр с актуальными данными.
    """

    def __init__(self, path: str = None) -> None:
        """
        Конструктор. Производит чтение файла телефонной книги
        и создает на новом экземпляре аттрибуты с заголовками и записями
        """

        if path:
            self.path = path
        else:
            self.path = 'data/phone_book.csv'

        with open(self.path) as fb_raw:
            self.fb_list = list(csv.reader(fb_raw))
            self.fb_headers = self.fb_list.pop(0)

    def write(self, record) -> None:
        """
        Метод для записи новых данных в файл телефонной книги.
        Записывает новые данные и вызывает метод сохранения.
        :param record: Данные для записи
        :return: None
        """
        record = list(record)
        self.fb_list.append(record)
        self.save()

    def save(self) -> None:
        """
        Метод сохранения изменений в файл. По умолчанию сортирует данные по полям:
        Фамилия, Имя, Отчество.
        Данные берутся из аттрибутов экземпляра.
        После сортировки файл телефонной книги перезаписывается новыми данными.
        :return: None
        """
        self.fb_list.sort(key=lambda row: [row[0], row[1], row[2]])
        updates_data = [self.fb_headers]
        updates_data.extend(self.fb_list)

        with open(self.path, 'w') as fb_raw:
            writer = csv.writer(fb_raw)
            for row in updates_data:
                writer.writerow(row)
