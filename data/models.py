import re

from pydantic import BaseModel, Field, field_validator


class FieldError(BaseException):
    """
    Кастомный класс исключений
    """
    pass


class RecordModelValidate(BaseModel):
    """
    Класс описывает модель данных для валидации.
    Если поле не валидно, вызывается исключение.
    После заполнения валидными данными,
    с класса можно получить форму с именами полей и валидными данными для записи в эти поля.
    """
    first_name: str = Field(default="-")
    last_name: str = Field(default="-")
    surname: str = Field(default="-")
    company_name: str = Field(default="-", validate_default=True)
    work_phone: str = Field(default="-")
    privacy_phone: str = Field(default="-")


    @field_validator("first_name")
    @classmethod
    def validate_first_name(cls, value) -> str:
        if value.isalpha() or value == '-':
            return value
        raise FieldError("В поле 'Фамилия' должны быть только буквы")

    @field_validator("last_name")
    @classmethod
    def validate_last_name(cls, value) -> str:
        if value.isalpha() or value == '-':
            return value
        raise FieldError("В поле 'Имя' должны быть только буквы")

    @field_validator("surname")
    @classmethod
    def validate_surname(cls, value) -> str:
        if value.isalpha() or value == '-':
            return value
        raise FieldError("В поле 'Отчество' должны быть только буквы")

    @field_validator("work_phone")
    @classmethod
    def validate_work_phone(cls, value: str) -> str:
        if re.fullmatch(r'^\d*', value) or value == '-':
            return value
        raise FieldError("В поле 'Телефон рабочий' должны быть только цифры")


    @field_validator("privacy_phone")
    @classmethod
    def validate_privacy_phone(cls, value) -> str:
        if re.fullmatch(r'^[\+7]?[\d]{11}\b', value) or value == '-':
            return value
        raise FieldError("В поле 'Телефон личный (сотовый)' должны быть номер в формате: +79998887766")


# try:
#     x = RecordModelValidate(
#         **{"first_name": "-", "last_name": "-", "surname": "-", "company_name": "ООО'АБВ'", "work_phone": "-",
#          "privacy_phone": "-"}
#         # first_name='f',
#         # last_name='r',
#         # # surname=,
#         # # company_name=,
# #         work_phone='123',
#         # privacy_phone='+7978584857',
#     )
#     print(x.model_dump().values())
#
# # print(x)
# except FieldError as ex:
#     print(ex)
#     # pass
# x = RecordModelValidate()
# print(x.model_dump())
