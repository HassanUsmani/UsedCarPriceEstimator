from pydantic import BaseModel 
from fastapi import APIRouter 
import pandas as pd 
import pickle 

model = pickle.load(open('../model/model.pkl','rb'))
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
    input_df = pd.DataFrame([input.dict()])
    
    prediction = model.predict(input_df)
    pred = prediction.tolist()[0]
    return pred
