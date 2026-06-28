import logging
logger = logging.getLogger(__name__)

from config import SOCKET_TYPES_LABELS
import streamlit as st

@st.dialog("Détails")
def render_detail_panels(point: dict) -> None:
    """Affiche le panneau détail (st.dialog) pour le point cliqué sur la carte.

    Args:
        point: dictionnaire issu de event.selection.objects, avec les clés
               'lodging_layer' ou 'station_layer' selon le point cliqué.
    """
    if 'lodging_layer' in point.keys():
        render_lodging_details(point['lodging_layer'][0])
    if 'station_layer' in point.keys():
        render_station_details(point['station_layer'][0])
    

def render_lodging_details(details: dict) -> None:
    """Affiche les informations détaillées d'un logement dans le panneau.

    Args:
        details: dict du logement issu de lodgings_data (champs : name, address,
                 nb_nearby_station, extern_link, rating, user_rating_totals).
    """
    st.subheader(details['name'])
    st.write(details['address'])
    st.write(f"{details['nb_nearby_station']} stations à proximité")
    st.page_link(details['extern_link'], label="Ouvrir dans Google Maps", icon="↗️")
    if details['rating']:
        st.write(f"Note moyenne: {details['rating']}")
    if details['user_rating_totals']:
        st.write(f"Nombre de votants: {details['user_rating_totals']}")

def render_station_details(station: dict):
    """Affiche les informations détaillées d'un groupe de bornes dans le panneau.

    Args:
        station: dict agrégé de la borne issu de stations_data (champs : name, store_name,
                 address, powers, nb_spots, socket_types_available, schedule, tarification, distance).
    """
    st.markdown(f"**{station['store_name']} - {station['name']}**")
    st.caption(station['address'])
    if station['powers']:
        st.caption(f"Puissances disponibles: {station['powers']}")
    if station['nb_spots']:
        st.caption(f"{station['nb_spots']} place(s).")
    if station['socket_types_available']:
        socket_labels = [SOCKET_TYPES_LABELS[code] for code in station['socket_types_available']]
        socket_str = ', '.join(socket_labels)
        st.caption(f"Types de prises: {socket_str}")
    if station['schedule']:
        st.caption(f"Horaires: {station['schedule']}")
    if station['tarification']:
        st.caption('Tarification: ')
        st.caption(station['tarification'])
    if station['distance']:
        st.caption(f"Distance du logement le plus proche: {round(station['distance'], 2)} km")