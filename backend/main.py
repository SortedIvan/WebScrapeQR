from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from service.email_service import SendRentalPropertyEmails

from models.rental import OldRentalListing,RentalListingUser, RentalListing, BrickvastListing, BudgetHousingListing
from models.rental import FriendlyHousing, FundaListing, HuislijnListing, HuurstuntListing

from apscheduler.schedulers.background import BackgroundScheduler
from database.databaseConnection import engine, sessionLocal, base
from routers import user_router
from utility.stopwatch import time_convert
import service.rental_fetch_service as rental_service
import time
import datetime
from datetime import date, timedelta
from models.user import User, UserSalt

app = FastAPI()

origins = [
    # "http://localhost",
    # "http://localhost:8080",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "HEAD", "OPTIONS"],
    allow_headers=[
      "Access-Control-Allow-Headers",
      "Content-Type", "Authorization", 
      "Access-Control-Allow-Origin","Set-Cookie"
    ]
)

base.metadata.create_all(bind=engine)

app.include_router(user_router.router)

# --------------- UTILITY METHODS -------------------------
def TestScheduler():
  print("hi")

def ClearOutOldRentalListings():
  with sessionLocal() as session:   
    try:
        session.query(RentalListing).delete()
        session.commit()
    except:
        #session.rollback()
        return

def ClearOutOldUserRentalConnections():
  with sessionLocal() as session:
    try:
      session.query(RentalListingUser).delete()
    except:
      #session.rollback()
      return

LISTING_TYPES = [BrickvastListing, BudgetHousingListing, FriendlyHousing, FundaListing, HuislijnListing, HuurstuntListing]
def MoveListingsToOld():
  with sessionLocal() as session:
    try:
      for type in LISTING_TYPES:
        today = datetime.datetime.today()
        thirty_days_ago = today - timedelta(days=30)
        listings_to_move = session.query(type).filter(type.dateCreated <= thirty_days_ago).all()
        for i in range(len(listings_to_move)):
          old_listing = OldRentalListing(
            id = listings_to_move[i].id,
            listingCity = listings_to_move[i].listingCity,
            listingType = listings_to_move[i].listingType,
            listingName = listings_to_move[i].listingName,
            listingDate = listings_to_move[i].listingDate,
            listingPrice = listings_to_move[i].listingPrice,
            listingSqm = listings_to_move[i].listingSqm,
            listingRooms = listings_to_move[i].listingRooms,
            listingExtraInfo = listings_to_move[i].listingExtraInfo,
            listingUrl = listings_to_move[i].listingUrl,
            listingAdress = listings_to_move[i].listingAdress,
            listingImageUrl = listings_to_move[i].listingImageUrl,
            dateCreated = listings_to_move[i].dateCreated
          )
          session.delete(listings_to_move[i])
          session.add(old_listing)
          session.commit()  
    except Exception as ex:
      print("Something went wrong")
      print(ex)

# -----------------------------------------------------------


@app.on_event('startup')
def init_data():
    sched = BackgroundScheduler()
    #Every day at 12AM, delete all instances of listings from the database and make space for new ones
    sched.add_job(MoveListingsToOld, 'cron', day_of_week = 'mon-sun', hour = 23, minute = 59)
    sched.add_job(ClearOutOldRentalListings, 'cron', day_of_week = 'mon-sun', hour = 23, minute = 59)
    sched.add_job(ClearOutOldUserRentalConnections, 'cron', day_of_week = 'mon-sun', hour = 23, minute = 59)

    #TODO: Add fetching new listings every 15-20 minutes
    sched.start()

@app.get("/deleteoldlistingstest")
async def delete_old_listings_test():
  start_time = time.time()
  MoveListingsToOld()
  end_time = time.time()
  time_lapsed = end_time - start_time
  print(time_convert(time_lapsed))
  return {"message" : "Sucessful", "time_it_took":str(time_convert(time_lapsed))}

@app.get("/")
async def root():
  #Testing purposes only
  return {"message": "Welcome to Rentswipe!"}

@app.get("/api/CreateRentalObjects")
async def test():
  start_time = time.time()
  
  #----------------------general----------------------------
  await rental_service.CreateFundaRentalListingObjects()
  await rental_service.CreateHuislijnListingObjects()
  await rental_service.CreateHuurstuntListingObjects()
  #-------------------end general---------------------------

  #------------------eindhoven specific-----------------------
  await rental_service.CreateBrickvastRentalObjects()
  await rental_service.CreateBudgetHousingRentalObjects()
  #------------------end eindhoven----------------------------

  end_time = time.time()
  time_lapsed = end_time - start_time
  print(time_convert(time_lapsed))

  return {"message" : "Sucessful", "time_it_took":str(time_convert(time_lapsed))}

@app.get("/api/send-user-offers")
async def TestSendEmails():
  await SendRentalPropertyEmails()


#----------------- API FOR TESTING -----------------------------
@app.get("/api/deleteusers")
async def DeleteAllUsers():
  with sessionLocal() as session:
    session.query(User).delete()
    session.query(UserSalt).delete()
    session.commit()
    return {"message": "users deleted succesfully"}

@app.get("/api/deleterentals")
async def DeleteRentalsAndConnections():
  ClearOutOldRentalListings()
  ClearOutOldUserRentalConnections()
  return {"message": "rentals deleted succesfully"}
# -------------------------------------------------------------