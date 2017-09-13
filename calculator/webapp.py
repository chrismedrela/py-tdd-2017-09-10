from flask import Flask, request

import calc

app = Flask(__name__)

HOME_PAGE = '''
<h1>Home Page</h1>
<form method="POST">
<input name="first" /> +
<input name="second" /> =
<input type="submit" value="?" />
</form>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        first = int(request.form['first'])
        second = int(request.form['second'])
        sum = calc.add(first, second)
        return "{} + {} = {}".format(first, second, sum)
    else:
        return HOME_PAGE

if __name__ == "__main__":
    app.run()