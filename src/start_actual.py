from Phidgets.Devices.GPS import GPS
from Phidgets.Devices.Spatial import Spatial

from binoculars import Binoculars
from device.button import Button
from storage import CsvStorage


gps = GPS()
spatial = Spatial()
storage = CsvStorage("output_fake.csv")
button = Button.get_for_system()

binoculars = Binoculars(button=button, gps=gps, spatial=spatial, storage=storage)

import web_server
web_server.start(binoculars)