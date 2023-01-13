from pydantic import BaseModel


# Object for initial creation/registration/login of user
class UserData(BaseModel):
    username: str
    useremail: str
    userpassword: str

# Object for using the object within the system (for sending emails, setting preferences, etc)
class SystemUser:
    def __init__(self, _username, _useremail, _subscribed, _property_city, _property_type, _min_price, _max_price, _property_sqm):
        self.username = _username
        self.useremail = _useremail
        self.subscribed = _subscribed
        self.property_city = _property_city
        self.property_type = _property_type
        self.min_price = _min_price
        self.max_price = _max_price
        self.property_sqm = _property_sqm