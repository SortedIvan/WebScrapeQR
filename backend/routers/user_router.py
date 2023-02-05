import uuid
from fastapi import APIRouter, HTTPException, Depends
from database.databaseConnection import sessionLocal
from starlette.responses import JSONResponse
from utility_data.userdata import UserData
from models.user import User, UserSalt
from tools.auth import AuthHandler
from datetime import timedelta
from service.auth_service import create_access_token, EncryptPassword, EncryptCompare, DecryptPassword, ACCESS_TOKEN_EXPIRE_MINUTES
from utility_data.user_preference import UserPreference
from tools.custom_exception import NoneException

router = APIRouter() # Defines application to be a router for linking
auth = AuthHandler() # Defines the authentication handler for password hashing and JWT tokens

# ------------------- UTILITY FUNCTIONS -----------------------------------------
def CheckUserEmail(useremail, session):
    try:
        user_with_same_email = session.query(User).filter(User.email == useremail).first()
        if user_with_same_email is not None:
            print(user_with_same_email)    
            return False
    except:
        print("Testing API")
    return True
# --------------------------------------------------------------------------------

#TODO: Add salting
@router.post("/api/register", status_code=201)
def register_user(userdata: UserData):
    with sessionLocal() as session:
        if not CheckUserEmail(userdata.dict().get("useremail"), session):
            raise HTTPException(status_code=400, detail="A user with this email already exists")

        hashed_password = auth.get_password_hash(userdata.dict().get('userpassword'))
        user = User(
            id = str(uuid.uuid4()),
            username = userdata.dict().get('username'),
            email = userdata.dict().get('useremail'),
            password = hashed_password,
            subscribed = False
        )
        session.add(user)
        session.commit()
    return

@router.post("/api/login")
def login_user(userdata: UserData):
    with sessionLocal() as session:
        user = None
        try:
            user = session.query(User).filter(User.email == userdata.dict().get('useremail')).first()
        except:
            raise HTTPException(status_code=400, detail = "A user with this email does not exist.")
        
        if (user is None) or (not auth.verify_password(userdata.dict().get("userpassword"), user.password)):
            raise HTTPException(status_code=400, detail = "Invalid email or password.")
        
        token = auth.encode_token(user.id)
        return {'token':token }

@router.put("/api/set-preferences")
async def SetUserPreferences(preference: UserPreference, user_id = Depends(auth.auth_wrapper)):
    with sessionLocal() as session:
        # First, get the user
        # TODO: Check token here
        user = session.query(User).filter(User.id == user_id).first()

        if user is None:
            raise NoneException("User has not been found! Please provide a valid user email.")
        
        user.property_city = preference.dict().get("property_city")
        user.property_type = preference.dict().get("property_type")
        user.min_price = preference.dict().get("min_price")
        user.max_price = preference.dict().get("max_price")
        user.property_sqm = preference.dict().get("property_sqm")
        
        session.commit()
        
        return JSONResponse(status_code=200, 
                        content = {"message": "User preferences succesfuly updated."})
