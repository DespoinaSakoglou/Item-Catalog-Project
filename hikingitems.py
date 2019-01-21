### populates ddatabase with information ###

# import dependencies from sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from database_setup import Base, User, Category, Item

# create_engine function shows which database the program should communicate with
engine = create_engine('sqlite:///HikingCatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


#delete user data, if existing
session.query(User).delete()
# delete category data, if existing
session.query(Category).delete()
# delete item data, if existing
session.query(Item).delete()


#create one user
user1 = User(name = "admin", 
			 email="ds_admin_ds@udacity.com", 
			 image="https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png")
session.add(user1)
session.commit()


# Items for Backpack
### create category Backpack
# , user_id = 1
category1 = Category(name = "Backpack")
session.add(category1)
session.commit()

### create items for Backpack
item1 = Item(name = "Day Pack", 
			 description = "A lightweight backpack with plenty of storage pockets.",
			 date=datetime.datetime.now(),
			 category_id = 1,
			 user_id = 1)
session.add(item1)
session.commit()

item2 = Item(name = "Rain Cover", 
			 description = "A backpack raincover in case of bad weather.",
			 date=datetime.datetime.now(),
			 category_id = 1,
			 user_id = 1)
session.add(item2)
session.commit()


# Items for Snacks
### create category Snacks
# , user_id = 1
category2 = Category(name = "Snacks")
session.add(category2)
session.commit()

### create items for Snacks
item1 = Item(name = "Food", 
			 description = "Energy bars, cookiesn dry food.",
			 date=datetime.datetime.now(),
			 category_id = 2,
			 user_id = 1)
session.add(item1)
session.commit()

item2 = Item(name = "Drinks", 
			 description = "Water, coffee/tea, energy drinks, soft drinks.",
			 date=datetime.datetime.now(),
			 category_id = 2,
			 user_id = 1)
session.add(item2)
session.commit()


# Items for Safety
### create category Safety
category3 = Category(name = "Safety")
session.add(category3)
session.commit()

### create items for Snacks
item1 = Item(name = "First Aid Kit", 
			 description = "Kit for wound treatment and medication.",
			 date=datetime.datetime.now(),
			 category_id = 3,
			 user_id = 1)
session.add(item1)
session.commit()

item2 = Item(name = "Sunsreen", 
			 description = "Sunscreen and lip balm with UV protection.",
			 date=datetime.datetime.now(),
			 category_id = 3,
			 user_id = 1)
session.add(item2)
session.commit()


# Items for Gear
### create category Gear
category4 = Category(name = "Gear")
session.add(category4)
session.commit()

### create items for Gear
item1 = Item(name = "Navigation Gear", 
			 description = "Map and compass for navigation.",
			 date=datetime.datetime.now(),
			 category_id = 4,
			 user_id = 1)
session.add(item1)
session.commit()

item2 = Item(name = "Lighting Gear", 
			 description = "Headlamps, flashlight.",
			 date=datetime.datetime.now(),
			 category_id = 4,
			 user_id = 1)
session.add(item2)
session.commit()


# Items for Electronics
### create category Electronics
category5 = Category(name = "Electronics")
session.add(category5)
session.commit()

### create items for Gear
item1 = Item(name = "Radio", 
			 description = "Radio device for communication.",
			 date=datetime.datetime.now(),
			 category_id = 5,
			 user_id = 1)
session.add(item1)
session.commit()


# Items for Clothing
### create category Clothing
category6 = Category(name = "Clothing")
session.add(category6)
session.commit()

### create items for Clothing
item1 = Item(name = "Jacket", 
			 description = "Lightweight jacket and rain jacket.",
			 date=datetime.datetime.now(),
			 category_id = 6,
			 user_id = 1)
session.add(item1)
session.commit()

item2 = Item(name = "Shirt", 
			 description = "Synthetic or wool shirt.",
			 date=datetime.datetime.now(),
			 category_id = 6,
			 user_id = 1)
session.add(item2)
session.commit()

item3 = Item(name = "Shoes", 
			 description = "Hiking shoes and synthetic or wool socks.",
			 date=datetime.datetime.now(),
			 category_id = 6,
			 user_id = 1)
session.add(item3)
session.commit()


# Items for Other
### create category Other
category7 = Category(name = "Other")
session.add(category7)
session.commit()

### no items in Other


print "added menu items!"
