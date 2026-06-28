import logging
logger = logging.getLogger(__name__)

from models.schemas import Lodging, ChargingStation
from config import ICON_ATLAS, ICON_MAPPING, COLOR_HOTEL, COLOR_STATION
import dataclasses
from collections import defaultdict, Counter
import pydeck as pdk
import streamlit as st

def render_map(results: dict[Lodging, list[tuple[ChargingStation, float]]], center: tuple[float, float], zoom: int):
    layers = None
    tooltip = None

    if results:
        lodgings_data = [{**dataclasses.asdict(l), 'nb_nearby_station': len(s), 'icon': 'hotel'}  for l, s in results.items()]

        groups = defaultdict(list)
        for stations in results.values():
            for station, _ in stations:
                key = (round(station.lat, 4), round(station.lng, 4))
                groups[key].append(station)
        stations_data = []
        for key, group in groups.items():
            stations_data.append({
                'lat': key[0],
                'lng': key[1],
                'name': Counter(s.name for s in group).most_common(1)[0][0],
                'store_name': Counter(s.store_name for s in group).most_common(1)[0][0],
                'address': Counter(s.address for s in group if s .address).most_common(1)[0][0],
                'schedule': Counter(s.schedule for s in group if s.schedule).most_common(1)[0][0],
                'nb_spots': max(s.nb_spots for s in group if s.nb_spots),
                'powers': " / ".join(str(p) for p in sorted({s.nominal_power for s in group if s.nominal_power})),
                'tarification': ", ".join(set(s.tarification for s in group if s.tarification)),
                'socket_types_available': list({t for s in group for t in s.socket_types_available}),
                'icon': 'station'
            })
        
        logger.debug(len(stations_data))

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

        layers = [lodging_layer, station_layer]
        tooltip = {"html": "<b>{name}</b><br/>{address}<br/>"}

    view_state = pdk.ViewState(longitude = center[1], latitude = center[0], zoom = zoom)
    deck = pdk.Deck(layers=layers, initial_view_state=view_state, tooltip=tooltip)

    return st.pydeck_chart(deck, on_select="rerun", selection_mode="single-object")

