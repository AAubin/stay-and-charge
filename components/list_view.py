import logging
logger = logging.getLogger(__name__)

from models.schemas import Lodging, ChargingStation
from services.station_finder import create_stations_data
from components.render_details import render_station_details
import streamlit as st

def render_list(results: dict[Lodging, list[tuple[ChargingStation, float]]]):
    """Affiche la vue liste des logements et leurs bornes associées en deux colonnes.

    Colonne gauche : cards cliquables par logement. Colonne droite : bornes du logement
    sélectionné, persistées via st.session_state['selected_lodging'].

    Args:
        results: dictionnaire {Lodging: [(ChargingStation, distance_km), ...]} filtré.
    """
    if results:
        col_lodgings, col_stations = st.columns(2)
        with col_lodgings:
            with st.container(height=900):
                for lodging, stations in results.items():
                    with st.container(border=True):
                        col_info, col_btn, col_ind = st.columns([4, 1, 1], vertical_alignment='center')
                        with col_info:
                            st.markdown(f"**{lodging.name}**")
                            st.caption(f"{lodging.address}")
                            st.caption(f"Note : {lodging.rating} - {len(stations)} stations à proximité")
                            st.page_link(lodging.extern_link, label="Ouvrir dans Google Maps")
                        with col_btn:
                            st.button("Bornes", key=lodging.place_id, on_click=select, args=(lodging,))
                        with col_ind:
                            if st.session_state.get('selected_lodging') == lodging:
                                st.caption("🟢")

        with col_stations:
            if st.session_state.get('selected_lodging'):
                lodging_results = {st.session_state['selected_lodging']: results[st.session_state['selected_lodging']]}
                stations_data = create_stations_data(lodging_results)
                with st.container(height=900):
                    for station in stations_data:
                        with st.container(border=True):
                            render_station_details(station)
    else:
        st.write("Pas de résultats trouvés")

def select(lodging: Lodging) -> None:
    """Callback on_click : enregistre le logement sélectionné dans st.session_state.

    Args:
        lodging: objet Lodging correspondant au bouton cliqué.
    """
    st.session_state['selected_lodging'] = lodging

