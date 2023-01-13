from sqlalchemy import Column, String, Boolean, Integer
from database.databaseConnection import base


# In order for comparisons to be faster and easer
# PropertyCity(int) = 1:Amsterdam, 2: Rotterdam, etc..
# PropertyType(int) = 1: Appartment, 2: Room, 3: House, etc.

class User(base):
    __tablename__="users"
    id=Column(String(255),primary_key=True,index=True)
    username = Column(String(255), index = True)
    email = Column(String(255), index = True)
    password = Column(String(255), index = True)
    subscribed = Column((Boolean),index=True)
    property_city = Column(Integer(10), index = True)
    property_type = Column(Integer(10), index = True)
    min_price = Column(Integer(20), index = True)
    max_price = Column(Integer(20), index = True)
    property_sqm = Column(Integer(20), index = True)


