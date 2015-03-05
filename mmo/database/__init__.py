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


class Observation(Base):
    __tablename__ = 'observation'
    hostname = Column(String)
    id = Column(Integer, primary_key=True, autoincrement=True)
    system_time = Column(DateTime)
    button = Column(String)
    compass0 = Column(Float)
    compass1 = Column(Float)
    compass2 = Column(Float)
    gyro0 = Column(Float)
    gyro1 = Column(Float)
    gyro2 = Column(Float)
    accelerometer0 = Column(Float)
    accelerometer1 = Column(Float)
    accelerometer2 = Column(Float)
    accelerometer_dip = Column(Float)
    accelerometer_dist = Column(Float)
    height = Column(Float)
    gps_time = Column(DateTime)
    latitude = Column(Float)
    longitude = Column(Float)
    altitude = Column(Float)
    heading = Column(Float)
    velocity = Column(Float)
    comments = Column(Text)

    def as_dict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            result[key] = getattr(self, key)
        return result


def create_tables():
    Base.metadata.create_all(engine)


create_tables()


class Database:
    @staticmethod
    def store_observation(host_name, gps_fix, gyro, accelerometer_fix, compass_fix, typ):
        obs = Observation()

        obs.hostname = host_name
        obs.button = typ
        obs.system_time = datetime.datetime.now()

        obs.accelerometer0 = accelerometer_fix.a0
        obs.accelerometer1 = accelerometer_fix.a1
        obs.accelerometer2 = accelerometer_fix.a2
        obs.accelerometer_dip = accelerometer_fix.dip
        obs.accelerometer_dist = accelerometer_fix.dist
        obs.height = accelerometer_fix.height

        obs.gps_time = gps_fix.timestamp
        obs.latitude = gps_fix.latitude
        obs.longitude = gps_fix.longitude
        obs.altitude = gps_fix.altitude
        obs.heading = gps_fix.heading
        obs.velocity = gps_fix.velocity

        obs.compass0 = compass_fix.compass0
        obs.compass1 = compass_fix.compass1
        obs.compass2 = compass_fix.compass2

        obs.gyro0 = gyro.gyro0
        obs.gyro1 = gyro.gyro1
        obs.gyro2 = gyro.gyro2

        session = Session()
        session.add(obs)
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