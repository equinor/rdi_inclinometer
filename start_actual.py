#!/usr/bin/env python

from mmo.binoculars import Binoculars
from mmo.device.button import Button
from mmo.device import Gps, Spatial
from mmo.device.tts import Voice
from mmo.storage import CsvStorage, DatabaseStorage, CombinationStorage


storage = CombinationStorage(DatabaseStorage(), CsvStorage('output_actual.csv'))
button = Button.get_for_system()
voice = Voice()
say = voice.say


def say_nothing(text):
   pass

binoculars = Binoculars(button=button, gps=Gps(), spatial=Spatial(), storage=storage, say=say)

from mmo import web_server
web_server.prestart(binoculars)
app = web_server.app

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, use_reloader=False, port=5000)
