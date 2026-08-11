from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel 
from fastapi.middleware.cors import CORSMiddleware
import pickle 
import pandas as pd
import os

print("Current working directory:", os.getcwd())
df = pd.read_csv("Data/carDekhoDataset_preprocessed.csv")
df["engine_group"] = pd.cut(
    df["engine"],
    bins=[0, 1000, 1500, 2000, 2500, 3000, float("inf")],
    labels=[
        "<1000",
        "1000-1499",
        "1500-1999",
        "2000-2499",
        "2500-2999",
        "3000+"]
)
grouped = (
    df.groupby(
        ["engine_group"],
        observed=True
    )["mileage"]
    .agg(["min", "max","count"])
)
print(grouped.index)
print(grouped)
print(df['fuel_type'].value_counts())
app = FastAPI()

model = pickle.load(open('./model/model.pkl','rb'))

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
    return related_engine.tolist()

@app.get('/fuel/{brandname}/{modelname}/{engine}')
def fuel_type(engine : int, modelname : str, brandname : str):
    related_data = df.loc[(df['brand'] == brandname) & (df['model'] == modelname) & (df['engine'] == engine)]
    related_fuel = related_data['fuel_type'].unique()
    if(len(related_fuel) == 0):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'Car with the given details is not available')
    return related_fuel.tolist()

@app.get('/trans/{brandname}/{modelname}/{engine}')
def transmission_type(brandname : str, modelname : str, engine : int): 
    related_data = df.loc[(df['brand'] == brandname) & (df['model'] == modelname) & (df['engine'] == engine)]
    related_trans = related_data['transmission_type'].unique()
    if(len(related_trans) == 0):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Car with the given details is not available')
    return related_trans.tolist()

@app.get('/mileage/{engine}')
def mileage_range(engine: int): 
    if(engine < 1000):
        min = grouped.loc["<1000","min"]
        max = grouped.loc["<1000","max"]
    elif(engine >= 1000 & engine < 1500):
        min = grouped.loc["1000-1499","min"]
        max = grouped.loc["1000-1499","max"]
    elif(engine >= 1500 & engine < 2000):
        min = grouped.loc["1500-1999","min"]
        max = grouped.loc["1500-1999","max"]
    elif(engine >= 2000 & engine < 2500):
        min = grouped.loc["2000-2499","min"]
        max = grouped.loc["2000-2499","max"]
    elif(engine >= 2500 & engine < 3000):
        min = grouped.loc["2500-2999","min"]
        max = grouped.loc["2500-2999","max"]
    else:
        min = grouped.loc["3000+","min"]
        max = grouped.loc["3000+","min"]
    return {"min":min, "max":max}
            
@app.get('/vehicle_age/{brandname}/{modelname}')
def veh_age_range(brandname : str, modelname : str):
    related_data = df.loc[(df['brand'] == brandname) & (df['model'] == modelname)]
    start_year = related_data['model_start_year'].unique().tolist()[0]
    return start_year