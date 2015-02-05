from binoculars import Binoculars
from device.button import KeyboardButton
from device.fake import FakeGps, FakeSpatial
from storage import CsvStorage

gps = FakeGps()
spatial = FakeSpatial()
storage = CsvStorage("output_fake.csv")
button = KeyboardButton()


binoculars = Binoculars(button=button, gps=gps, spatial=spatial, storage=storage)

import web_server
web_server.start(binoculars)

