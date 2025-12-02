from pydantic import BaseModel

class PredictionInput(BaseModel):
    district: str
    surface_m2: int

class PredictionOutput(BaseModel):
    predicted_price: float
    input_district: str
    input_surface_m2: int
    model_version: str