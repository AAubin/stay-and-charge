import logging
from logging_manager import setup_logging
setup_logging()
logger = logging.getLogger(__name__)

from data.cache import geocode_city, search_lodgings, search_charging_stations
from services.geo import calculate_distance
from services.station_finder import find_all_nearby_stations

test_city = 'Bordeaux'
test_coord = geocode_city(test_city)
logger.info(f"Coordonnées de la ville test: {test_coord}")

test_lodgings = search_lodgings(test_coord)
nb_lodgings = len(test_lodgings)
logger.info(f"Nb de logements trouvés: {nb_lodgings}")
lodging = None
if nb_lodgings > 0:
    lodging = test_lodgings[0]
    logger.info(f"Exemple de logement: {lodging}")

test_stations = search_charging_stations(test_coord)
nb_stations = len(test_stations)
logger.info(f"Nb de stations trouvées {nb_stations}")
station = None
if nb_stations > 0:
    station = test_stations[0]
    logger.info(f"Exemple de station: {station}")

if lodging and station:
    coord_lodg = (lodging.lat, lodging.lng)
    coord_stat = (station.lat, station.lng)
    test_dist = calculate_distance(coord_lodg, coord_stat)
    logger.info(f"Exemple de cacul de distance {test_dist}")

test_lodging_to_match = test_lodgings[:3]
results = find_all_nearby_stations(test_lodging_to_match, test_stations, 5000)
for lodging, stations in list(results.items())[:1]:
    logger.info(f"Exemple: {lodging.name} → {len(stations)} bornes")



