from pydantic import BaseModel


class PredictionInputTest(BaseModel):
    artifact_name: str
    sq_mt_built: int
    n_rooms: int
    n_bathrooms: int


class PredictionOutputTest(BaseModel):
    predicted_price: float | int
