from flask import Flask, make_response

from binoculars import Binoculars
from button import *
from storage import CsvStorage


button = Button.get_for_system()

csv_filename = "output.csv"

binoculars = Binoculars(button=button, store=CsvStorage(csv_filename))

app = Flask(__name__)


def read_csv():
    with open(csv_filename, "r") as f:
        return f.read()


@app.route('/data.csv')
def dump_csv():
    text = read_csv()
    response = make_response(text, 200)
    response.headers['Content-type'] = "text/csv"
    return response


if __name__ == '__main__':
    app.run()