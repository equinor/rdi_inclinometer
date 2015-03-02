from flask import Flask, make_response
from flask import send_file
from json_dumper import dump_as_json
from export import excel


class Registry:
    def __init__(self):
        self.binoculars = None

registry = Registry()

app = Flask(__name__, static_url_path='')

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

@app.route('/data.xlsx')
def dump_excel():
    filename = excel.export(registry.binoculars.storage.dump_list())
    response = send_file(filename)
    return response



@app.route('/data.json')
def dump_json():
    data_list = registry.binoculars.storage.dump_list()

    text = dump_as_json(data_list)
    print text
    response = make_response(text, 200)
    response.headers['Content-type'] = "application/json"
    return response

@app.route('/')
def index():
    return app.send_static_file('index.html')



def start(binoculars, **kwargs):
    registry.binoculars = binoculars
    app.run(host="0.0.0.0", **kwargs)

