from pydantic import BaseModel


class HouseData(BaseModel):

    sqft: float

    yrbuilt: int

    beds: int

    baths: float

    floors: float

    view: int

    cond: int

    waterfront: int