from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from Setup_file import *

engine = create_engine('sqlite:///bookyard.db')
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

# Delete BookYard if exisitng.
session.query(BookYard).delete()
# Delete BookName if exisitng.
session.query(BookName).delete()
# Delete User if exisitng.
session.query(GmailUser).delete()

# Create sample users data
SampleUser = GmailUser(name="Madisetty Prathyusha",
                       email="mgprathyusha@gmail.com",
                       )
session.add(SampleUser)
session.commit()
print ("Successfully Add First User")
# Create sample book names
Type1 = BookYard(name="Biography",
                 user_id=1)
session.add(Type1)
session.commit()

Type2 = BookYard(name="Business",
                 user_id=1)
session.add(Type2)
session.commit

Type3 = BookYard(name="Children's",
                 user_id=1)
session.add(Type3)
session.commit()

Type4 = BookYard(name="Cookbook",
                 user_id=1)
session.add(Type4)
session.commit()

Type5 = BookYard(name="Health & Fitness",
                 user_id=1)
session.add(Type5)
session.commit()

Type6 = BookYard(name="History",
                 user_id=1)
session.add(Type6)
session.commit()

# Populare a bykes with models for testing
# Using different users for bykes names year also
item1 = BookName(name="Wings of Fire",
                 year="1999",
                 booktype="Leader biography",
                 author="A.P.J.Abdul Kalam",
                 price="226",
                 bookyardid=1,
                 gmailuser_id=1)
session.add(item1)
session.commit()

item2 = BookName(name="Indian Unbound",
                 year="2019",
                 booktype="Economics",
                 author="Gurcharan Das",
                 price="340",
                 bookyardid=2,
                 gmailuser_id=1)
session.add(item2)
session.commit()

item3 = BookName(name="Charlotte's Web",
                 year="1952",
                 booktype="Animals",
                 author="E.B.White",
                 price="624",
                 bookyardid=3,
                 gmailuser_id=1)
session.add(item3)
session.commit()

item4 = BookName(name="The Ultimate Ice Cream Book",
                 year="1999",
                 booktype="Desserts",
                 author="Bruce Weinstein",
                 price="958",
                 bookyardid=4,
                 gmailuser_id=1)
session.add(item4)
session.commit()

item5 = BookName(name="The Great Indian Diet",
                 year="2014",
                 booktype="special diet",
                 author="Shilpa Shetty",
                 price="170",
                 bookyardid=5,
                 gmailuser_id=1)
session.add(item5)
session.commit()

item6 = BookName(name="Krishna",
                 year="2008",
                 booktype="Religious History",
                 author="Tapasi de",
                 price="500",
                 bookyardid=6,
                 gmailuser_id=1)
session.add(item6)
session.commit()

print("Your books database has been inserted!")
