from flask import Flask, make_response
from flask import send_file


class Registry:
    def __init__(self):
        self.binoculars = None

registry = Registry()

app = Flask(__name__)

@app.route('/data.csv')
def dump_csv():
    text = registry.binoculars.storage.dump_csv()
    response = make_response(text, 200)
    response.headers['Content-type'] = "text/csv"
    return response

@app.route('/data.html')
def dump_table():
    text = registry.binoculars.storage.dump_table()
    response = make_response(text, 200)
    response.headers['Content-type'] = "text/html"
    return response

@app.route('/')
def index():
    return send_file('html/index.html')



def start(binoculars, **kwargs):
    registry.binoculars = binoculars
    app.run(host="0.0.0.0", **kwargs)

