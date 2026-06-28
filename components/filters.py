import logging
logger = logging.getLogger(__name__)

import streamlit as st

def render_filters() -> dict:
    """Affiche les widgets de filtres dans la sidebar et retourne les valeurs saisies.

    Returns:
        Dictionnaire avec les clés : city (str), search_radius (int, en mètres),
        max_distance (int, en km), searched (bool).
    """
    with st.sidebar:
        city = st.text_input(label='Ville ou code postal')
        radius = st.number_input(label='Rayon de recherche (km)', min_value=0, value=30)
        max_distance = st.selectbox(label='Distance max des bornes de recharge (km)', options=[1, 5, 10, 15, 20])
        searched = st.button(label='Recherche')
    return {
        'city': city,
        'search_radius': radius*1000,
        'max_distance': max_distance,
        'searched': searched
    }

