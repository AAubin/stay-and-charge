import logging
logger = logging.getLogger(__name__)

from models.schemas import Lodging, ChargingStation
from services.geo import calculate_distance
from data.cache import search_charging_stations

def find_nearby_stations(lodging: Lodging, max_distance: float) -> list[tuple[ChargingStation, float]]:
    """Interroge l'API ODRÉ autour du logement et retourne les bornes trouvées avec leur distance.

    Args:
        lodging: le logement de référence.
        max_distance: rayon de recherche en kilomètres.
    Returns:
        Liste de tuples (ChargingStation, distance_km) triés par distance croissante.
    """
    nearby_station = []
    lodging_coord = (lodging.lat, lodging.lng)
    radius = max_distance*1000
    stations_list = search_charging_stations(lodging_coord, radius=radius)
    for station in stations_list:
        station_coord = (station.lat, station.lng)
        distance = calculate_distance(lodging_coord, station_coord)
        nearby_station.append((station, distance))
    logger.debug(f"Nombre de stations trouvées: {len(nearby_station)}")
    return nearby_station

def find_all_nearby_stations(lodgings_list: list[Lodging], max_distance: float) -> dict[Lodging, list[tuple[ChargingStation, float]]]:
    """Associe chaque logement à ses bornes de recharge proches via l'API ODRÉ.

    Args:
        lodgings_list: liste des logements à traiter.
        max_distance: rayon de recherche en kilomètres.
    Returns:
        Dictionnaire {Lodging: [(ChargingStation, distance_km), ...]} pour chaque logement.
        Un logement sans borne proche est associé à une liste vide.
    """
    results = {}
    for lodging in lodgings_list:
        results[lodging] = find_nearby_stations(lodging, max_distance)
    logger.debug("Logements associées aux bornes")
    return results
