from .extensions import db 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(75))       # Name of the user
    email = db.Column(db.String(150))     # Email of the user
    password = db.Column(db.String(150))  # Password of the user
    role = db.Column(db.String(50))       # Role of the user (admin, normal user, etc.)
    index_number = db.Column(db.Integer)  # Index number of the user
    fingerprintID = db.Column(db.Integer) # Fingerprint ID of the user

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index_number = db.Column(db.Integer)   # Index number of the user
    attended = db.Column(db.Boolean)       # Whether the user attended (True/False)
    time = db.Column(db.DateTime)          # Timestamp of the data
    course_name = db.Column(db.String)

""""
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://kleb_backend_user:v4MSlxy6gCuZHgNq3hHZXBaPf31pU2B9@dpg-cj4hdltgkuvsl0ccaatg-a.oregon-postgres.render.com/kleb_backend"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(75))       # Name of the user
    email = Column(String(150))     # Email of the user
    password = Column(String(150))  # Password of the user
    role = Column(String(50))       # Role of the user (admin, normal user, etc.)
    index_number = Column(Integer)  # Index number of the user
    fingerprintID = Column(Integer) # Fingerprint ID of the user

class Attendance(Base):
    __tablename__ = 'attendance'
    id = Column(Integer, primary_key=True)
    index_number = Column(Integer)   # Index number of the user
    attended = Column(Boolean)       # Whether the user attended (True/False)
    time = Column(DateTime)          # Timestamp of the data

Base.metadata.create_all(engine)
"""
