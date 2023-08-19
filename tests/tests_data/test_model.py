import unittest

from phonebook.data.models import RecordModelValidate, FieldError


class TestModel(unittest.TestCase):
    def setUp(self) -> None:
        self.model = RecordModelValidate()

    def test_valid_data(self):
        valid_data = ['Петров', 'Петр', 'Петрович', "ООО""АБЫ""", '123456', '+79998887765']
        form = self.model.model_dump()
        for key, data in zip(form.keys(), valid_data):
            form[key] = data
            with self.subTest():
                rec = RecordModelValidate(**form)
                self.assertEqual(rec.model_dump()[key], data)

    def test_invalid_data(self):
        invalid_data = ['1', '2', '3', "ООО""АБЫ""", 'ab', '+79998']
        form = self.model.model_dump()
        for key, data in zip(form.keys(), invalid_data):
            form[key] = data
            with self.subTest():
                try:
                    RecordModelValidate(**form)
                    self.assertRaises(FieldError)
                except FieldError:
                    pass
