#!/usr/bin/env python
from Phidgets.Devices.GPS import GPS
from Phidgets.Devices.Spatial import Spatial

from mmo.binoculars import Binoculars
from mmo.device.button import Button
from mmo.storage import CsvStorage


gps = GPS()
spatial = Spatial()
storage = CsvStorage("output_fake.csv")
button = Button.get_for_system()

binoculars = Binoculars(button=button, gps=gps, spatial=spatial, storage=storage)

from mmo import web_server
web_server.start(binoculars)