from utils import train_and_evaluate_model
from pathlib import Path
import joblib
import json
import pandas as pd
from utils import train_and_evaluate_model
from sklearn.linear_model import LinearRegression
import sys

def main():
  data_path = Path('data/houses_madrid.csv')
  df = pd.read_csv(data_path)
  df = df[['buy_price', 'sq_mt_built', 'n_rooms', 'n_bathrooms']]
  pipeline, metrics = train_and_evaluate_model(
        df,
        LinearRegression(),
        columns_to_scale=['sq_mt_built']  # StandarScaler dans le code de utils.py
    )

  Path("artifacts").mkdir(exist_ok=True)

  joblib.dump(pipeline, "artifacts/model_linear_v1.pkl")


if __name__ == "__main__":
    main()