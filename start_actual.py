#!/usr/bin/env python

import logging
from logging.handlers import RotatingFileHandler

import mmo
from mmo.binoculars import Binoculars
from mmo.device.button import Button
from mmo.device.gps import Gps
from mmo.device.spatial import Spatial
from mmo.device.tts import Voice
from mmo.storage import CsvStorage, DatabaseStorage, CombinationStorage
from mmo import web_server

app = web_server.app
app.use_reloader = False
app.config.from_object("config.ProductionConfig")
logFormatter = logging.Formatter(app.config.get('LOG_FORMATTER', ''))

logfile = app.config.get('LOG_FILE', None)
handler = RotatingFileHandler(app.config.get('LOG_FILE', None), maxBytes=10000, backupCount=10)
handler.setLevel(logging.INFO)
handler.setFormatter(logFormatter)
app.logger.addHandler(handler)
mmo.logger = app.logger


storage = CombinationStorage(DatabaseStorage(), CsvStorage('output_actual.csv'))
button = Button.get_for_system()
voice = Voice()
say = voice.say


def say_nothing(text):
    pass


binoculars = Binoculars(button=button,
                        gps=Gps(),
                        spatial=Spatial(),
                        storage=storage,
                        say=say,
                        on_long_click=web_server.long_click_handler,
                        on_short_click=web_server.short_click_handler)
web_server.prestart(binoculars)

if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)

    try:
        server.serve_forever()
    except Exception as e:
        mmo.logger.warn("Stopping fake spatial service..")
        binoculars.spatial.stop()
        mmo.logger.warn("Done!")
        mmo.logger.warn(e)
