import streamlit as st
import pandas as pd
import requests
from io import StringIO

DATASETS_ENDPOINT = "http://localhost:8000/datas"
DATA_ENDPOINT = "http://localhost:8000/data"

st.set_page_config(
    page_title="Visualisation des données",
    page_icon="📊",
    layout="wide"
)

st.header("📊 Visualisation des Données")

# Récupération de la liste des datasets
try:
    response = requests.get(DATASETS_ENDPOINT, timeout=5)
    response.raise_for_status()
    datasets = response.json()
except Exception as e:
    st.error(f"Erreur lors de la récupération des datasets : {e}")
    st.stop()

# Selectbox pour choisir le dataset
dataset_options = [""] + datasets
selected_dataset = st.selectbox(
    "Sélectionnez un dataset",
    options=dataset_options,
    format_func=lambda x: "-- Choisissez un dataset --" if x == "" else x
)

# Affichage du dataset sélectionné
if selected_dataset:
    try:
        # Charger les métadonnées du dataset
        response = requests.get(DATA_ENDPOINT + f"/{selected_dataset}", timeout=10)
        response.raise_for_status()
        data_info = response.json()
        
        # En-tête avec informations générales
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📁 Dataset", selected_dataset)
        with col2:
            st.metric("📊 Nombre de lignes", f"{data_info['row_count']:,}")
        with col3:
            st.metric("📋 Nombre de colonnes", len(data_info['columns']))
        
        st.markdown("---")
        
        # Affichage des colonnes et types
        st.subheader("🔍 Structure du dataset")
        
        # Créer un DataFrame pour afficher les colonnes
        columns_df = pd.DataFrame([
            {"Colonne": col, "Type": dtype}
            for col, dtype in data_info['columns'].items()
        ])
        
        # Ajouter des emojis selon le type
        def get_type_emoji(dtype):
            if 'int' in dtype:
                return "🔢"
            elif 'float' in dtype:
                return "💯"
            elif 'bool' in dtype:
                return "✅"
            elif 'object' in dtype:
                return "📝"
            else:
                return "❓"
        
        columns_df['Type'] = columns_df['Type'].apply(
            lambda x: f"{get_type_emoji(x)} {x}"
        )
        
        # Afficher dans un tableau stylisé
        st.dataframe(
            columns_df,
            use_container_width=True,
            height=400,
            hide_index=True
        )
        
        # Statistiques sur les types
        with st.expander("📈 Répartition des types de données"):
            type_counts = columns_df['Type'].str.extract(r'(int|float|bool|object)')[0].value_counts()
            col1, col2 = st.columns([2, 1])
            with col1:
                st.bar_chart(type_counts)
            with col2:
                for dtype, count in type_counts.items():
                    st.metric(dtype, count)
        
    except Exception as e:
        st.error(f"Erreur lors du chargement des données : {e}")
        st.write("Détails de l'erreur :", str(e))
else:
    st.info("👆 Veuillez sélectionner un dataset ci-dessus")