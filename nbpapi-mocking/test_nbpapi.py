import datetime
import unittest
from unittest import mock
import nbpapi
import io


EXAMPLE_DIR_TXT = b'''\xef\xbb\xbfc001z170102
h001z170102
a001z170102
c002z170103
h002z170103
a002z170103
c003z170104
'''

EXAMPLE_TABLE_LIST = [
    'c001z170102', 'h001z170102', 'a001z170102',
    'c002z170103', 'h002z170103', 'a002z170103',
    'c003z170104'
]

class GetTablesTests(unittest.TestCase):
    @mock.patch('nbpapi.request')
    def test_it(self, request_mock):
        request_mock.urlopen.return_value = io.BytesIO(EXAMPLE_DIR_TXT)
        # stream_mock = request_mock.urlopen.return_value
        # stream_mock.read.return_value = EXAMPLE_DIR_TXT

        got = nbpapi.get_tables()
        self.assertEqual(EXAMPLE_TABLE_LIST, got)
        request_mock.urlopen.assert_called_once_with('http://www.nbp.pl/kursy/xml/dir.txt')


@mock.patch('nbpapi.get_tables')
class GetTableNameTests(unittest.TestCase):
    def test_everything(self, get_tables_mock):
        for date, expected in [
            (datetime.date(2017, 1, 3), 'a002z170103'),
            (datetime.date(2017, 1, 4), None),
        ]:
            with self.subTest(date=date, expected=expected):
                get_tables_mock.return_value = EXAMPLE_TABLE_LIST
                got = nbpapi.get_table_name(date)
                self.assertEqual(got, expected)
                get_tables_mock.assert_called_with()
        self.assertEqual(get_tables_mock.call_count, 2)

    def test_should_return_valid_table_name(self, get_tables_mock):
        self._test_get_table_name(get_tables_mock,
            date=datetime.date(2017, 1, 3),
            expected='a002z170103')

    def test_should_return_None_for_missing_tables(self, get_tables_mock):
        self._test_get_table_name(get_tables_mock,
            date=datetime.date(2017, 1, 4),
            expected=None)        

    def _test_get_table_name(self, get_tables_mock, date, expected):
        get_tables_mock.return_value = EXAMPLE_TABLE_LIST
        got = nbpapi.get_table_name(date)
        self.assertEqual(got, expected)
        get_tables_mock.assert_called_once_with()        


if __name__ == '__main__':
    unittest.main()