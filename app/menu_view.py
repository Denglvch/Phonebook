from phonebook.app.handlers import Handlers


class MainMenuView:
    """
        Данный класс создает представление главного меню,
        а так же запускает обработчик ввода пользователя

        attrs: options_data - Доступные для обработки команды
    """
    options_data = {
        '1': 'Показать записи',
        '2': 'Добавить новую запись',
        '3': 'Редактировать существующую запись',
        '4': 'Поиск записей',
        '+': 'Настройки',
        '0': 'Выход из программы'
    }

    def run(self):
        """
        Метод ждет ответ от options и передает его на обработчики
        :return: None
        """
        while True:
            action_num = self.options()
            Handlers(action_num)

    def options(self) -> str:
        """
        Метод создает представление главного меню для пользователя,
        принимет ввод пользователя и возвращает его.
        :return: str - Ввод пользователя.
        """

        while True:
            print('\nДействия:')
            for num, action in self.options_data.items():
                print(f'{num} - {action}')

            target = input('\nВведите номер действия: ')
            if target in self.options_data.keys():
                return target
            print(f'Ошибка ввода. Ввод должен содержать только одно из {tuple(self.options_data.keys())}\n')

