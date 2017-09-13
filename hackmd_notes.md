# Markdown Cheat Sheet

Formatowanie: **pogrubienie**

- lista
- lista

Kod źródłowy

```python
print(2)
```

# Recently Used List kata

```python
>>> rul = RecentlyUsedList()
>>> rul.insert('first')
>>> rul.insert('second')
>>> rul.insert('third')
>>> rul[0]  # rul.__getitem__(0)
'third'
>>> rul[1]
'second'
>>> rul[2]
'first'
>>> len(rul)  # rul.__len__()
3
>>> list(rul)  # wystarczy zaimplementowac __getitem__ i __len__
['third', 'second', 'first']
>>> rul.insert('second')
>>> list(rul)
['second', 'third', 'first']
```

Hint:

```python
class RecentlyUsedList:
    def __init__(self): ...
    def insert(self, item): ...
    def __getitem__(self, index): ...
    def __len__(self): ...
```

# Bank Account

- Napisać klasę reprezentującą konto bankowe.
- Konto bankowe ma identyfikator (`id`).
- Na koncie może znajdować się dowolna liczba środków lub może mieć debet (property `balance`) .
- Konto może znajdować się w jednym z dwóch stanów (property `state`): "normal" lub "overdraft".
- Na koncie można zdeponować środki (metoda `deposit`).
- Z konta można pobrać środki (metoda `withdraw`) jeśli tylko jest w stanie "normal", nawet jeśli nie ma na nim wystarczająco dużo środków. Jeżeli konto jest w stanie "overdraft", wówczas rzucony jest wyjątek `InsufficientFunds` zawierający informację o identyfikatorze konta.
- Na koncie naliczają się odsetki (metoda `pay_interest`). 10% od zgromadzonych środków. Jeśli konto jest w stanie "overdraft", wówczas naliczane są 20% odsetki.

# BDD - NBP Web app

## HTML

```HTML
<h1>Home Page</h1>
<p>1 USD = 3.5293 PLN</p>
<form method="POST">
  <p>Date: <input type="text" name="date" /></p>
  <p>Currency
    <select name="currency">
      <option value="USD">dolar amerykanski USD</option>
      <option value="THB">bat (Tajlandia) THB</option>
      <option value="ISK">korona islandzka ISK</option>
    </select>
  </p>
  <p><input type="submit" value="Get exchange rate!"></p>
</form>

```

## Parsowanie daty

```python
DATE_FORMAT = '%Y/%m/%d'
date = datetime.datetime.strptime(date_as_str, DATE_FORMAT).date()
```

## Parametryzowane kroki

```pyython
@then(u'{text} should be displayed')
def step_impl(context, text):
    assert text in context.resp
```

## *Sub*testy akceptacyjne

```
    Scenario Outline: Exchange rate form works
        Given I navigate to Home Page
          And I enter <date> as date
          And I enter <currency> as currency
         When I sent the form
         Then <expected output> should be displayed

    Examples:
      | date       | currency | expected output      |
      | 2017/02/03 | USD      | 1 USD = 4.0014 PLN   |
```

## `nbpapi.py`

```python
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
        
        return rate
```
