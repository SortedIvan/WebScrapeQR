from sqlalchemy import Column, String
from database.databaseConnection import base

class RentalU1K(base):
    __tablename__="rental_U1K"
    id=Column(String(255),primary_key=True,index=True)
    listingType = Column(String(255), index = True)
    listingName = Column(String(255), index = True)
    listingDate = Column(String(255),index=True)
    listingPrice = Column(String(255),index=True)
    listingSqm = Column(String(255),index=True)
    listingRooms = Column(String(255),index=True)
    listingExtraInfo = Column(String(255),index=True)

class RentalB1K2K(base):
    __tablename__="rentalB1K2K"
    id=Column(String(255),primary_key=True,index=True)
    listingType = Column(String(255), index = True)
    listingName = Column(String(255), index = True)
    listingDate = Column(String(255),index=True)
    listingPrice = Column(String(255),index=True)
    listingSqm = Column(String(255),index=True)
    listingRooms = Column(String(255),index=True)
    listingExtraInfo = Column(String(255),index=True)

class RentalA2K(base):
    __tablename__="rentalA2K"
    id=Column(String(255),primary_key=True,index=True)
    listingType = Column(String(255), index = True)
    listingName = Column(String(255), index = True)
    listingDate = Column(String(255),index=True)
    listingPrice = Column(String(255),index=True)
    listingSqm = Column(String(255),index=True)
    listingRooms = Column(String(255),index=True)
    listingExtraInfo = Column(String(255),index=True)




