#!/usr/bin/env python

import logging
from logging.handlers import RotatingFileHandler

import mmo
from mmo.binoculars import Binoculars
from mmo.device.button import KeyboardButton
from mmo.device.fake import FakeSpatial
from mmo.device.fake import FakeGps
from mmo.storage import DatabaseStorage, CsvStorage, CombinationStorage
from mmo import web_server

app = web_server.app
app.config.from_object("config.DevelopmentConfig")
logFormatter = logging.Formatter(app.config.get('LOG_FORMATTER', ''))

logfile = app.config.get('LOG_FILE', None)
handler = RotatingFileHandler(app.config.get('LOG_FILE', None), maxBytes=10000, backupCount=1)
handler.setLevel(logging.DEBUG)
handler.setFormatter(logFormatter)
app.logger.addHandler(handler)
mmo.logger = app.logger

gps = FakeGps()
spatial = FakeSpatial()
storage = CombinationStorage(DatabaseStorage(), CsvStorage('output_fake.csv'))
button = KeyboardButton()


def say_nothing(text):
    pass


binoculars = Binoculars(button=button, gps=gps,
                        spatial=spatial, storage=storage,
                        say=say_nothing,
                        on_long_click=web_server.long_click_handler,
                        on_short_click=web_server.short_click_handler)
web_server.prestart(binoculars)

if __name__ == "__main__":
    mmo.logger.info("=== Starting fake server! ===")
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)

    try:
        server.serve_forever()
    except Exception as e:
        mmo.logger.warn("Got exception in web_server:start")
        mmo.logger.warn("Stopping fake spatial service..")
        binoculars.spatial.stop()
        mmo.logger.warn("Done!")

        print(e)
