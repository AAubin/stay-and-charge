import logging
logger = logging.getLogger(__name__)

import streamlit as st

@st.dialog('Détails:')
def show_details(point: dict):
    if 'lodging_layer' in point.keys():
        lodging_details(point['lodging_layer'][0])
    if 'station_layer' in point.keys():
        station_details(point['station_layer'][0])
    

def lodging_details(details: dict):
    st.subheader(details['name'])
    st.write(details['address'])
    st.write(f"{details['nb_nearby_station']} stations à proximité")
    st.page_link(details['extern_link'], label="Ouvrir dans Google Maps", icon="↗️")
    if details['rating']:
        st.write(f"Note moyenne: {details['rating']}")
    if details['user_rating_totals']:
        st.write(f"Nombre de votants: {details['user_rating_totals']}")

def station_details(details: dict):
    st.subheader(f"{details['store_name']} - {details['name']}")
    st.write(details['address'])
    if details['powers']:
        st.write(f"Puissances disponibles: {details['powers']}")
    if details['nb_spots']:
        st.write(f"{details['nb_spots']} place(s).")
    if details['socket_types_available']:
        socket_str = ', '.join(details['socket_types_available']).replace('_', ' ')
        st.write(f"Types de prises: {socket_str}")
    if details['schedule']:
        st.write(f"Horaires: {details['schedule']}")
    if details['tarification']:
        st.write('Tarification: ')
        st.write(details['tarification'])
