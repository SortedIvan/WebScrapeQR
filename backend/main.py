from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scheduler.scheduler import sched
import service.rental_fetch_service as rental_service
from database.databaseConnection import engine, sessionLocal, base

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
    await rental_service.CreateFundaRentalListingObjects()
    return {"message" : "Hi!"}

# Every day at 12AM, delete all instances of listings from the database and make space for new ones
#@sched.scheduled_job('cron', day_of_week='mon-sun', hour=24)

