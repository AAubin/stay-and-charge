import logging
logger = logging.getLogger(__name__)

import streamlit as st
from config import SOCKET_TYPES_LABELS, POWER_BOUNDS

def render_filters() -> dict:
    """Affiche les widgets de filtres dans la sidebar et retourne les valeurs saisies.

    Returns:
        Dictionnaire avec les clés : city (str), search_radius (int, en mètres),
        max_distance (int, en km), searched (bool).
    """
    with st.sidebar:
        city = st.text_input(label='Ville ou code postal')
        radius = st.number_input(label='Rayon de recherche en km (max 50 km))', min_value=0, value=20, max_value=50)
        max_distance = st.selectbox(label='Distance max des bornes de recharge (km)', options=[1, 5, 10, 15, 20])
        searched = st.button(label='Recherche')
        st.divider()
        min_rating = st.slider(label="Note minimal du logement:", min_value=0.0, max_value=5.0, value=0.0, step=0.1, format="%0.1f")
        st.divider()
        socket_types_wanted = st.multiselect(label="Types de prise", options=SOCKET_TYPES_LABELS.values(), default=SOCKET_TYPES_LABELS.values())
        min_power = st.slider(label="Puissance minimale (kW)", min_value=POWER_BOUNDS[0], max_value=POWER_BOUNDS[1], value=0, step=10)

    return {
        'city': city,
        'search_radius': radius*1000,
        'max_distance': max_distance,
        'searched': searched,
        'socket_types_wanted': socket_types_wanted,
        'min_power': min_power,
        'min_rating': min_rating
    }

