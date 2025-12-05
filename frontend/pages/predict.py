import streamlit as st
import pandas as pd
import requests

DATA = 'data/houses_Madrid.csv'
PREDICT_ENDPOINT = "http://localhost:8000/predict"
METRICS_ENDPOINT = "http://localhost:8000/metrics"

st.set_page_config(
    page_title="Estimateur",
    page_icon="🔍",
)

st.markdown("# 🏠 Estimation immobilière")

# Récupération des modèles
all_models = {}
try:
    response = requests.get(METRICS_ENDPOINT, timeout=5)
    response.raise_for_status()
    all_models = response.json()
except Exception as e:
    st.error(f"Erreur lors de l'appel à l'API : {e}")
    st.stop()

# Création des options avec une option vide par défaut
model_options = [""] + list(all_models.keys())
model_names = {key: all_models[key]["name"] for key in all_models.keys()}
model_names[""] = "-- Sélectionnez un modèle --"

# Récupérer le modèle pré-sélectionné depuis metrics (s'il existe)
preselected_model = st.session_state.get("selected_model", "")
default_index = model_options.index(preselected_model) if preselected_model in model_options else 0

# Selectbox pour choisir le modèle
selected_model = st.selectbox(
    "🤖 Modèle",
    options=model_options,
    index=default_index,
    format_func=lambda x: model_names[x],
    key="predict_model_select"
)

if not selected_model:
    st.info("👆 Veuillez sélectionner un modèle ci-dessus pour continuer")
    st.stop()

st.markdown(f"### Modèle actif : **{model_names[selected_model]}**")
st.markdown("---")

st.write("# 🔍 Veuillez remplir ce questionnaire")

col1, col2 = st.columns(2)

with col1:
    st.markdown("## Quartier")
    district = st.selectbox("Quartier", options=["Option 1", "Option 2", "Option 3"], label_visibility="collapsed")

    st.markdown("## Surface (m²)")
    surface = st.number_input(
        "Surface",
        min_value=15,
        max_value=399,
        value=60,
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

if st.button("Back to metrics"):
    st.switch_page("pages/metrics.py")

if st.button("Estimer le prix"):
    if not selected_model:
        st.error("⚠️ Veuillez sélectionner un modèle avant d'estimer le prix")
        st.stop()
    
    payload = {
        "district": district,
        "surface_m2": int(surface),
        "n_rooms": n_rooms,
        "n_bath": n_bath,
        "floor": floor,
        "property_type": property_type,
        "built_year": built_year,
        "energie_certificate": energie_certificate,
    }

    try:
        response = requests.post(PREDICT_ENDPOINT, json=payload, timeout=5)
        response.raise_for_status()
        data = response.json()

        show_result(data)

    except Exception as e:
        st.error(f"Erreur lors de l'appel à l'API : {e}")