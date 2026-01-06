import streamlit as st
import pandas as pd
import requests

METRICS_ENDPOINT = "http://localhost:8000/metrics"

st.set_page_config(
    page_title="Metriques",
    page_icon="📊",
)

# Récupération des modèles
all_models = {}
try:
    response = requests.get(METRICS_ENDPOINT, timeout=5)
    response.raise_for_status()
    all_models = response.json()

except Exception as e:
    st.error(f"Erreur lors de l'appel à l'API : {e}")
    st.stop()

st.write("# Veuillez sélectionner un modèle pour afficher les métriques")

# Création des options avec une option vide par défaut
model_options = [""] + list(all_models.keys())
model_names = {key: all_models[key]["name"] for key in all_models.keys()}
model_names[""] = "-- Sélectionnez un modèle --"

selected_model = st.selectbox(
    "Modèle",
    options=model_options,
    format_func=lambda x: model_names[x],
    key="model_select",
)

if "show_metrics" not in st.session_state:
    st.session_state.show_metrics = False

if selected_model and st.button("Afficher les métriques"):
    st.session_state.show_metrics = True
    st.session_state.selected_model = selected_model

if selected_model and st.session_state.show_metrics:
    model_data = all_models[selected_model]

    st.markdown(f"## Modèle : {model_data['name']}")

    metrics = model_data.get("metrics", {})
    params = model_data.get("parameters", {})

    if metrics:
        metrics_df = pd.DataFrame(list(metrics.items()), columns=["Métrique", "Valeur"])
        params_df = pd.DataFrame(list(params.items()), columns=["Paramètre", "Valeur"])
        st.dataframe(metrics_df, hide_index=True, use_container_width=True)
        st.markdown("### Paramètres du modèle")
        st.dataframe(params_df, hide_index=True, use_container_width=True)
    else:
        st.write("Aucune métrique disponible pour ce modèle.")

    st.markdown("---")
    if st.button("Prédire votre bien", key="btn_predict", use_container_width=True):
        st.session_state.selected_model = selected_model  # Persister avant navigation
        st.switch_page("pages/predict.py")

elif not selected_model:
    st.session_state.show_metrics = False
    st.info("👆 Veuillez sélectionner un modèle ci-dessus")
