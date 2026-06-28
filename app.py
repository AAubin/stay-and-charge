import logging
from logging_manager import setup_logging
setup_logging()
logger = logging.getLogger(__name__)

import streamlit as st
from config import DEFAULT_CENTER, DEFAULT_ZOOM_CITY, DEFAULT_ZOOM_FRANCE
from data.cache import search_lodgings, geocode_location
from services.station_finder import find_all_nearby_stations
from components.map_view import render_map
from components.filters import render_filters
from components.detail_panel import show_details

st.set_page_config(layout='wide')
st.title("Stay & Charge")
st.markdown("Trouvez un logement avec une borne de recharge à proximité")

filters = render_filters()

update_map = filters['searched']

if update_map:
    city = filters['city']
    st.session_state['center'] = geocode_location(city)
    lodgings = search_lodgings(st.session_state['center'], radius=filters['search_radius'])
    st.session_state['results'] = find_all_nearby_stations(lodgings, max_distance=filters['max_distance'])


results = st.session_state.get('results', {})
center = st.session_state.get('center', DEFAULT_CENTER)
if 'zoom' not in st.session_state:
    zoom = DEFAULT_ZOOM_FRANCE
    st.session_state['zoom'] = DEFAULT_ZOOM_CITY
else:
    zoom = st.session_state['zoom']

event = render_map(results, center, zoom)
if event.selection.objects:
    show_details(event.selection.objects)
