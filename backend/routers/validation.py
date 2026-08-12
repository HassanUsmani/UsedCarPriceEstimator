from fastapi import APIRouter, status, HTTPException
from data import df, grouped 

router = APIRouter()
@router.get('/mileage/{engine}')
def mileage_range(engine: int): 
    if engine < 1000:
        min = grouped.loc["<1000","min"]
        max = grouped.loc["<1000","max"]
    elif 1000 <= engine < 1500:
        min = grouped.loc["1000-1499","min"]
        max = grouped.loc["1000-1499","max"]
    elif 1500 <= engine < 2000:
        min = grouped.loc["1500-1999","min"]
        max = grouped.loc["1500-1999","max"]
    elif 2000 <= engine < 2500:
        min = grouped.loc["2000-2499","min"]
        max = grouped.loc["2000-2499","max"]
    elif 2500 <= engine < 3000:
        min = grouped.loc["2500-2999","min"]
        max = grouped.loc["2500-2999","max"]
    else:
        min = grouped.loc["3000+","min"]
        max = grouped.loc["3000+","max"]
    return {"min":min, "max":max}
            
@router.get('/vehicle_age/{brandname}/{modelname}')
def veh_age_range(brandname : str, modelname : str):
    related_data = df.loc[(df['brand'] == brandname) & (df['model'] == modelname)]
    if(len(related_data) == 0):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car with the details is not available")
    start_year = related_data['model_start_year'].unique().tolist()[0]
    return start_year