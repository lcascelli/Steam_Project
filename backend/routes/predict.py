from fastapi import APIRouter
from pydantic import BaseModel
import joblib
import os
import numpy as np

router = APIRouter()

model_path = os.path.join(os.path.dirname(__file__), '..', 'model', 'rf_model.joblib')

model = joblib.load(model_path)

class PredictionInput(BaseModel):
    Action: int
    Casual: int
    Adventure: int
    Simulation: int
    Strategy: int
    RPG: int
    Early_Access: int
    Free_To_Play: int
    Sports: int
    Racing: int
    Massively_Multiplayer: int
    Violent: int
    Gore: int
    positive: int
    negative: int
    average_forever: float
    median_forever: float
    ccu: int
    same_dev_pub: int


@router.options("/predict")
async def options_predict():
    return JSONResponse(
        content = {"message": "CORS preflight"},
        headers = {
            "Access-Control-Allow-Origin": "http://localhost:3000",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        }
    )

bin_map = {
    1: '0-100,000',
    2: '100,001-500,000',
    3: '500,001-1,000,000',
    4: '1,000,001-5,000,000',
    5: '5,000,001-10,000,000',
    6: '10,000,001+'
    }

@router.post("/predict")
def predict(input_data: PredictionInput):
    features = np.array([[
        input_data.Action,
        input_data.Casual,
        input_data.Adventure,
        input_data.Simulation,
        input_data.Strategy,
        input_data.RPG,
        input_data.Early_Access,
        input_data.Free_To_Play,
        input_data.Sports,
        input_data.Racing,
        input_data.Massively_Multiplayer,
        input_data.Violent,
        input_data.Gore,
        input_data.positive,
        input_data.negative,
        input_data.average_forever,
        input_data.median_forever,
        input_data.ccu,
        input_data.same_dev_pub
    ]])

    prediction = model.predict(features)[0]
    predicted_proba = model.predict_proba(features)[0]

    probabilities = {
        bin_map[int(cls)]: f"{prob * 100:.1f}%"
                for cls, prob in zip(model.classes_, predicted_proba)
    }

    return {
        "Predicted Ownership Range": bin_map[int(prediction)],
        "Predicted Probabilities Across Classes": probabilities,   
    }
