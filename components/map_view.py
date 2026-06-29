import logging
logger = logging.getLogger(__name__)

from models.schemas import Lodging, ChargingStation
from config import ICON_ATLAS, ICON_MAPPING, COLOR_HOTEL, COLOR_STATION, COLOR_CIRCLE
from services.station_finder import create_stations_data, count_grouped_stations
import dataclasses
import pydeck as pdk
import streamlit as st

def render_map(results: dict[Lodging, list[tuple[ChargingStation, float]]], center: tuple[float, float], zoom: int, radius: int)-> st.delta_generator.DeltaGenerator:
    """Construit et affiche la carte pydeck avec les layers logements et bornes.

    Args:
        results: dictionnaire {Lodging: [(ChargingStation, distance_km), ...]} issu de find_all_nearby_stations.
        center: (latitude, longitude) du centre initial de la carte.
        zoom: niveau de zoom initial (5 = France entière, 12 = ville).
        radius: rayon du cercle affiché
    Returns:
        Evénement de sélection pydeck (contient les données du point cliqué via .selection.objects).
    """
    layers = None
    tooltip = None

    if results:
        lodgings_data = [{**dataclasses.asdict(l), 'nb_nearby_station': count_grouped_stations(s), 'icon': 'hotel'}  for l, s in results.items()]
        logger.debug(f"{len(lodgings_data)} logements trouvées")

        stations_data = create_stations_data(results)
        logger.debug(f"{len(stations_data)} stations trouvées")

        lodging_layer = pdk.Layer(
            type = 'IconLayer',
            id = 'lodging_layer',
            data = lodgings_data,
            get_position = ['lng', 'lat'],
            get_icon = 'icon',
            get_size = 4,
            size_scale = 3,
            icon_atlas = ICON_ATLAS,
            icon_mapping = ICON_MAPPING,
            get_color = COLOR_HOTEL,
            pickable = True
        )

        station_layer = pdk.Layer(
            type = 'IconLayer',
            id = 'station_layer',
            data = stations_data,
            get_position = ['lng', 'lat'],
            get_icon = 'icon',
            get_size = 4,
            size_scale = 3,
            icon_atlas = ICON_ATLAS,
            icon_mapping = ICON_MAPPING,
            get_color = COLOR_STATION,
            pickable = True
        )

        circle = pdk.Layer(
            type = 'ScatterplotLayer',
            data = [{'lat': center[0], 'lng': center[1], 'radius': radius}],
            get_position = ['lng', 'lat'],
            get_radius = 'radius',
            get_fill_color = COLOR_CIRCLE['fill'],
            get_line_color = COLOR_CIRCLE['line'],
            line_width_min_pixels = 1,
            stroked = True,
            filled = True,
            pickable = False
        )

        layers = [lodging_layer, station_layer, circle]
        tooltip = {"html": "<b>{name}</b><br/>{address}<br/>"}

    view_state = pdk.ViewState(longitude = center[1], latitude = center[0], zoom = zoom)
    deck = pdk.Deck(layers=layers, initial_view_state=view_state, tooltip=tooltip)

    return st.pydeck_chart(deck, on_select="rerun", selection_mode="single-object")
