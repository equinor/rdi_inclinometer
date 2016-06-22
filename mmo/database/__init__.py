from collections import OrderedDict
import datetime

from mmo.distance_calculator import calculate_distance
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import sessionmaker
import mmo

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
    gps_time = Column(DateTime, primary_key=True)
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
    gm0 = Column(Float)
    gm1 = Column(Float)
    gm2 = Column(Float)
    a0 = Column(Float)
    a1 = Column(Float)
    a2 = Column(Float)
    axis = Column(String(length=1))
    height = Column(Float)
    gps_time = Column(DateTime)
    lat = Column(Float)
    lon = Column(Float)
    alt = Column(Float)
    hdg = Column(Float)
    vel = Column(Float)
    roll = Column(Float)
    pitch = Column(Float)
    yaw = Column(Float)
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
    def store_observation(host_name, gps_fix, gyro, gyro_momentary, accelerometer_fix, compass_fix, roll_pitch_yaw, typ):
        obs = Observation()

        obs.hostname = host_name
        obs.button = typ
        obs.system_time = datetime.datetime.utcnow()

        obs.a0 = accelerometer_fix.a0
        obs.a1 = accelerometer_fix.a1
        obs.a2 = accelerometer_fix.a2
        obs.height = mmo.config.height
        obs.axis = mmo.config.axis_translator.name

        obs.gps_time = gps_fix.timestamp
        obs.lat = gps_fix.latitude
        obs.lon = gps_fix.longitude
        obs.alt = gps_fix.altitude
        obs.hdg = gps_fix.heading
        obs.vel = gps_fix.velocity

        obs.c0 = compass_fix.compass0
        obs.c1 = compass_fix.compass1
        obs.c2 = compass_fix.compass2

        obs.roll = roll_pitch_yaw.roll
        obs.pitch = roll_pitch_yaw.pitch
        obs.yaw = roll_pitch_yaw.yaw

        obs.g0 = gyro.gyro0
        obs.g1 = gyro.gyro1
        obs.g2 = gyro.gyro2

        obs.gm0 = gyro_momentary['gm0']
        obs.gm1 = gyro_momentary['gm1']
        obs.gm2 = gyro_momentary['gm2']

        session = Session()
        session.add(obs)
        session.commit()
        session.close()
        return obs.id

    @staticmethod
    def store_position(gps_time, latitude, longitude, altitude):
        session = Session()
        track = GpsTrack(gps_time, latitude, longitude, altitude)
        session.add(track)
        session.commit()
        session.close()

    @staticmethod
    def get_positions():
        session = Session()
        return session.query(GpsTrack).all()

    @staticmethod
    def dump_observations(limit=1000000, page=1):
        session = Session()
        fixes = session.query(Observation).order_by(Observation.id.desc()).offset(limit * (page - 1)).limit(limit)
        dicts = [x.as_dict() for x in fixes]

        rev_dicts = reversed(dicts)
        last_ref_pitch = None
        for observation in rev_dicts:
            observation['rpitch'] = None
            observation['distance'] = None
            if observation['pitch'] is None:
                continue
            if observation['button'] == 'long':
                last_ref_pitch = observation['pitch']
                observation['rpitch'] = 0.0
                observation['distance'] = calculate_distance(height_m=observation['height'],
                                                             degrees_below_horizon=0)
            else:
                if last_ref_pitch is None:
                    observation['rpitch'] = None
                else:
                    observation['rpitch'] = last_ref_pitch - observation['pitch']
                    observation['distance'] = calculate_distance(height_m=observation['height'],
                                                                 degrees_below_horizon=observation['rpitch'])

        return dicts

    @staticmethod
    def get_config():
        session = Session()
        configs = session.query(Config).all()
        # Initialize with default values
        d = {'height': '20',
             'selectedAxis': 'A',
             'samplingRate': '200',
             'averageSampleCount': '1',
             'observationsToShowOnMainPage': '25',
             'sampleSpeak': '1'}
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

    @staticmethod
    def store_comment(observation_id, comment):
        session = Session()
        obs = session.query(Observation).get(observation_id)
        obs.comments = comment
        session.commit()
        session.close()

    @staticmethod
    def get_num_observations():
        session = Session()
        result = session.query(Observation).count()
        session.close()
        return result