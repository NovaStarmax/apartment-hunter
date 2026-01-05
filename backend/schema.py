from pydantic import BaseModel
class PredictionInputTest(BaseModel):
    sq_mt_built: int
    n_rooms: int
    n_bathrooms: int

class PredictionOutputTest(BaseModel):
    predicted_price: float | int