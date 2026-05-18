from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from schema import HouseData

import joblib
import numpy as np

from database import SessionLocal
from database import engine
from database import Base

from models import Prediction

app = FastAPI()

# CREATE TABLE
Base.metadata.create_all(bind=engine)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# LOAD MODEL
model = joblib.load("../model/model.pkl")
scaler = joblib.load("../model/scaler.pkl")

# FRONTEND
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

@app.get("/")
def home():
    return FileResponse("../frontend/index.html")


# PREDICTION API
@app.post("/predict")
def predict(data: HouseData):

    db = SessionLocal()

    try:

        features = np.array([[
            data.sqft,
            data.yrbuilt,
            data.beds,
            data.baths,
            data.floors,
            data.view,
            data.cond,
            data.waterfront
        ]])

        scaled_data = scaler.transform(features)

        prediction = model.predict(scaled_data)

        predicted_price = float(prediction[0])

        # SAVE DATABASE
        new_prediction = Prediction(
            sqft=data.sqft,
            yrbuilt=data.yrbuilt,
            beds=data.beds,
            baths=data.baths,
            floors=data.floors,
            view=data.view,
            cond=data.cond,
            waterfront=data.waterfront,
            predicted_price=predicted_price
        )

        db.add(new_prediction)
        db.commit()

        return {
            "predicted_price": round(predicted_price, 2)
        }

    except Exception as e:
        return {
            "error": str(e)
        }

    finally:
        db.close()