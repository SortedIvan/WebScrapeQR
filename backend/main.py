from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from service.email_service import SendRentalPropertyEmails
from models.listing import RentalListingUser, RentalListing
from apscheduler.schedulers.background import BackgroundScheduler
from database.databaseConnection import engine, sessionLocal, base
from routers import user_router
from utility.stopwatch import time_convert
import service.rental_fetch_service as rental_service
import time

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
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
        session.query(RentalListingUser).delete()
        session.commit()
    except:
        #session.rollback()
        print("")
# -----------------------------------------------------------


@app.on_event('startup')
def init_data():
    sched = BackgroundScheduler()
    #sched.add_job(TestScheduler, 'cron', second='*/5')

    #Every day at 12AM, delete all instances of listings from the database and make space for new ones
    sched.add_job(ClearOutOldRentalListings, 'cron', day_of_week = 'mon-sun', hour = 23, minute = 59)
    sched.start()


@app.get("/")
async def root():
  #Testing purposes only
  return {"message": "Welcome to Rentswipe!"}

@app.get("/test")
async def test():
  start_time = time.time()
  await rental_service.CreateFundaRentalListingObjects()
  await rental_service.CreateHuislijnListingObjects()
  end_time = time.time()

  time_lapsed = end_time - start_time
  print(time_convert(time_lapsed))

  return {"message" : "Sucessful"}

@app.get("/test_user_email")
async def TestSendEmails():
  await SendRentalPropertyEmails()


