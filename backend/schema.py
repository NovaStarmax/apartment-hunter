from pydantic import BaseModel


class PredictionInputTest(BaseModel):
    artifact_name: str
    sq_mt_built: int
    n_rooms: int
    n_bathrooms: int


class PredictionOutput(BaseModel):
    predicted_price: float | int

class PredictionInput(BaseModel):
    artifact_name: str
    sq_mt_built: int
    n_rooms: int
    n_bathrooms: int
    floor: int | float
    is_renewal_needed: bool
    is_new_development: bool
    built_year: int | float
    has_ac: bool
    has_lift: bool
    is_exterior: bool
    has_garden: bool
    has_pool: bool
    has_terrace: bool
    has_storage_room: bool
    energy_certificate: int
    has_parking: bool
    neigh_price_m2: float | int
    neighborhood: str
    district: str
    house_type: str