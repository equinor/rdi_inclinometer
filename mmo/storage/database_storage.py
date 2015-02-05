import sqlite3


class DatabaseStorage:
    def __init__(self, file_path):
        conn = sqlite3.connect(file_path)
        conn.row_factory = sqlite3.Row


    def store(self, gps_fix, gyro, accelerometer_fix, compass_fix, typ):
        pass