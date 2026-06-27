import logging
logger = logging.getLogger(__name__)

from models.schemas import Lodging, ChargingStation
from services.geo import calculate_distance

def find_nearby_stations(lodging: Lodging, stations_list: list[ChargingStation], max_distance: float) -> list[tuple[ChargingStation, float]]:
    """Retourne les bornes de recharge situées dans un rayon donné autour d'un logement.

    Args:
        lodging: le logement de référence.
        stations_list: liste de toutes les bornes à filtrer.
        max_distance: rayon maximum en mètres.
    Returns:
        Liste de tuples (ChargingStation, distance_km) pour les bornes dans le rayon,
        sans ordre garanti.
    """
    close_station = []
    lodging_coord = (lodging.lat, lodging.lng)

    logger.debug(f"nombre de stations à associer: {len(stations_list)}")
    for station in stations_list:
        station_coord = (station.lat, station.lng)
        distance = calculate_distance(lodging_coord, station_coord)
        if distance <= max_distance:
            close_station.append((station, distance))
    logger.debug(f"Nombre de stations trouvées: {len(close_station)}")
    if close_station:
        close_station.sort(key=lambda x: x[1])
        logger.debug(f"Station la plus proche: {close_station[0]}")
    return close_station

def find_all_nearby_stations(lodgings_list: list[Lodging], stations_list: list[ChargingStation], max_distance: float) -> dict[Lodging, list[tuple[ChargingStation, float]]]:
    """Associe chaque logement à ses bornes de recharge proches.

    Args:
        lodgings_list: liste des logements à traiter.
        stations_list: liste de toutes les bornes candidates.
        max_distance: rayon maximum en mètres.
    Returns:
        Dictionnaire {Lodging: [(ChargingStation, distance_km), ...]} pour chaque logement.
        Un logement sans borne proche est associé à une liste vide.
    """
    results = {}
    for lodging in lodgings_list:
        results[lodging] = find_nearby_stations(lodging, stations_list, max_distance)
    logger.debug("Logements associées aux bornes")
    return results
