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
                        spatial=spatial, storage=storage, say=say_nothing)

web_server.prestart(binoculars)
web_server.start(binoculars=binoculars, debug=True, use_reloader=False)
