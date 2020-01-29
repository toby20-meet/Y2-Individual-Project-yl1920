from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Student(Base):
   __tablename__ = 'students'
   Id = Column(Integer, primary_key=True)
   name = Column(String)
   phone_number = Column(String)
   parent_phone_number = Column(String)

class Photo(Base):
	__tablename__ = 'Gallery'
	Id = Column(Integer, primary_key=True)
	photo_location = Column(String)