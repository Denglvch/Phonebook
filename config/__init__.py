class ConfigData:
    """
    Класс предоставляет доступ к файлу конфигурации справочника
    """
    def __init__(self):
        with open("config/config") as file:
            open_file = file.read().split('=')
            self.config_data = {open_file[0]: int(open_file[1])}

    @staticmethod
    def write_config(page_size: int | str) -> None:
        """
        Метод записывает в файл новую конфигурацию
        :param page_size: Количество записей на странице
        :return: None
        """
        with open("config/config", 'w') as file:
            line = f'page_size={page_size}'
            file.write(line)

