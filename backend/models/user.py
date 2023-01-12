from sqlalchemy import Column, String, Boolean
from database.databaseConnection import base

class User(base):
    __tablename__="users"
    id=Column(String(255),primary_key=True,index=True)
    username = Column(String(255), index = True)
    email = Column(String(255), index = True)
    password = Column(String(255), index = True)
    subscribed = Column((Boolean),index=True)
