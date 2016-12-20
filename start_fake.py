#!/usr/bin/env python
from mmo.binoculars import Binoculars
from mmo.device.button import KeyboardButton
from mmo.device.fake import FakeSpatial
from mmo.device.fake import FakeGps
from mmo.storage import DatabaseStorage, CsvStorage, CombinationStorage
from mmo import web_server

gps = FakeGps()
spatial = FakeSpatial()
storage = CombinationStorage(DatabaseStorage(), CsvStorage('output_fake.csv'))
button = KeyboardButton()


def say_nothing(text):
    pass


binoculars = Binoculars(button=button, gps=FakeGps(),
                        spatial=spatial, storage=storage,
                        say=say_nothing,
                        on_long_click=web_server.long_click_handler,
                        on_short_click=web_server.short_click_handler)

web_server.prestart(binoculars)
#web_server.start(binoculars=binoculars, debug=True, use_reloader=False)
app = web_server.app
app.debug = True

if __name__ == "__main__":
    print("Starting fake server!")
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)

    try:
        server.serve_forever()
    except Exception as e:
        print("Got exception in web_server:start")
        print("Stopping fake spatial service..")
        binoculars.spatial.stop()
        print("Done!")

        print(e)
