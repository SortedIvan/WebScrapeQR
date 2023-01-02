from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scheduler.scheduler import sched

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

@app.get("/")
async def root():
  return {"message": "Welcome to Rentswipe!"}

# Every day at 12AM, delete all instances of listings from the database and make space for new ones
#@sched.scheduled_job('cron', day_of_week='mon-sun', hour=24)

