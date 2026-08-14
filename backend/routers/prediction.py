from pydantic import BaseModel 
from fastapi import APIRouter 
import pandas as pd 
import pickle 
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_PATH = BASE_DIR / "model" / "model.pkl"

model = pickle.load(open(MODEL_PATH, "rb"))
router = APIRouter()

class inputModel(BaseModel):
    brand : str 
    model : str
    vehicle_age : float 
    km_driven : float 
    fuel_type : str 
    transmission_type : str 
    mileage : float 
    engine : int 

@router.post('/post')
def predict(input:inputModel):
    input_df = pd.DataFrame([input.model_dump()])
    
    prediction = model.predict(input_df)
    pred = prediction.tolist()[0]
    return pred