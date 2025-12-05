from pydantic import BaseModel
from typing import Union

class PredictionInput(BaseModel):
    district: str # Bon
    surface_m2: int # Bon
    n_rooms: int # Bon
    n_bath: int # Bon
    floor: Union[int, str]  # For "Rez de chaussé"
    property_type: str
    built_year: int
    energie_certificate: str 

class PredictionOutput(BaseModel):
    predicted_price: float
    input_district: str
    input_surface_m2: int
    model_version: str