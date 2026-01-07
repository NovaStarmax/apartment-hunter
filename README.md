# Apartment hunter

A real estate price prediction application for Madrid properties, built on a Kaggle dataset. This project combines Data Science, Data Engineering, and application deployment with a complete Frontend + API + ML models architecture, runnable locally or via Docker Compose.

Dataset: https://www.kaggle.com/datasets/mirbektoktogaraev/madrid-real-estate-market

---

## Features

- Predict apartment prices in Madrid based on property characteristics
- REST API built with FastAPI for model inference
- Interactive frontend using Streamlit
- Trained models exported as .joblib files
- Training metrics and model information exposed through the API
- Simplified deployment with Docker & Docker Compose

---

## Architecture

```
[ Streamlit Frontend ]
          |
          v
[ FastAPI Backend ]
          |
          v
[ ML Pipeline (.joblib) ]
```

- The frontend collects user inputs
- The API dynamically loads the selected model
- The sklearn pipeline applies preprocessing + prediction
- Results are returned to the frontend

---

## Project Structure

```
apartment-hunter/
├── backend/
│   ├── api.py                 # FastAPI application
│   ├── schema.py              # Pydantic schemas
│   ├── models/                # ML models + training_results.json
│   ├── data/                  # CSV files used by the API
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── index.py               # Streamlit app
│   ├── pages/
│   ├── Dockerfile
│   └── requirements.txt
│
├── notebooks/                 # EDA / cleaning / training
├── docker-compose.yml
├── makefile
├── pyproject.toml
└── README.md
```

---

## Running with Docker Compose (recommended)

### Prerequisites
- Docker Desktop installed and running
- Docker Compose (included with Docker Desktop)

### Launch

From the project root:

```bash
docker compose up --build
```

### Access
- Frontend (Streamlit): http://localhost:8501
- API (FastAPI): http://localhost:8000
- API Documentation (Swagger): http://localhost:8000/docs

### Stop

```bash
CTRL + C
```

### Restart

```bash
docker compose up
```

---

## Running Locally (development mode)

Useful for rapid iteration without Docker rebuilds.

### Prerequisites
- Python 3.11
- uv installed

### Single command

```bash
uv run make dev
```

This launches:
- FastAPI API on localhost:8000
- Streamlit frontend on localhost:8501

---

## Configuration

### Environment Variables

No .env file required.

The frontend uses:

```python
API_URL = os.getenv("API_URL", "http://localhost:8000")
```

- In Docker, API_URL is injected via docker-compose.yml
- Locally, the localhost fallback is used

---

## Models & Data

- ML Models: `backend/models/*.joblib`
- Training results: `backend/models/training_results.json`
- CSV data: `backend/data/`

Models are loaded dynamically based on the name provided by the frontend.

---

## Tech Stack

- Python 3.11
- FastAPI
- Streamlit
- scikit-learn
- pandas
- joblib
- Docker / Docker Compose
- uv

---

## Project Goals

This project demonstrates:
- End-to-end Data project structuring
- Clear separation between training and inference
- Production deployment of an ML model
- Full application containerization