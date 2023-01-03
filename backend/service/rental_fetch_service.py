from scrapers.funda import fundascraper
from scrapers.huislijn import huislijnscraper
from scrapers.huurstunt import huurstuntscraper
from database.databaseConnection import sessionLocal
from scheduler.scheduler import sched
from database.databaseConnection import sessionLocal
from models.listing import FundaRentalListing, HuislijnRentalListing, HuurstuntRentalListing

cities_funda = [
    "amsterdam",
    "rotterdam",
    "den-haag",
    "utrecht",
    "eindhoven",
    "tilburg",
    "almere",
    "groningen",
    "breda",
    "nijmegen",
    "enschede",
    "apeldoorn",
    "haarlem",      
    "arnhem",           
    "gemeente-zaanstad",         
    "amersfoort",          
    "gemeente-haarlemmermeer",  
    "den-bosch",
    "zoetermeer",
    "zwolle",
    ]

async def CreateFundaRentalListingObjects():
    with sessionLocal() as session:
        try:
            for i in range(len(cities_funda)):
                listings = fundascraper.GetFundaRentalListings(cities_funda[i])

                for listing in listings:
                    listing_exists = session.query(FundaRentalListing).filter(FundaRentalListing.listingUrl == listing.listingUrl).count()

                    if listing_exists:
                        continue

                    funda_listing = FundaRentalListing (
                        id = listing.listingId,
                        listingType = listing.listingType,
                        listingName = listing.listingName,
                        listingDate = listing.listingDate,
                        listingPrice = listing.listingPrice,
                        listingSqm = listing.listingSqm,
                        listingRooms = listing.listingRooms,
                        listingExtraInfo = listing.listingExtraInfo,
                        listingUrl = listing.listingUrl,
                        listingAdress = listing.listingAdress
                    )
                    print(listing.listingName)
                    session.add(funda_listing)
                    session.commit()
        except Exception as e:
            print(e)

