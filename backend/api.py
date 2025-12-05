from fastapi import FastAPI
from .schema import PredictionInput, PredictionOutput
import json
from functools import lru_cache
from enum import Enum
import os
import pandas as pd

app = FastAPI()

class ModelName(str, Enum):
    linear_regression = "linear_regression"
    random_forest = "random_forest"

@lru_cache()
def load_model_info():
    with open("backend/model.json") as f:
        return json.load(f)

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

@app.get("/metrics/{model_name}")
def get_model_info(model_name: ModelName):
    model_info = load_model_info()
    return model_info[model_name]

@app.get("/metrics")
def get_all_metrics():
    """Récupère les métriques de tous les modèles."""
    return load_model_info()

@app.get("/datas")
def return_datasets():
    all_files = os.listdir("data/")
    csv_files = [f for f in all_files if f.endswith('.csv')]
    return csv_files

@app.get("/data/{file_name}")
def get_data(file_name: str):
    df = pd.read_csv(f"data/{file_name}")
    columns_info = {col: str(df[col].dtype) for col in df.columns}
    return {
        "columns": columns_info,
        "row_count": len(df)
    }