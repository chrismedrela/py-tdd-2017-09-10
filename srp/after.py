import re
import unittest
from typing import Union


EMAIL_PATTERN = re.compile(r'^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$')


class Email:
    def __init__(self, email: Union['Email', str]):
        if isinstance(email, Email):
            raw_email = email._email
        else:
            raw_email = email

        if EMAIL_PATTERN.match(raw_email) is None:
            raise ValueError('Invalid email')        
        else:
            self._email = email


class Person:
    def __init__(self,
                 first_name: str,
                 last_name: str,
                 email: Union[Email, str]):
        self.first_name = first_name 
        self.last_name = last_name
        self.email = Email(email)


class PersonTests(unittest.TestCase):
    def test_valid_email(self):
        Person('Jan', 'Kowalski', 'jan@kowalski.pl')

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            Person('Jan', 'Kowalski', 'invalid email')


if __name__ == "__main__":
    unittest.main()
