from scrapers.funda import fundascraper
from scrapers.huislijn import huislijnscraper
from scrapers.huurstunt import huurstuntscraper
from database.databaseConnection import sessionLocal
from models.listing import RentalListing
from service.citites import cities


async def CreateFundaRentalListingObjects():
    with sessionLocal() as session:
        try:
            for i in range(len(cities)):
                listings = fundascraper.GetFundaRentalListings(cities[i])

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
                        listingAdress = listing.listingAdress,
                        listingImageUrl = listing.imageUrl
                    )
                    print(listing.listingName)
                    session.add(funda_listing)
                    session.commit()
        except Exception as e:
            print(e)

async def CreateHuurstuntListingObjects():
    with sessionLocal() as session:
            listings = huurstuntscraper.GetAllListings()
            for listing in listings:
                listing_exists = session.query(RentalListing).filter(RentalListing.listingUrl == listing.listingUrl).count()

                if listing_exists:
                    continue

                huurstunt_listing = RentalListing (
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
                    listingAdress = listing.listingAdress,
                    listingImageUrl = listing.imageUrl
                )
                print(listing.listingName)
                session.add(huurstunt_listing)
                session.commit()

async def CreateHuislijnListingObjects():
        with sessionLocal() as session:
            for i in range(len(cities)):
                listings = huislijnscraper.GetHuislijnRentalListings(cities[i])

                for listing in listings:
                    listing_exists = session.query(RentalListing).filter(RentalListing.listingUrl == listing.listingUrl).count()

                    if listing_exists:
                        continue

                    huislijn_listing = RentalListing (
                        id = listing.listingId,
                        listingCity = cities[i],
                        listingType = listing.listingType,
                        listingName = listing.listingName,
                        listingDate = listing.listingDate,
                        listingPrice = listing.listingPrice,
                        listingSqm = listing.listingSqm,
                        listingRooms = listing.listingRooms,
                        listingExtraInfo = listing.listingExtraInfo,
                        listingUrl = listing.listingUrl,
                        listingAdress = listing.listingAdress,
                        listingImageUrl = listing.imageUrl
                    )

                    session.add(huislijn_listing)
                    session.commit()
