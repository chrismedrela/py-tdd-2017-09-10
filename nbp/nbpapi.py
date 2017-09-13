import datetime
from collections import namedtuple
import urllib.request

from xml.etree import ElementTree


class NoData(Exception):
    pass

ExchangeRate = namedtuple('ExchangeRate', 'rate cfactor')


API_ENDPOINT = 'http://www.nbp.pl/kursy/xml/{}'
TABLE_LIST_FILENAME = 'dir.txt'
TABLE_ENDPOINT = API_ENDPOINT + '.xml'
TABLE_TYPE = 'a'
DATE_FORMAT = '%y%m%d'
RATE_SELECTOR_PATTERN = './pozycja/[kod_waluty="{}"]/kurs_sredni'
CFACTOR_SELECTOR_PATTERN = './pozycja/[kod_waluty="{}"]/przelicznik'

def get_exchange_rate(currency, date):
    # getting list of tables 
    url = API_ENDPOINT.format(TABLE_LIST_FILENAME)
    tables = urllib.request.urlopen(url).read().decode('utf-8-sig').splitlines()

    date_as_str = date.strftime(DATE_FORMAT)

    try:
        # finding matching table
        table_name = next(
            name for name in tables
            if name.startswith(TABLE_TYPE)
            and name.endswith(date_as_str))
    except StopIteration:
        raise NoData
    else:
        table_url = TABLE_ENDPOINT.format(table_name)

        #download
        raw_xml = urllib.request.urlopen(table_url).read()

        # parsing
        xml = ElementTree.fromstring(raw_xml)

        rate_selector = RATE_SELECTOR_PATTERN.format(currency)
        rate_as_str = xml.find(rate_selector).text
        rate = float(rate_as_str.replace(',', '.'))

        cfactor_selector = CFACTOR_SELECTOR_PATTERN.format(currency)
        cfactor_as_str = xml.find(cfactor_selector).text
        cfactor = int(cfactor_as_str)
        
        return rate, cfactor
