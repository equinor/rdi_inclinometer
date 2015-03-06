import socket
import random
import string

from flask import Flask, make_response, request, render_template, send_file, redirect, flash

import mmo
from json_dumper import dump_as_json
from export import excel
from mmo.database import Database
from mmo.export.gpx import export_gpx


class Registry:
    def __init__(self):
        self.binoculars = None


registry = Registry()

app = Flask(__name__, static_url_path='', template_folder='templates')
app.secret_key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
app.config['hostname'] = socket.gethostname()


@app.route('/data.csv')
def dump_csv():
    text = registry.binoculars.storage.dump_csv()
    response = make_response(text, 200)
    response.headers['Content-type'] = "text/csv"
    return response


@app.route('/data.html')
def dump_table():
    rows = registry.binoculars.storage.dump_list()
    return render_template('dataTable.html', rows=rows)


@app.route('/data.xlsx')
def dump_excel():
    filename = excel.export(registry.binoculars.storage.dump_list())
    response = send_file(filename)
    return response


@app.route('/config.html', methods=['GET'])
def get_config():
    config = Database.get_config()
    return render_template('config.html', axisOptions=['A', 'B'], **config)


@app.route('/config.html', methods=['POST'])
def set_config():
    Database.set_config(request.form)
    flash("Config was updated")
    mmo.config.refresh()
    return redirect('/config.html')


@app.route('/observations')
def observations():
    return "Hello there"


@app.route('/data.json')
def dump_json():
    data_list = registry.binoculars.storage.dump_list()

    text = dump_as_json(data_list)
    print text
    response = make_response(text, 200)
    response.headers['Content-type'] = "application/json"
    return response


@app.route('/track.gpx')
def gpx_track():
    gpx = export_gpx(Database.get_positions())
    response = make_response(gpx, 200)
    response.headers['Content-type'] = "application/gpx+xml"
    return response


@app.route('/')
def index():
    return render_template('index.html', status=mmo.status)


def start(binoculars, **kwargs):
    registry.binoculars = binoculars
    app.run(host="0.0.0.0", **kwargs)

