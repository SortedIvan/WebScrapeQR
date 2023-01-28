from fastapi import APIRouter
from database.databaseConnection import sessionLocal
from starlette.responses import JSONResponse
from fastapi_utils.tasks import repeat_every

router = APIRouter() # Defines application to be a router for linking

