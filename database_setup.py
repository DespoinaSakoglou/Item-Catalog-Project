import os
# sys module provides functions and variables
# that are used to manipulate different parts
# of the python runtime environment
import sys
# classes used for mapper code
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
# declarative_base used in configuration and class code
from sqlalchemy.ext.declarative import declarative_base
# relationship class used to create foreign key relationships
from sqlalchemy.orm import relationship
# create_engine class used in configuration code at the EOF
from sqlalchemy import create_engine

# instance of declarative_base class
Base = declarative_base()

# class to store user information
class User(Base):
	# table info
	__tablename__ = 'user'

	# mapper
	id = Column(Integer, primary_key = True)
	name = Column(String(250), nullable = False)
	email = Column(String(250), nullable = False)
	image = Column(String(250))


# class for categories
class Category(Base):
	# table info
	__tablename__ = 'category'

	# mapper
	id = Column(Integer, primary_key = True)
	name = Column(String(250), nullable = False)
	# user_id = Column(Integer, ForeignKey('user.id'))
	# user = relationship(User)

	@property
	def serialize(self):
		# returns object data in easily serializeable format
		return {
			'name' : self.name,
			'id' : self.id
		}
	

# class for items
class Item(Base):
	# table info
	__tablename__ = 'items'

	# mapper
	id = Column(Integer, primary_key = True)
	name = Column(String(250), nullable = False)
	description = Column(String(), nullable = False)
	date = Column(DateTime, nullable = False)
	category_id = Column(Integer, ForeignKey('category.id'))
	category = relationship(Category)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)

	@property
	def serialize(self):
		# returns object data in easily serializeable format
		return {
			'name' : self.name,
			'id' : self.id,
			'description': self.description,
			'category' : self.category.name
		}

######insert at end of file #######
# instance of create_engine class pointing to the db
engine = create_engine('sqlite:///HikingCatalog.db')
# adds classes as tables in db
Base.metadata.create_all(engine)