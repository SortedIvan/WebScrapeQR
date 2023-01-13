from pydantic import BaseModel
class UserData(BaseModel):
    username: str
    useremail: str
    userpassword: str
