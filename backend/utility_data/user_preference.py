from pydantic import BaseModel

class UserPreference(BaseModel):
    property_city: int
    property_type: int
    min_price: int
    max_price: int
    property_sqm: int
