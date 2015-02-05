import datetime
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import sessionmaker
from mmo.storage import Storage

Base = declarative_base()

engine = create_engine('sqlite:///database.db', echo=False)
Session = sessionmaker(bind=engine)

class Fix(Base):
    __tablename__ = 'fix'
    id = Column(Integer, primary_key=True, autoincrement=True)
    button = Column(String)
    system_time = Column(DateTime)
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


class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fix_id = Column(Integer, ForeignKey("fix.id"))
    text = Column(Text)


def create_tables():
    Base.metadata.create_all(engine)


create_tables()


class DatabaseStorage(Storage):
    def store(self, gps_fix, gyro, accelerometer_fix, compass_fix, typ):
        fix = Fix()

        fix.button = typ
        fix.system_time = datetime.datetime.now()

        fix.accelerometer0 = accelerometer_fix.a0
        fix.accelerometer1 = accelerometer_fix.a1
        fix.accelerometer2 = accelerometer_fix.a2
        fix.accelerometer_dip = accelerometer_fix.dip
        fix.accelerometer_dist = accelerometer_fix.dist
        fix.height = accelerometer_fix.height


        fix.gps_time = gps_fix.timestamp
        fix.latitude = gps_fix.latitude
        fix.longitude = gps_fix.longitude
        fix.altitude = gps_fix.altitude
        fix.heading = gps_fix.heading
        fix.velocity = gps_fix.velocity

        fix.compass0 = compass_fix.compass0
        fix.compass1 = compass_fix.compass1
        fix.compass2 = compass_fix.compass2

        fix.gyro0=gyro.gyro0
        fix.gyro1=gyro.gyro1
        fix.gyro2=gyro.gyro2

        session = Session()
        session.add(fix)
        session.commit()
        session.close()

    def dump_csv(self):
        import csv
        import io
        output = io.BytesIO()

        l=self.dump_list()
        keys = l[0].keys()
        keys.sort()
        writer = csv.DictWriter(output, fieldnames=keys)
        writer.writeheader()
        writer.writerows(l)
        return output.getvalue()

    def dump_list(self):
        session = Session()
        fixes = session.query(Fix)
        return [x.__dict__ for x in fixes.all()]