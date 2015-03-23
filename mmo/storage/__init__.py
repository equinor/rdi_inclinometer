from abc import abstractmethod


class Storage(object):
    """
    Handles storing measurements from sensors
    """

    def __init__(self):
        pass

    @abstractmethod
    def store(self, host_name, gps_fix, gyro, accelerometer_fix, compass_fix, roll_pitch_yaw, typ):
        """
        :type host_name: str
        :type compass_fix: mmo.device.output.CompassFix
        :type typ: str
        :type accelerometer_fix: mmo.device.output.AccelerometerFix
        :type gyro: mmo.device.Gyro
        :type roll_pitch_yaw: mmo.device.output.RollPitchYaw
        :type gps_fix: mmo.device.GpsFix
        """
        pass

    @abstractmethod
    def dump_list(self, limit=1000000):
        return []

    def dump_csv(self):
        import csv
        import io

        output = io.BytesIO()

        l = self.dump_list()
        keys = l[0].keys()
        keys.sort()
        writer = csv.DictWriter(output, fieldnames=keys)
        writer.writeheader()
        writer.writerows(l)
        return output.getvalue()

    def dump_table(self):
        l = self.dump_list()
        keys = l[0].keys()
        keys.sort()

        ret = "<table><thead><tr>"
        for key in keys:
            ret += "<th>{}</th>".format(key)
        ret += "</tr></thead><tbody>"
        for row in l:
            ret += "<tr>"
            for key in keys:
                ret += "<td>{}</td>".format(row[key])
            ret += "</tr>"
        ret += "</tbody></table>"
        return ret

from csv_storage import CsvStorage
from database_storage import DatabaseStorage
from combination_storage import CombinationStorage