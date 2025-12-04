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
    page_title="Estimateur",
    page_icon="🔍",
)

st.write("# 🔍 Veuillez remplir ce questionnaire")

# Créer deux colonnes list(range(1, 11)) + ["Rez de chaussé"]
col1, col2 = st.columns(2)

with col1:
    st.markdown("## Quartier")
    district = st.selectbox("Quartier", options=["Option 1", "Option 2", "Option 3"], label_visibility="collapsed")

    st.markdown("## Surface (m²)")
    surface = st.number_input(
        "Surface",
        min_value=int(df['sq_mt_built'].min()),
        max_value=int(df['sq_mt_built'].max()),
        value=int(df['sq_mt_built'].median()),
        help="Surface totale construite de l'appartement",
        label_visibility="collapsed"
    )

    st.markdown("## Nombre de pièces")
    n_rooms = st.selectbox("Nombre de pièces", index=1, options=list(range(1, 11)), label_visibility="collapsed")

    st.markdown("## Nb de salles de bain")
    n_bath = st.selectbox("Nombre de salles de bain", index=0, options=list(range(1, 5)), label_visibility="collapsed")


with col2:
    st.markdown("## Étage")
    floor = st.selectbox("Étage", index=10, options=list(range(1, 11)) + ["Rez de chaussé"], label_visibility="collapsed")
    
    st.markdown("## Type de bien")
    property_type = st.selectbox("Type de bien", options=["Appartement", "Maison", "Studio"], label_visibility="collapsed")

    st.markdown("## Année du bien")
    built_year = st.number_input(
        "Année de construction",
        min_value=1800,
        max_value=2024,
        value=2000,
        help="Année de construction du bien",
        label_visibility="collapsed"
    )

    st.markdown("## Classe énergétique")
    energie_certificate = st.selectbox("Classe énergétique", index=2 ,options=["A", "B", "C", "D", "E", "F", "G"], label_visibility="collapsed")

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