import datetime

from flask import Flask, request

import nbpapi

app = Flask(__name__)

HOME_PAGE = """
<h1>Home Page</h1>
<p>{msg}</p>
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
"""
EXCHANGE_RATE_TEMPLATE = \
    '{cfactor} {currency} = {rate} PLN'
NO_DATA_MSG = 'No data for this day.'
DATE_FORMAT = '%Y/%m/%d'

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        date_as_str = request.form['date']
        date = datetime.datetime.strptime(date_as_str, DATE_FORMAT).date()
        currency = request.form['currency']

        try:
            rate, cfactor = nbpapi.get_exchange_rate(
                date=date, currency=currency)
        except nbpapi.NoData:
            msg = NO_DATA_MSG
        else:
            msg = EXCHANGE_RATE_TEMPLATE.format(
                cfactor=cfactor,
                currency=currency,
                rate=rate)
    else:
        msg = ''
    return HOME_PAGE.format(msg=msg)

if __name__ == "__main__":
    app.run()