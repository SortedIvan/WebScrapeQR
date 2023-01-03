from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scheduler.scheduler import sched
import service.rental_fetch_service as rental_service
from database.databaseConnection import engine, sessionLocal, base
import time

def time_convert(sec):
  mins = sec // 60
  sec = sec % 60
  hours = mins // 60
  mins = mins % 60
  print("Time Lapsed = {0}:{1}:{2}".format(int(hours),int(mins),sec))



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

@app.get("/")
async def root():
  #Testing purposes only
  return {"message": "Welcome to Rentswipe!"}

@app.get("/test")
async def test():
    start_time = time.time()
    await rental_service.CreateFundaRentalListingObjects()
    end_time = time.time()
    time_lapsed = end_time - start_time
    time_it_took = time_convert(time_lapsed)
    return {"message" : "Hi!", "time_it_took":str(time_it_took)}

# Every day at 12AM, delete all instances of listings from the database and make space for new ones
#@sched.scheduled_job('cron', day_of_week='mon-sun', hour=24)

