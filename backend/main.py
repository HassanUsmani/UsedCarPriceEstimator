from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel 
from fastapi.middleware.cors import CORSMiddleware
import pickle 
import pandas as pd
import os

print("Current working directory:", os.getcwd())
df = pd.read_csv("Data/carDekhoDataset.csv")
print(df.head())

app = FastAPI()

model = pickle.load(open('./model/model.pkl','rb'))
print('done')
origin = ['http://localhost:8080']
app.add_middleware(
    CORSMiddleware,
    allow_origins = origin,
    allow_credentials = True,
    allow_headers = ["*"],
    allow_methods = ["*"]
)

class inputModel(BaseModel):
    brand : str 
    model : str
    vehicle_age : float 
    km_driven : float 
    fuel_type : str 
    transmission_type : str 
    mileage : float 
    engine : int 

class modelname(BaseModel):
    model : str

@app.post('/post')
def predict(input:inputModel):
    input_df = pd.DataFrame([input.dict()])
    
    prediction = model.predict(input_df)
    pred = prediction.tolist()[0]
    return pred



@app.get('/engine/{brandname}/{modelname}')
def engine_size(brandname: str, modelname: str):
    related_data = df.loc[(df['model'] == modelname) & (df['brand'] == brandname)]
    related_engine = related_data['engine'].unique()
    if(len(related_engine) == 0):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f'Car with the given details is not available')
    print(related_engine)
    return related_engine.tolist()

@app.get('/fuel/{brandname}/{modelname}/{engine}')
def fuel_type(engine : int, modelname : str, brandname : str):
    related_data = df.loc[(df['brand'] == brandname) & (df['model'] == modelname) & (df['engine'] == engine)]
    related_fuel = related_data['fuel_type'].unique()
    if(len(related_fuel) == 0):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'Car with the given details is not available')
    print(related_fuel)
    return related_fuel.tolist()

@app.get('/trans/{brandname}/{modelname}/{engine}')
def transmission_type(brandname : str, modelname : str, engine : int): 
    related_data = df.loc[(df['brand'] == brandname) & (df['model'] == modelname) & (df['engine'] == engine)]
    related_trans = related_data['transmission_type'].unique()
    if(len(related_trans) == 0):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Car with the given details is not available')
    print(related_trans)
    return related_trans.tolist()