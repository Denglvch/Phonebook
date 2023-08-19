import unittest

from phonebook.data.data import PhoneBook


class TestData(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.path = '../../data/phone_book.csv'
        cls.phonebook_main = PhoneBook('../../data/phone_book.csv')

    def setUp(self) -> None:
        self.phonebook = PhoneBook(self.path)

    def tearDown(self) -> None:
        self.phonebook_main.save()

    def test_read(self):
        phonebook = self.phonebook
        self.assertTrue(phonebook.fb_headers)

    def test_write_and_save(self):
        test_row = ['1' for _ in self.phonebook.fb_headers]
        self.phonebook.write(test_row)
        self.assertIn(test_row, PhoneBook(self.path).fb_list)
