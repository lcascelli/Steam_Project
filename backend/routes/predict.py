from fastapi import APIRouter
from pydantic import BaseModel
import joblib
import os
import numpy as np

router = APIRouter()

@router.post("/predict")
async def predict(data:dict):
    return {"received": data}


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

    return {
        "Predicted Ownership Classification": prediction.tolist(),
        "Predicted Probabilities Across Classes": {str(cls): float(prob) for cls, prob in zip(model.classes_, predicted_proba)}
    }