import streamlit as st
import pandas as pd
import requests

DATA = 'data/houses_Madrid.csv'
METRICS_ENDPOINT = "http://localhost:8000/metrics"

st.set_page_config(
    page_title="Apartment Hunter",
    page_icon="🏠",
    layout="wide"
)

st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        color: white;
        font-size: 3rem;
        margin: 0;
    }
    .subtitle {
        text-align: center;
        font-size: 1.3rem;
        color: #666;
        margin-bottom: 3rem;
    }
    .stButton>button {
        width: 100%;
        height: 150px;
        font-size: 1.2rem;
        font-weight: bold;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🏠 Apartment Hunter</h1></div>', unsafe_allow_html=True)

st.markdown('<p class="subtitle">Votre assistant intelligent pour la recherche d\'appartements à Madrid</p>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Cards pour les boutons
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("### 📊 Exploration des données")
    st.markdown("Visualisez et analysez les données immobilières de Madrid")
    if st.button("Afficher les données", key="btn_data", use_container_width=True):
        st.switch_page("pages/data_viz.py")

with col2:
    st.markdown("### 🎯 Performance des modèles")
    st.markdown("Découvrez les métriques et performances de nos modèles ML")
    if st.button("Voir les performances", key="btn_metrics", use_container_width=True):
        st.switch_page("pages/metrics.py")