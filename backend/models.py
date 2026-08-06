from sqlalchemy import Column, Integer, Float, String
from backend.database import Base

class Prediction(Base):

    __tablename__ = "prediction"

    id = Column(Integer, primary_key=True, index=True)

    Area = Column(String)

    SuperBuiltup_sqft = Column(Float)

    Carpet_sqft = Column(Float)

    BHK = Column(Integer)

    Bathroom = Column(Integer)

    Balcony = Column(Integer)

    Floor = Column(Integer)

    TotalFloors = Column(Integer)

    Parking = Column(Integer)

    AgeYears = Column(Integer)

    PredictedPrice = Column(Float)