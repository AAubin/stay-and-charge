import logging
logger = logging.getLogger(__name__)

import streamlit as st
from config import SOCKET_TYPES_LABELS, POWER_BOUNDS

def render_filters() -> dict:
    """Affiche les widgets de filtres dans la sidebar et retourne les valeurs saisies.

    Returns:
        Dictionnaire avec les clés : city (str), search_radius (int, en mètres),
        max_distance (float, en mètres), searched (bool), min_rating (float),
        socket_types_wanted (list[str], labels lisibles), min_power (int, en kW).
    """
    with st.sidebar:
        city = st.text_input(label='Ville ou code postal', value=st.query_params.get('city', ''))
        radius = st.number_input(label='Rayon de recherche (km)', min_value=0, max_value=50, value=int(st.query_params.get('radius', 10)), help="max 50 km")
        max_distance = st.slider(label='Distance max des bornes de recharge (km)', min_value=0.1, max_value=20.0, step=0.1, value=float(st.query_params.get('max_distance', 0.1)), format="%0.1f")
        searched = st.button(label='Recherche')
        st.divider()
        min_rating = st.slider(label="Note minimal du logement:", min_value=0.0, max_value=5.0, step=0.1, value=float(st.query_params.get('min_rating', 0.0)), format="%0.1f")
        st.divider()
        default_sockets = st.query_params.get_all('socket_types_wanted') or list(SOCKET_TYPES_LABELS.values())
        socket_types_wanted = st.multiselect(label="Types de prise", options=SOCKET_TYPES_LABELS.values(), default=default_sockets)
        min_power = st.slider(label="Puissance minimale (kW)", min_value=POWER_BOUNDS[0], max_value=POWER_BOUNDS[1], step=10, value=int(st.query_params.get('min_power', 0)))

    return {
        'city': city,
        'search_radius': radius*1000,
        'max_distance': max_distance*1000,
        'searched': searched,
        'socket_types_wanted': socket_types_wanted,
        'min_power': min_power,
        'min_rating': min_rating
    }

