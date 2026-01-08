from fastapi import FastAPI
from .schema import PredictionOutput, PredictionInput
import json
from functools import lru_cache
import pandas as pd
import joblib
from pathlib import Path

app = FastAPI()


@lru_cache()
def load_model_info():
    with open(Path(__file__).parent / "models" / "training_results.json") as f:
        return json.load(f)


def build_dataframe(input: PredictionInput) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "sq_mt_built": [input.sq_mt_built],
            "n_rooms": [input.n_rooms],
            "n_bathrooms": [input.n_bathrooms],
            "floor": [input.floor],
            "is_renewal_needed": [input.is_renewal_needed],
            "is_new_development": [input.is_new_development],
            "built_year": [input.built_year],
            "has_ac": [input.has_ac],
            "has_lift": [input.has_lift],
            "is_exterior": [input.is_exterior],
            "has_garden": [input.has_garden],
            "has_pool": [input.has_pool],
            "has_terrace": [input.has_terrace],
            "has_storage_room": [input.has_storage_room],
            "energy_certificate": [input.energy_certificate],
            "has_parking": [input.has_parking],
            "neigh_price_m2": [input.neigh_price_m2],
            "neighborhood": [input.neighborhood],
            "district": [input.district],
            "house_type": [input.house_type],
        }
    )


@app.post("/predicted", response_model=PredictionOutput)
def predict(input: PredictionInput) -> PredictionOutput:
    model = input.artifact_name
    try:
        pipeline = joblib.load(Path(__file__).parent / "models" / model)
    except FileNotFoundError:
        raise ValueError(
            f'Le modèle "{model}" n’a pas été trouvé dans la base de donnée.'
        )
    X = build_dataframe(input)
    prediction = pipeline.predict(X)

    return PredictionOutput(
        predicted_price=prediction[0],
    )


@app.get("/metric/{model_name}")
def get_model_info(model_name: str) -> dict:
    model_info = load_model_info()
    return model_info[model_name]


@app.get("/metrics")
def get_all_metrics() -> dict:
    return load_model_info()


@app.get("/datas")
def return_datasets() -> list[str]:
    all_files = Path(__file__).parent / "data"
    csv_files = [f.name for f in all_files.iterdir() if f.suffix == ".csv"]
    return csv_files


@app.get("/data/{file_name}")
def get_data(file_name: str):
    data_dir = Path(__file__).parent / "data"
    file_path = data_dir / file_name
    df = pd.read_csv(file_path)
    columns_info = {col: str(df[col].dtype) for col in df.columns}
    return {"columns": columns_info, "row_count": len(df)}
