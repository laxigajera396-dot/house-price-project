from sqlalchemy import Column

from sqlalchemy import Integer

from sqlalchemy import Float


from database import Base


class Prediction(Base):

    __tablename__ = "predictions"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    sqft = Column(Float)

    yrbuilt = Column(Integer)

    beds = Column(Integer)

    baths = Column(Float)

    floors = Column(Float)

    view = Column(Integer)

    cond = Column(Integer)

    waterfront = Column(Integer)

    predicted_price = Column(Float)