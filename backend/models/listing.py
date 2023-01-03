from sqlalchemy import Column, String
from database.databaseConnection import base

class FundaRentalListing(base):
    __tablename__="funda_rentals"
    id=Column(String(255),primary_key=True,index=True)
    listingType = Column(String(255), index = True)
    listingName = Column(String(255), index = True)
    listingDate = Column(String(255),index=True)
    listingPrice = Column(String(255),index=True)
    listingSqm = Column(String(255),index=True)
    listingRooms = Column(String(255),index=True)
    listingExtraInfo = Column(String(255),index=True)
    listingUrl = Column(String(255), index = True)
    listingAdress = Column(String(255), index = True)

class HuislijnRentalListing(base):
    __tablename__="huislijn_rentals"
    id=Column(String(255),primary_key=True,index=True)
    listingType = Column(String(255), index = True)
    listingName = Column(String(255), index = True)
    listingDate = Column(String(255),index=True)
    listingPrice = Column(String(255),index=True)
    listingSqm = Column(String(255),index=True)
    listingRooms = Column(String(255),index=True)
    listingExtraInfo = Column(String(255),index=True)

class HuurstuntRentalListing(base):
    __tablename__="huurstund_rentals"
    id=Column(String(255),primary_key=True,index=True)
    listingType = Column(String(255), index = True)
    listingName = Column(String(255), index = True)
    listingDate = Column(String(255),index=True)
    listingPrice = Column(String(255),index=True)
    listingSqm = Column(String(255),index=True)
    listingRooms = Column(String(255),index=True)
    listingExtraInfo = Column(String(255),index=True)

class RentalCity(base):
    __tablename__ = "rental_citites"
    city = Column(String(255), primary_key = True, index = True)
    listing_id = Column(String(255), index = True)

