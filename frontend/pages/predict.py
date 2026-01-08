import streamlit as st
import requests
from babel.numbers import format_currency
import os

energy_scores = {
    "A": 7,
    "B": 6,
    "C": 5,
    "D": 4,
    "E": 3,
    "F": 2,
    "G": 1,
}

houses_types = {
    1: "Pisos",
    2: "Casa o chalet",
    4: "Dúplex",
    5: "Áticos",
}

districts = {
    "Arganzuela": [
        "Imperial",
        "Chopera",
        "Acacias",
        "Delicias",
        "Palos de Moguer",
        "Legazpi",
    ],
    "Barajas": [
        "Casco Histórico de Barajas",
        "Alameda de Osuna",
        "Timón",
        "Campo de las Naciones-Corralejos",
    ],
    "Carabanchel": [
        "Opañel",
        "Comillas",
        "Abrantes",
        "San Isidro",
        "Puerta Bonita",
        "Vista Alegre",
        "Pau de Carabanchel",
        "Buena Vista",
    ],
    "Centro": [
        "Lavapiés-Embajadores",
        "Huertas-Cortes",
        "Malasaña-Universidad",
        "Chueca-Justicia",
        "Palacio",
        "Sol",
    ],
    "Chamartín": [
        "El Viso",
        "Nueva España",
        "Castilla",
        "Bernabéu-Hispanoamérica",
        "Prosperidad",
        "Ciudad Jardín",
    ],
    "Chamberí": [
        "Gaztambide",
        "Nuevos Ministerios-Ríos Rosas",
        "Almagro",
        "Trafalgar",
        "Arapiles",
        "Vallehermoso",
    ],
    "Ciudad Lineal": [
        "Ventas",
        "Pueblo Nuevo",
        "Quintana",
        "San Juan Bautista",
        "Colina",
        "Costillares",
        "Concepción",
        "San Pascual",
    ],
    "Fuencarral": [
        "Las Tablas",
        "Mirasierra",
        "Montecarmelo",
        "La Paz",
        "Peñagrande",
        "Pilar",
        "Fuentelarreina",
        "Tres Olivos - Valverde",
        "Arroyo del Fresno",
    ],
    "Hortaleza": [
        "Sanchinarro",
        "Conde Orgaz-Piovera",
        "Valdebebas - Valdefuentes",
        "Canillas",
        "Palomas",
        "Virgen del Cortijo - Manoteras",
        "Pinar del Rey",
        "Apóstol Santiago",
    ],
    "Latina": [
        "Puerta del Ángel",
        "Aluche",
        "Lucero",
        "Los Cármenes",
        "Águilas",
        "Campamento",
    ],
    "Moncloa": [
        "Aravaca",
        "Argüelles",
        "Ciudad Universitaria",
        "Valdezarza",
        "Casa de Campo",
        "Valdemarín",
        "El Plantío",
    ],
    "Moratalaz": ["Fontarrón", "Vinateros", "Marroquina", "Media Legua"],
    "Puente de Vallecas": [
        "Palomeras sureste",
        "Palomeras Bajas",
        "San Diego",
        "Entrevías",
        "Numancia",
        "Portazgo",
    ],
    "Retiro": ["Niño Jesús", "Ibiza", "Adelfas", "Pacífico", "Jerónimos", "Estrella"],
    "Salamanca": [
        "Recoletos",
        "Goya",
        "Lista",
        "Castellana",
        "Guindalera",
        "Fuente del Berro",
    ],
    "Tetuán": [
        "Valdeacederas",
        "Cuzco-Castillejos",
        "Cuatro Caminos",
        "Bellas Vistas",
        "Berruguete",
        "Ventilla-Almenara",
    ],
    "Usera": [
        "Orcasitas",
        "San Fermín",
        "Moscardó",
        "Pradolongo",
        "Zofío",
        "Almendrales",
        "12 de Octubre-Orcasur",
    ],
    "Vicálvaro": [
        "Valdebernardo - Valderribas",
        "Ambroz",
        "Casco Histórico de Vicálvaro",
        "El Cañaveral - Los Berrocales",
    ],
    "Villa de Vallecas": [
        "Casco Histórico de Vallecas",
        "Ensanche de Vallecas - La Gavia",
        "Santa Eugenia",
    ],
    "Villaverde": [
        "San Cristóbal",
        "Los Ángeles",
        "San Andrés",
        "Los Rosales",
        "Butarque",
    ],
}


API_URL = os.getenv("API_URL", "http://localhost:8000")
PREDICT_ENDPOINT = f"{API_URL}/predicted"
METRICS_ENDPOINT = f"{API_URL}/metrics"

st.set_page_config(page_title="Estimateur", page_icon="🔍")
st.markdown("# 🏠 Estimation immobilière")


def bool01(v: bool) -> int:
    return 1 if v else 0


@st.dialog("Résultat de l'estimation")
def show_result(data: dict) -> None:
    st.markdown("# 💰 Prix estimé")
    st.write(format_currency(data["predicted_price"], "EUR", locale="fr_FR"))


try:
    resp = requests.get(METRICS_ENDPOINT, timeout=5)
    resp.raise_for_status()
    all_models = resp.json()
except Exception as e:
    st.error(f"Erreur lors de l'appel à l'API : {e}")
    st.stop()

model_options = [""] + list(all_models.keys())
model_names = {k: all_models[k].get("name", k) for k in all_models.keys()}
model_names[""] = "-- Sélectionnez un modèle --"

preselected_model = st.session_state.get("selected_model", "")
default_index = (
    model_options.index(preselected_model) if preselected_model in model_options else 0
)

selected_model = st.selectbox(
    "Modèle",
    options=model_options,
    index=default_index,
    format_func=lambda x: model_names[x],
    key="predict_model_select",
)

if not selected_model:
    st.info("👆 Veuillez sélectionner un modèle ci-dessus pour continuer")
    st.stop()

st.markdown(f"### Modèle actif : **{model_names[selected_model]}**")
st.markdown("---")


st.write("# Veuillez remplir ce questionnaire")

# ---- Localisation (CAT) ----
st.subheader("Localisation")

district_list = sorted(districts.keys())
default_district = "Centro" if "Centro" in district_list else district_list[0]

district = st.selectbox(
    "Secteur", options=district_list, index=district_list.index(default_district)
)

neighborhood_list = districts.get(district, [])
if not neighborhood_list:
    st.error("Aucun neighborhood disponible pour ce district.")
    st.stop()

default_neigh = "Sol" if "Sol" in neighborhood_list else neighborhood_list[0]
neighborhood = st.selectbox(
    "Quartier",
    options=neighborhood_list,
    index=neighborhood_list.index(default_neigh),
)

st.subheader("Type de bien")

house_type_options = list(houses_types.items())
house_type_label_to_value = {label: label for _, label in house_type_options}
house_type_labels = [label for _, label in house_type_options]

default_house_type = "Pisos" if "Pisos" in house_type_labels else house_type_labels[0]
house_type = st.selectbox(
    "House type",
    options=house_type_labels,
    index=house_type_labels.index(default_house_type),
)


colA, colB = st.columns(2)

with colA:
    st.subheader("Caractéristiques")

    sq_mt_built = st.number_input(
        "Surface construite (m²)", min_value=10, max_value=500, value=70, step=1
    )
    n_rooms = st.number_input(
        "Nombre de pièces", min_value=0, max_value=20, value=3, step=1
    )
    n_bathrooms = st.number_input(
        "Nombre de salles de bain", min_value=0, max_value=10, value=1, step=1
    )

    floor = st.number_input(
        "Étage",
        min_value=0,
        max_value=80,
        value=3,
        step=1,
        help="0 = rez-de-chaussée",
    )
    built_year = st.number_input(
        "Année de construction",
        min_value=1800,
        max_value=2026,
        value=1990,
        step=1,
    )

    neigh_price_m2 = st.number_input(
        "Prix moyen du quartier (€/m²)",
        min_value=0,
        max_value=20000,
        value=4000,
        step=50,
    )

    energy_letter = st.selectbox(
        "Classe énergétique",
        options=list(energy_scores.keys()),
        index=list(energy_scores.keys()).index("D"),
    )
    energy_certificate = float(energy_scores[energy_letter])

with colB:
    st.subheader("Votre bien comprend")

    has_ac = st.checkbox("Climatisation", value=False)
    has_lift = st.checkbox("Ascenseur", value=True)
    is_exterior = st.checkbox("Extérieur", value=True)
    has_garden = st.checkbox("Jardin", value=False)
    has_pool = st.checkbox("Piscine", value=False)
    has_terrace = st.checkbox("Terrasse", value=False)
    has_storage_room = st.checkbox("Cave / Storage room", value=False)
    has_parking = st.checkbox("Parking", value=False)
    # état
    is_renewal_needed = st.checkbox("Travaux nécessaires", value=False)
    is_new_development = st.checkbox("Programme neuf", value=False)


col_btn1, col_btn2 = st.columns([1, 2])

with col_btn1:
    if st.button("Back to metrics"):
        st.switch_page("pages/metrics.py")

with col_btn2:
    if st.button("Estimer le prix", type="primary"):
        payload = {
            "display_name": all_models[selected_model]["name"],
            "artifact_name": all_models[selected_model]["artifact_name"],
            # NUM
            "sq_mt_built": float(sq_mt_built),
            "n_rooms": int(n_rooms),
            "n_bathrooms": float(n_bathrooms),
            "floor": float(floor),
            "is_renewal_needed": int(bool01(is_renewal_needed)),
            "is_new_development": int(bool01(is_new_development)),
            "built_year": float(built_year),
            "has_ac": int(bool01(has_ac)),
            "has_lift": int(bool01(has_lift)),
            "is_exterior": int(bool01(is_exterior)),
            "has_garden": int(bool01(has_garden)),
            "has_pool": int(bool01(has_pool)),
            "has_terrace": int(bool01(has_terrace)),
            "has_storage_room": int(bool01(has_storage_room)),
            "energy_certificate": float(energy_certificate),
            "has_parking": int(bool01(has_parking)),
            "neigh_price_m2": float(neigh_price_m2),
            # CAT
            "neighborhood": neighborhood.strip(),
            "district": district.strip(),
            "house_type": house_type.strip(),
        }

        try:
            r = requests.post(PREDICT_ENDPOINT, json=payload, timeout=15)
            r.raise_for_status()
            data = r.json()
            show_result(data)
        except Exception as e:
            st.error(f"Erreur lors de l'appel à l'API : {e}")
            st.caption(
                "Astuce: vérifie que district/neighborhood/house_type matchent les catégories vues à l'entraînement."
            )
