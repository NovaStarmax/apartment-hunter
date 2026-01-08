import requests

END_POINT = "http://localhost:8000/predicted"

row = {
    "artifact_name": "linear_regression_model.joblib",
    "sq_mt_built": 60.0,
    "n_rooms": 3,
    "n_bathrooms": 1.0,
    "floor": 3.0,
    "is_renewal_needed": 0,
    "is_new_development": 0,
    "built_year": 1960.0,
    "has_ac": 1,
    "has_lift": 0,
    "is_exterior": 1,
    "has_garden": 0,
    "has_pool": 0,
    "has_terrace": 0,
    "has_storage_room": 0,
    "energy_certificate": 4.0,
    "has_parking": 0,
    "neigh_price_m2": 1308.89,
    "neighborhood": "San Cristóbal",
    "district": "Villaverde",
    "house_type": "Pisos",
}
response = requests.post(END_POINT, json=row)
print("Response JSON:", response.json())
