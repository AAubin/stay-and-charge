import logging
from logging_manager import setup_logging
setup_logging()
logger = logging.getLogger(__name__)

from config import DEFAULT_CENTER, DEFAULT_ZOOM_CITY, DEFAULT_ZOOM_FRANCE, THRESHOLD_KM
import streamlit as st
from data.cache import search_lodgings, geocode_location
from services.station_finder import find_all_nearby_stations, filter_lodging, filter_stations
from services.geo import results_are_distant
from components.map_view import render_map
from components.list_view import render_list
from components.filters import render_filters
from components.render_details import render_detail_panels
from components.footer import render_footer

st.set_page_config(layout='wide', initial_sidebar_state='expanded')
st.title("Stay & Charge")
st.markdown("Trouvez un logement avec une borne de recharge à proximité")
map_tab, list_tab = st.tabs(['Carte', 'Liste'])

filters = render_filters()

has_query_params = bool(st.query_params.get('city'))
first_load = 'results' not in st.session_state
should_search = filters['searched'] or (has_query_params and first_load)

if should_search:
    try:
        with st.spinner("Recherche en cours..."):
            city = filters['city']
            center = geocode_location(city)
            lodgings = search_lodgings(center, radius=filters['search_radius'])
            if not lodgings:
                st.info("Aucun logement trouvé.")
                st.stop()
            if results_are_distant(center, lodgings, THRESHOLD_KM):
                st.info('Les résultats semblent éloignés du centre de la recherche, naviguer sur la carte ou réduisez le rayon de recherche')
            results = find_all_nearby_stations(lodgings, max_distance=filters['max_distance'])
    except ValueError:
        st.error("Ville introuvable, vérifiez l'orthographe ou le code postal")
        st.stop()
    except Exception as e:
        st.error(f"Erreur api: {e}")
        st.stop()

    st.session_state['center'] = center
    st.session_state['results'] = results

    st.query_params['city'] = city
    st.query_params['radius'] = filters['search_radius']//1000
    st.query_params['max_distance'] = filters['max_distance']
    st.query_params['min_rating'] = filters['min_rating']
    st.query_params['socket_types_wanted'] = filters['socket_types_wanted']
    st.query_params['min_power'] = filters['min_power']

results = filter_stations(filter_lodging(st.session_state.get('results', {}), filters['min_rating']), filters['min_power'], filters['socket_types_wanted'])

with map_tab:
    center = st.session_state.get('center', DEFAULT_CENTER)
    zoom = DEFAULT_ZOOM_CITY if results else DEFAULT_ZOOM_FRANCE
    event = render_map(results, center, zoom, filters['search_radius'])
    st.write(event.selection.objects)
    if event.selection.objects:
        render_detail_panels(event.selection.objects)

with list_tab:
    render_list(results)

render_footer()
