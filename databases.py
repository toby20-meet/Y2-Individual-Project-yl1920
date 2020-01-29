from model import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def run_them():
	engine = create_engine('sqlite:///database.db')
	Base.metadata.create_all(engine)
	DBSession = sessionmaker(bind=engine)
	session = DBSession()
	return session

def addStudent(student_name,phone_number,parent_phone_number):
	session = run_them()
	new_student = Student(name = student_name,phone_number = phone_number,parent_phone_number=parent_phone_number)
	session.add(new_student)
	session.commit()

def delStudent(student_id):
	session = run_them()
	student_object = session.query(Student).filter_by(Id = student_id).first()
	session.delete(student_object)
	session.commit()

def delPhoto(photo_id):
	session = run_them()
	photo_object = session.query(Photo).filter_by(Id = photo_id).first()
	session.delete(photo_object)
	session.commit()

def allStudents():
	session = run_them()
	return session.query(Student).all()

def bringStudent(student_id):
	session = run_them()
	return session.query(Student).filter_by(Id = student_id).first()

def editStudent(student_id,change_var,new_vlaue):
	session = run_them()
	student_object = session.query(Student).filter_by(Id = student_id).first()
	setattr(student_object,change_var,new_vlaue)
	session.commit()

def addPhoto(photo_location):
	session = run_them()
	new_photo = Photo(photo_location = photo_location)
	session.add(new_photo)
	session.commit()

def all_photos():
	session = run_them()
	return session.query(Photo).all()

