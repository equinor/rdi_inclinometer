#!/usr/bin/env python
from mmo.binoculars import Binoculars
from mmo.device.button import KeyboardButton
from mmo.device.fake import FakeGps, FakeSpatial
from mmo.storage import DatabaseStorage, CsvStorage

gps = FakeGps()
spatial = FakeSpatial()
storage = DatabaseStorage()
#CsvStorage("output_fake.csv")
button = KeyboardButton()


binoculars = Binoculars(button=button, gps=gps, spatial=spatial, storage=storage)

from mmo import web_server
web_server.start(binoculars=binoculars, debug=True)