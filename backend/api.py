from fastapi import FastAPI
from .schema import PredictionInputTest, PredictionOutputTest
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


def build_dataframe(input: PredictionInputTest) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "sq_mt_built": [input.sq_mt_built],
            "n_rooms": [input.n_rooms],
            "n_bathrooms": [input.n_bathrooms],
        }
    )


@app.post("/predicted", response_model=PredictionOutputTest)
def predict(input: PredictionInputTest) -> PredictionOutputTest:
    model = input.artifact_name
    try:
        pipeline = joblib.load(Path(__file__).parent / "models" / model)
    except FileNotFoundError:
        raise ValueError(
            f'Le modèle "{model}" n’a pas été trouvé dans la base de donnée.'
        )
    X = build_dataframe(input)
    prediction = pipeline.predict(X)

    return PredictionOutputTest(
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
