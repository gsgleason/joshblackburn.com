import datetime
from sqlalchemy import create_engine, Column, String, Integer, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import config

Base = declarative_base()
engine = create_engine(config.db.uri, convert_unicode=True, pool_recycle=280)
session = scoped_session(sessionmaker(expire_on_commit=False, autocommit=False, autoflush=False, bind=engine))

class Event(Base):
	__tablename__ = 'event'
	id = Column(Integer, primary_key=True)
	title = Column(String(length=255))
	location = Column(String(length=255))
	start = Column(DateTime)
	end = Column(DateTime)
	all_day = Column(Boolean)

	def __repr__(self):
		return "<Event(id={}, title='{}', location='{}', start='{}', end='{}', all_day={})>".format(self.id, self.title, self.location, self.start, self.end, self.all_day)

class Contact(Base):
	__tablename__ = 'contact'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	email = Column(String)
	message = Column(String)
	ip = Column(String)
	utctime = Column(DateTime, default=datetime.datetime.utcnow)

	def __repr__(self):
		return "<Contact(id={}, name='{}', email='{}', message='{}', ip='{}', utctime='{}')>".format(self.id, self.name, self.email, self.message, self.ip, self.utctime)

def initDB():
	Base.metadata.drop_all(engine)
	Base.metadata.create_all(engine)
