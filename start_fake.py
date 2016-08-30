#!/usr/bin/env python
from mmo.binoculars import Binoculars
from mmo.device.button import KeyboardButton
from mmo.device.fake import FakeSpatial
from mmo.device.fake import FakeGps
from mmo.storage import DatabaseStorage, CsvStorage, CombinationStorage

gps = FakeGps()
spatial = FakeSpatial()
storage = CombinationStorage(DatabaseStorage(), CsvStorage('output_fake.csv'))
button = KeyboardButton()


def say_nothing(text):
    pass

binoculars = Binoculars(button=button, gps=FakeGps(), spatial=spatial, storage=storage, say=say_nothing)

from mmo import web_server
web_server.start(binoculars=binoculars, debug=True, use_reloader=False)