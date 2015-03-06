#!/usr/bin/env python

from mmo.binoculars import Binoculars
from mmo.device.button import Button
from mmo.device import Gps, Spatial
from mmo.storage import CsvStorage, DatabaseStorage, CombinationStorage


storage = CombinationStorage(DatabaseStorage(), CsvStorage('output_actual.csv'))
button = Button.get_for_system()

binoculars = Binoculars(button=button, gps=Gps(), spatial=Spatial(), storage=storage)

from mmo import web_server
web_server.start(binoculars,  debug=True, use_reloader=False)