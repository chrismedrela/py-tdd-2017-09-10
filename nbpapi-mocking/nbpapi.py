from urllib import request


API_ENDPOINT = 'http://www.nbp.pl/kursy/xml/'
TABLE_LIST_ENDPOINT = API_ENDPOINT + 'dir.txt'
DATE_FORMAT = '%y%m%d'
TABLE_NAME_PREFIX = 'a'


def get_tables():
    stream = request.urlopen(TABLE_LIST_ENDPOINT)
    bytes = stream.read()
    text = bytes.decode('utf-8-sig')
    tables = text.splitlines()
    return tables


def get_table_name(date):
    tables = get_tables()
    try:
        return next(
            table_name for table_name in tables
            if is_right_table(table_name, date))
    except StopIteration:
        return None

    # for table_name in tables:
    #     if is_right_table(table_name, date):
    #         return table_name
    # return None


def is_right_table(table_name, date):
    right_prefix = table_name.startswith(TABLE_NAME_PREFIX)
    date_as_str = date.strftime(DATE_FORMAT)
    right_date = table_name.endswith(date_as_str)
    return right_prefix and right_date
