import uuid
from fastapi import APIRouter
from database.databaseConnection import sessionLocal
from starlette.responses import JSONResponse
from utility_data.userdata import UserData
from models.user import User, UserSalt
from datetime import timedelta
from fastapi import HTTPException
from service.auth_service import create_access_token, EncryptPassword, EncryptCompare, DecryptPassword, ACCESS_TOKEN_EXPIRE_MINUTES
from utility_data.user_preference import UserPreference
from tools.custom_exception import NoneException

router = APIRouter() # Defines application to be a router for linking

def CheckUserEmail(useremail, session):
    try:
        user_with_same_email = session.query(User).filter(User.email == useremail).first()
        if user_with_same_email is not None:
            print(user_with_same_email)    
            return False
    except:
        print("Testing API")
    return True

@router.post("/api/register")
async def register(userdata: UserData):
    with sessionLocal() as session:
        if CheckUserEmail(userdata.dict().get("useremail"), session):
            # Generate a salt
            pw_info = EncryptPassword(userdata.dict().get("userpassword"))

            salt = pw_info[0]
            hashed_pw = pw_info[1]
            encrypt_key = pw_info[2]

            user = User (
                id = str(uuid.uuid4()),
                username = userdata.dict().get("username"),
                email = userdata.dict().get("useremail"),
                password = hashed_pw,
                subscribed = True
            )

            user_salt = UserSalt (
                user_id = user.id,
                user_salt = salt,
                user_key = encrypt_key
            )

            session.add(user)
            session.add(user_salt)
            session.commit()
            session.refresh(user)
            session.refresh(user_salt)
            return JSONResponse(status_code=200, 
                content = {"message": "Sucessfully registered.", "registered":True, "username":userdata.dict().get("username"),
                "user_email": userdata.dict().get("useremail")})

        #Case where user's email already exists, we return false
        return JSONResponse(status_code=401, 
        content = {"message": "Email already exists!", "registered":False})

@router.post("/api/login")
async def login(userdata: UserData):
    with sessionLocal() as session:
        db_user = session.query(User).filter(User.email == userdata.dict().get("useremail")).first()
        user_salt = session.query(UserSalt).filter(UserSalt.user_id == db_user.id).first()
        if db_user is None:
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        if not EncryptCompare(db_user.password, userdata.dict().get("userpassword"),user_salt.user_salt, user_salt.user_key):
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        # Create the access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": db_user.email}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer", "message": "Login succesful"}

@router.put("/api/set-preferences")
async def SetUserPreferences(preference: UserPreference, useremail):
    with sessionLocal() as session:
        # First, get the user
        # TODO: Check token here
        user = session.query(User).filter(User.email == useremail).first()

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



