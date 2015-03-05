from collections import OrderedDict
import datetime

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

engine = create_engine('sqlite:///database.db', echo=False)
Session = sessionmaker(bind=engine)


class Config(Base):
    __tablename__ = 'config'
    key = Column(String, primary_key=True)
    value = Column(String)

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def as_tuple(self):
        return self.key, self.value


class GpsTrack(Base):
    __tablename__ = "gps_track"
    gps_time = Column(DateTime)
    lat = Column(Float)
    lon = Column(Float)
    alt = Column(Float)

    def __init__(self, gps_time, lat, lon, alt):
        self.gps_time = gps_time
        self.lat = lat
        self.lon = lon
        self.alt = alt


class Observation(Base):
    __tablename__ = 'observation'
    hostname = Column(String)
    id = Column(Integer, primary_key=True, autoincrement=True)
    system_time = Column(DateTime)
    button = Column(String)
    c0 = Column(Float)
    c1 = Column(Float)
    c2 = Column(Float)
    g0 = Column(Float)
    g1 = Column(Float)
    g2 = Column(Float)
    a0 = Column(Float)
    a1 = Column(Float)
    a2 = Column(Float)
    a_dip = Column(Float)
    a_dist = Column(Float)
    height = Column(Float)
    gps_time = Column(DateTime)
    lat = Column(Float)
    lon = Column(Float)
    alt = Column(Float)
    hdg = Column(Float)
    vel = Column(Float)
    comments = Column(Text)

    def as_dict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            result[key] = getattr(self, key)
        return result


def create_tables():
    Base.metadata.create_all(engine)


create_tables()


class Database(object):
    @staticmethod
    def store_observation(host_name, gps_fix, gyro, accelerometer_fix, compass_fix, typ):
        obs = Observation()

        obs.hostname = host_name
        obs.button = typ
        obs.system_time = datetime.datetime.now()

        obs.a0 = accelerometer_fix.a0
        obs.a1 = accelerometer_fix.a1
        obs.a2 = accelerometer_fix.a2
        obs.a_dip = accelerometer_fix.dip
        obs.a_dist = accelerometer_fix.dist
        obs.height = accelerometer_fix.height

        obs.gps_time = gps_fix.timestamp
        obs.lat = gps_fix.latitude
        obs.lon = gps_fix.longitude
        obs.alt = gps_fix.altitude
        obs.hdg = gps_fix.heading
        obs.vel = gps_fix.velocity

        obs.c0 = compass_fix.compass0
        obs.c1 = compass_fix.compass1
        obs.c2 = compass_fix.compass2

        obs.g0 = gyro.gyro0
        obs.g1 = gyro.gyro1
        obs.g2 = gyro.gyro2

        session = Session()
        session.add(obs)
        session.commit()
        session.close()

    @staticmethod
    def store_position(gps_time, latitude, longitude, altitude):
        session = Session()
        track = GpsTrack(gps_time, latitude, longitude, altitude)
        session.add(track)
        session.commit()
        session.close()

    @staticmethod
    def dump_observations():
        session = Session()
        fixes = session.query(Observation)
        return [x.as_dict() for x in fixes.all()]

    @staticmethod
    def get_config():
        session = Session()
        configs = session.query(Config).all()
        # Initialize with default values
        d = {'height': '20', 'selectedAxis': 'A'}
        for config in configs:
            d[config.key] = config.value
        return d

    @staticmethod
    def set_config(form):
        session = Session()
        for key in form:
            session.merge(Config(key, form[key]))
        session.commit()
        session.close()