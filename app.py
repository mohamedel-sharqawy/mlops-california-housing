from fastapi import FastAPI
from pydantic import BaseModel
import mlflow
import mlflow.xgboost
import pandas as pd
import xgboost as xgb
import os


app = FastAPI(title="California Housing Predictor")


class HousingInput(BaseModel):
    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    Population: float
    AveOccup: float
    Latitude: float
    Longitude: float


MODEL_PATH = os.getenv("MODEL_PATH", "./model")

model = None


@app.on_event("startup")
def load_model():
    global model
    model = mlflow.xgboost.load_model(MODEL_PATH)


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict")
def predict(data: HousingInput):

    input_data = pd.DataFrame([data.model_dump()])

    dmatrix = xgb.DMatrix(input_data)

    prediction = model.predict(dmatrix)[0]

    price = prediction * 100000

    return {
        "prediction": f"${price:,.2f}"
    }