import logging
logger = logging.getLogger(__name__)

from config import SOCKET_TYPES_LABELS
import streamlit as st

@st.dialog('Détails:')
def show_details(point: dict) -> None:
    """Affiche le panneau détail (st.dialog) pour le point cliqué sur la carte.

    Args:
        point: dictionnaire issu de event.selection.objects, avec les clés
               'lodging_layer' ou 'station_layer' selon le point cliqué.
    """
    if 'lodging_layer' in point.keys():
        lodging_details(point['lodging_layer'][0])
    if 'station_layer' in point.keys():
        station_details(point['station_layer'][0])
    

def lodging_details(details: dict) -> None:
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

def station_details(details: dict) -> None:
    """Affiche les informations détaillées d'un groupe de bornes dans le panneau.

    Args:
        details: dict agrégé de la borne issu de stations_data (champs : name, store_name,
                 address, powers, nb_spots, socket_types_available, schedule, tarification, distance).
    """
    st.subheader(f"{details['store_name']} - {details['name']}")
    st.write(details['address'])
    if details['powers']:
        st.write(f"Puissances disponibles: {details['powers']}")
    if details['nb_spots']:
        st.write(f"{details['nb_spots']} place(s).")
    if details['socket_types_available']:
        socket_labels = [SOCKET_TYPES_LABELS[code] for code in details['socket_types_available']]
        socket_str = ', '.join(socket_labels)
        st.write(f"Types de prises: {socket_str}")
    if details['schedule']:
        st.write(f"Horaires: {details['schedule']}")
    if details['tarification']:
        st.write('Tarification: ')
        st.write(details['tarification'])
    if details['distance']:
        st.write(f"Distance du logement le plus proche: {round(details['distance'], 2)} km")
