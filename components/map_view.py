import logging
logger = logging.getLogger(__name__)

from models.schemas import Lodging, ChargingStation
import dataclasses
import pydeck as pdk
import streamlit as st

def render_map(results: dict[Lodging, list[tuple[ChargingStation, float]]], center: tuple[float, float], zoom: int):
    layers = None
    tooltip = None

    if results:
        lodgings_data = [{**dataclasses.asdict(l), 'nb_nearby_station': len(s)}  for l, s in results.items()]
        unique_stations = {
            station.station_id: station
            for stations in results.values()
            for station, _ in stations
        }
        stations_data = [dataclasses.asdict(s) for s in unique_stations.values()]
        logger.debug(len(stations_data))

        lodging_layer = pdk.Layer(
            type = 'ScatterplotLayer',
            id = 'lodging_layer',
            data = lodgings_data,
            get_position = ['lng', 'lat'],
            get_color = [209, 41, 10],
            get_radius = 50,
            pickable = True
        )

        station_layer = pdk.Layer(
            type = 'ScatterplotLayer',
            id = 'station_layer',
            data = stations_data,
            get_position = ['lng', 'lat'],
            get_color = [10, 17, 209],
            get_radius = 30,
            pickable = True
        )

        layers = [lodging_layer, station_layer]
        tooltip = {"html": "<b>{name}</b><br/>{address}<br/>"}

    view_state = pdk.ViewState(longitude = center[1], latitude = center[0], zoom = zoom)
    deck = pdk.Deck(layers=layers, initial_view_state=view_state, tooltip=tooltip)

    return st.pydeck_chart(deck, on_select="rerun", selection_mode="single-object")

