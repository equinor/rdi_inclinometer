#!/usr/bin/env python
from Phidgets.Devices.GPS import GPS
from Phidgets.Devices.Spatial import Spatial

from mmo.binoculars import Binoculars
from mmo.device.button import Button
from mmo.storage import CsvStorage, DatabaseStorage, CombinationStorage


gps = GPS()
spatial = Spatial()
storage = CombinationStorage(CsvStorage('output_fake.csv'), DatabaseStorage())
button = Button.get_for_system()

binoculars = Binoculars(button=button, gps=gps, spatial=spatial, storage=storage)

from mmo import web_server
web_server.start(binoculars)