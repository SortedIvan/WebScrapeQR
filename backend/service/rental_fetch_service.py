from scrapers.funda import fundascraper
from scrapers.huislijn import huislijnscraper
from scrapers.huurstunt import huurstuntscraper
from database.databaseConnection import sessionLocal
from scheduler.scheduler import sched
from database.databaseConnection import sessionLocal
from models.listing import RentalListing
from service.citites import cities_funda, cities_huurstunt, cities_huislijn


async def CreateFundaRentalListingObjects():
    with sessionLocal() as session:
        try:
            for i in range(len(cities_funda)):
                listings = fundascraper.GetFundaRentalListings(cities_funda[i])

                for listing in listings:
                    listing_exists = session.query(RentalListing).filter(RentalListing.listingUrl == listing.listingUrl).count()

                    if listing_exists:
                        continue

                    funda_listing = RentalListing (
                        id = listing.listingId,
                        listingCity = listing.listingCity,
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

async def CreateHuurstuntListingObjects():
    with sessionLocal() as session:
            for i in range(len(cities_huurstunt)):
                listings = huurstuntscraper.GetAllRentalListings(cities_huurstunt[i])

                for listing in listings:
                    listing_exists = session.query(RentalListing).filter(RentalListing.listingUrl == listing.listingUrl).count()

                    if listing_exists:
                        continue

                    huurstunt_listing = RentalListing (
                        id = listing.listingId,
                        listingCity = cities_huurstunt[i],
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
                    session.add(huurstunt_listing)
                    session.commit()

async def CreateHuislijnListingObjects():
        with sessionLocal() as session:
            for i in range(len(cities_huislijn)):
                listings = huislijnscraper.GetHuislijnRentalListings(cities_huislijn[i])

                for listing in listings:
                    listing_exists = session.query(RentalListing).filter(RentalListing.listingUrl == listing.listingUrl).count()

                    if listing_exists:
                        continue

                    huislijn_listing = RentalListing (
                        id = listing.listingId,
                        listingCity = cities_huislijn[i],
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

                    print(listing.listingCity)
                    print(listing.listingType)
                    print(listing.listingName)
                    print(listing.listingDate)
                    print(listing.listingPrice)
                    print(listing.listingSqm)
                    print(listing.listingRooms)
                    print(listing.listingExtraInfo)
                    print(listing.listingUrl)

                    print(listing.listingName)
                    session.add(huislijn_listing)
                    session.commit()
