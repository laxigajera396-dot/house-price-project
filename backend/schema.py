from pydantic import BaseModel

class HouseInput(BaseModel):

    Area: str
    BHK: int
    Bathroom: int
    Balcony: int
    SuperBuiltup_sqft: float
    Carpet_sqft: float
    Floor: int
    TotalFloors: int
    Parking: int
    AgeYears: int