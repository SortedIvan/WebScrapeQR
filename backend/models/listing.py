from sqlalchemy import Column, String, Integer
from database.databaseConnection import base

class RentalListing(base):
    __tablename__="rentals"
    id=Column(String(255),primary_key=True,index=True)
    listingCity = Column(String(255), index = True)
    listingType = Column(String(255), index = True)
    listingName = Column(String(255), index = True)
    listingDate = Column(String(255),index=True)
    listingPrice = Column(Integer,index=True)
    listingSqm = Column(Integer,index=True)
    listingRooms = Column(String(255),index=True)
    listingExtraInfo = Column(String(255),index=True)
    listingUrl = Column(String(255), index = True)
    listingAdress = Column(String(255), index = True)

class RentalCity(base):
    __tablename__ = "rental_citites"
    city = Column(String(255), primary_key = True, index = True)
    listing_id = Column(String(255), index = True)

class RentalListingUser(base):
    __tablename__ = "rentals_users"
    property_id = Column(String(255), primary_key = True, index = True)
    user_id = Column(String(255), index = True)