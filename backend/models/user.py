from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.types import LargeBinary
from database.databaseConnection import base


# In order for comparisons to be faster and easer
# PropertyCity(int) = 1:Amsterdam, 2: Rotterdam, etc..
# PropertyType(int) = 1: Appartment, 2: Room, 3: House, etc.

class User(base):
    __tablename__="users"
    id=Column(String(255),primary_key=True,index=True)
    username = Column(String(255), index = True)
    email = Column(String(255), index = True)
    #password = Column(LargeBinary, index = True)
    password = Column(String(255), index = True)
    subscribed = Column((Boolean),index=True)
    property_city = Column(Integer, index = True)
    property_type = Column(Integer, index = True)
    min_price = Column(Integer, index = True)
    max_price = Column(Integer, index = True)
    property_sqm = Column(Integer, index = True)

class UserSalt(base):
    __tablename__ = "usersalts"
    user_id = Column(String(255), primary_key = True, index = True)
    user_salt = Column(String(255), index = True)
    user_key = Column(LargeBinary, index = True)
