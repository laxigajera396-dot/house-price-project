from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from pathlib import Path
import pandas as pd
import joblib

from database import Base, engine, SessionLocal
from models import Prediction
from schema import HouseInput

app = FastAPI(title="Surat House Price Prediction")

# ---------------- Database ----------------

Base.metadata.create_all(bind=engine)

# ---------------- CORS ----------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Template ----------------

BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(
    directory=str(BASE_DIR / "frontend")
)

# ---------------- Model ----------------

model = joblib.load(str(BASE_DIR / "model" / "model.pkl"))

encoder = joblib.load(str(BASE_DIR / "model" / "area_encoder.pkl"))

# ---------------- Home ----------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

# ---------------- Prediction ----------------

@app.post("/predict")
def predict(data: HouseInput):

    db = SessionLocal()

    area = encoder.transform([data.Area])[0]

    input_df = pd.DataFrame([{

        "Area": area,
        "BHK": data.BHK,
        "Bathroom": data.Bathroom,
        "Balcony": data.Balcony,
        "SuperBuiltup_sqft": data.SuperBuiltup_sqft,
        "Carpet_sqft": data.Carpet_sqft,
        "Floor": data.Floor,
        "TotalFloors": data.TotalFloors,
        "Parking": data.Parking,
        "AgeYears": data.AgeYears

    }])

    prediction = model.predict(input_df)[0]

    save_prediction = Prediction(

    Area=data.Area,

    SuperBuiltup_sqft=data.SuperBuiltup_sqft,

    Carpet_sqft=data.Carpet_sqft,

    BHK=data.BHK,

    Bathroom=data.Bathroom,

    Balcony=data.Balcony,

    Floor=data.Floor,

    TotalFloors=data.TotalFloors,

    Parking=data.Parking,

    AgeYears=data.AgeYears,

    PredictedPrice=float(prediction)

)

    db.add(save_prediction)
    db.commit()
    db.close()

    return {
        "Predicted Price": float(prediction)
    }

print("✅ MODEL IS RUNNING")