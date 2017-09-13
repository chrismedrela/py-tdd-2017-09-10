# -*- encoding: utf-8 -*-

import datetime

from mock import patch, Mock
from nose2.tools import such

from nbpapi import get_exchange_rate, NoData

with such.A('NBP API') as it:
    with it.having('get_exchange_rate function'):
        DIR_TXT = "a011z170117".encode('utf-8-sig')
        DIR_TXT_URL = 'http://www.nbp.pl/kursy/xml/dir.txt'
        A011Z170117_XML = '''
<tabela_kursow typ="A" uid="17a011">
<numer_tabeli>011/A/NBP/2017</numer_tabeli>
<data_publikacji>2017-01-17</data_publikacji>
<pozycja>
<nazwa_waluty>bat (Tajlandia)</nazwa_waluty>
<przelicznik>1</przelicznik>
<kod_waluty>THB</kod_waluty>
<kurs_sredni>0,1161</kurs_sredni>
</pozycja>
<pozycja>
<nazwa_waluty>dolar amerykański</nazwa_waluty>
<przelicznik>1234</przelicznik>
<kod_waluty>USD</kod_waluty>
<kurs_sredni>4,0989</kurs_sredni>
</pozycja>
</tabela_kursow>
        '''.encode('utf-8-sig')
        A011Z170117_XML_URL = 'http://www.nbp.pl/kursy/xml/a011z170117.xml'

        def urlopen_mock(url):
            m = Mock()
            url2data = {
                DIR_TXT_URL: DIR_TXT,
                A011Z170117_XML_URL: A011Z170117_XML,
            }
            m.read.return_value = url2data[url]
            return m

        with it.having('a working day'):
            @it.has_setup
            @patch('nbpapi.urllib')
            @patch('nbpapi.datetime')
            def setup(datetime_mock, urllib_mock):
                datetime_mock.datetime.now.return_value = datetime.datetime(2017, 1, 28)
                urllib_mock.request.urlopen.side_effect = urlopen_mock
                it.datetime_mock = datetime_mock
                it.urllib_mock = urllib_mock

                it.retval = get_exchange_rate(
                    currency='USD',
                    date=datetime.date(2017, 1, 17))

            @it.should('request tables list from NBP API')
            def test():
                it.urllib_mock.request.urlopen.assert_any_call(
                    DIR_TXT_URL)

            @it.should('request right table from NBP API')
            def test():
                it.urllib_mock.request.urlopen.assert_any_call(
                    A011Z170117_XML_URL)

            @it.should('return exchange rate and cfactor')
            def test():
                it.assertIsInstance(it.retval, tuple)
                it.assertIsInstance(it.retval[0], float)
                it.assertIsInstance(it.retval[1], int)

            @it.should('return correct exchange rate')
            def test():
                it.assertEqual(it.retval[0], 4.0989)

            @it.should('return correct cfactor')
            def test():
                it.assertEqual(it.retval[1], 1234)

        with it.having('a non-working day'):
            @it.should('raise NoData')
            @patch('nbpapi.urllib')
            @patch('nbpapi.datetime')
            def test(datetime_mock, urllib_mock):
                datetime_mock.datetime.now.return_value = datetime.datetime(2017, 1, 28)
                urllib_mock.request.urlopen.side_effect = urlopen_mock
                it.datetime_mock = datetime_mock
                it.urllib_mock = urllib_mock

                with it.assertRaises(NoData):
                    get_exchange_rate(
                        currency='USD',
                        date=datetime.date(2017, 1, 18))

    it.createTests(globals())