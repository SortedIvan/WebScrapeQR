from scrapers.funda import fundascraper
from scrapers.huislijn import huislijnscraper
from scrapers.huurstunt import huurstuntscraper
from scrapers.brickvast import brickvastscraper
from scrapers.budgethousing import budgethousingscraper
from database.databaseConnection import sessionLocal
from models import rental
from service.citites import cities
from sqlalchemy.sql import func



# -------------- General --------------------
async def CreateFundaRentalListingObjects():
    with sessionLocal() as session:
        try:
            for i in range(len(cities)):
                listings = fundascraper.GetFundaRentalListings(cities[i])

                for listing in listings:
                    listing_exists = session.query(rental.FundaListing).filter(rental.FundaListing.listingUrl == listing.listingUrl).count()

                    if listing_exists:
                        continue

                    funda_listing = rental.FundaListing (
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
                listing_exists = session.query(rental.HuurstuntListing).filter(rental.HuurstuntListing.listingUrl == listing.listingUrl).count()

                if listing_exists:
                    continue

                huurstunt_listing = rental.HuurstuntListing (
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
                    listing_exists = session.query(rental.HuislijnListing).filter(rental.HuislijnListing.listingUrl == listing.listingUrl).count()

                    if listing_exists:
                        continue

                    huislijn_listing = rental.HuislijnListing (
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
# --------------------------------------------


# --------------eindhoven specific-------------------------
async def CreateBrickvastRentalObjects():
    with sessionLocal() as session:
        listings = brickvastscraper.GetAllBrickvastRentalListings()
        for listing in listings:
            listing_exists = session.query(rental.BrickvastListing).filter(rental.BrickvastListing.listingUrl == listing.listingUrl).count()

            if listing_exists:
                continue

            brickvast_listing = rental.BrickvastListing (
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

            session.add(brickvast_listing)
            session.commit()            

async def CreateBudgetHousingRentalObjects():
    with sessionLocal() as session:
        listings = budgethousingscraper.GetBudgetHousingListings()
        for listing in listings:
            listing_exists = session.query(rental.BudgetHousingListing).filter(rental.BudgetHousingListing.listingUrl == listing.listingUrl).count()

            if listing_exists:
                continue

            budgethousinglisting = rental.BudgetHousingListing (
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

            session.add(budgethousinglisting)
            session.commit()   
# ----------------end eindhoven---------------------------