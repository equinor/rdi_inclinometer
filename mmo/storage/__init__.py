from abc import abstractmethod


class Storage:
    """
    Handles storing measurements from sensors
    """
    @abstractmethod
    def store(self, gps_fix, gyro, accelerometer_fix, compass_fix, typ):
        """
        :type compass_fix: mmo.device.CompassFix
        :type gps_fix: mmo.device.GpsFix
        :type gyro: mmo.device.Gyro
        :type accelerometer_fix: mmo.device.AccelerometerFix
        """
        pass

    @abstractmethod
    def dump_list(self):
        pass

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
        keys=l[0].keys()
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