import streamlit as st
import pandas as pd
import requests

DATA = 'data/houses_Madrid.csv'
PREDICT_ENDPOINT = "http://localhost:8000/predict"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA)
    return df

df = load_data()

st.set_page_config(
    page_title="Apartment Hunter",
    page_icon="🏠",
)

st.write("# 🏠 Estimer votre bien à Madrid")
st.markdown("## Veuillez sélectionner le quartier de votre bien")

district = st.selectbox("Quartier", options=["Option 1", "Option 2", "Option 3"])

st.markdown("## Veuillez renseigner les m² de votre bien")

surface = st.number_input(
    "Surface",
    min_value=int(df['sq_mt_built'].min()),
    max_value=int(df['sq_mt_built'].max()),
    value=int(df['sq_mt_built'].median()),
    help="Surface totale construite de l'appartement"
)

@st.dialog("Résultat de l'estimation")
def show_result(data):
    st.markdown("# 💰 Prix estimé")
    st.write(f"{data['predicted_price']} €")

    st.markdown("### 📍 Détails")
    st.write(f"- Quartier : {data.get('input_district', district)}")
    st.write(f"- Surface : {data.get('input_surface_m2', surface)} m²")
    st.write(f"- Modèle : {data.get('model_version', 'inconnu')}")

if st.button("Estimer le prix"):
    payload = {
        "district": district,
        "surface_m2": int(surface),
    }

    try:
        response = requests.post(PREDICT_ENDPOINT, json=payload, timeout=5)
        response.raise_for_status()
        data = response.json()

        show_result(data)

    except Exception as e:
        st.error(f"Erreur lors de l'appel à l'API : {e}")