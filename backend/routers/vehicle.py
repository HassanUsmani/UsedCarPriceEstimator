from fastapi import APIRouter, status, HTTPException
from data import df

router = APIRouter()
@router.get('/engine/{brandname}/{modelname}')
def engine_size(brandname: str, modelname: str):
    related_data = df.loc[(df['model'] == modelname) & (df['brand'] == brandname)]
    related_engine = related_data['engine'].unique()
    if(len(related_engine) == 0):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f'Car with the given details is not available')
    return related_engine.tolist()

@router.get('/fuel/{brandname}/{modelname}/{engine}')
def fuel_type(engine : int, modelname : str, brandname : str):
    related_data = df.loc[(df['brand'] == brandname) & (df['model'] == modelname) & (df['engine'] == engine)]
    related_fuel = related_data['fuel_type'].unique()
    if(len(related_fuel) == 0):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'Car with the given details is not available')
    return related_fuel.tolist()

@router.get('/trans/{brandname}/{modelname}/{engine}')
def transmission_type(brandname : str, modelname : str, engine : int): 
    related_data = df.loc[(df['brand'] == brandname) & (df['model'] == modelname) & (df['engine'] == engine)]
    related_trans = related_data['transmission_type'].unique()
    if(len(related_trans) == 0):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Car with the given details is not available')
    return related_trans.tolist()
