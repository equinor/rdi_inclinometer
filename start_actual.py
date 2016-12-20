#!/usr/bin/env python

from mmo.binoculars import Binoculars
from mmo.device.button import Button
from mmo.device.gps import Gps
from mmo.device.spatial import Spatial
from mmo.device.tts import Voice
from mmo.storage import CsvStorage, DatabaseStorage, CombinationStorage
from mmo import web_server


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
app = web_server.app
app.use_reloader = False
app.debug = True

if __name__ == "__main__":
    #app.run(host="0.0.0.0", debug=True, use_reloader=False, port=5000)
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)

    try:
        server.serve_forever()
    except Exception as e:
        print("Stopping fake spatial service..")
        binoculars.spatial.stop()
        print("Done!")
        print(e)
