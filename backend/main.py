from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import prediction, validation, vehicle


app = FastAPI()


origin = ["http://localhost:8080","https://used-car-price-estimator.vercel.app"]
app.add_middleware(
    CORSMiddleware,
    allow_origins = origin,
    allow_credentials = True,
    allow_headers = ["*"],
    allow_methods = ["*"]
)

app.include_router(prediction.router,tags=["Prediction"])
app.include_router(validation.router,tags=["Validation"])
app.include_router(vehicle.router,tags=["Vehicle"])

