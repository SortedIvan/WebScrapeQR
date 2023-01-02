from fastapi import APIRouter
from database.databaseConnection import sessionLocal
from starlette.responses import JSONResponse

router = APIRouter() # Defines application to be a router for linking
