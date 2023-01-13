import uuid
from fastapi import APIRouter
from database.databaseConnection import sessionLocal
from starlette.responses import JSONResponse
from utility_data.userdata import UserData
from models.user import User


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


#TODO: Salt password on register and give the user a token response
@router.post("/api/register-user")
async def RegisterUser(userdata: UserData) -> JSONResponse:
    with sessionLocal() as session:
        if CheckUserEmail(userdata.dict().get("useremail"), session):
            user = User (
                id = str(uuid.uuid4()),
                username = userdata.dict().get("username"),
                email = userdata.dict().get("useremail"),
                password = userdata.dict().get("userpassword"),
                subscribed = True
            )
            #TODO: Hashing the passwords & checking for username
            session.add(user)
            session.commit()
            return JSONResponse(status_code=200, 
                content = {"message": "Sucessfully registered.", "registered":True, "username":userdata.dict().get("username"),
                "user_email": userdata.dict().get("useremail")})

        #Case where user's email already exists, we return false
        return JSONResponse(status_code=401, 
        content = {"message": "Email already exists!", "registered":False})