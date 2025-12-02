from fastapi import FastAPI
from .schema import PredictionInput, PredictionOutput

app = FastAPI()
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/predict", response_model=PredictionOutput)
def predict(input: PredictionInput):
    return PredictionOutput(
        predicted_price=123456,
        input_district=input.district,
        input_surface_m2=input.surface_m2,
        model_version="v0.0-dummy"
    )