from flask import Flask, make_response

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

def start(binoculars):
    registry.binoculars = binoculars
    app.run(host="0.0.0.0")

