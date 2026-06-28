import logging
logger = logging.getLogger(__name__)

from models.schemas import Lodging, ChargingStation
from services.geo import calculate_distance
from data.cache import search_charging_stations
from config import SOCKET_TYPES_LABELS

def find_nearby_stations(lodging: Lodging, max_distance: float) -> list[tuple[ChargingStation, float]]:
    """Interroge l'API ODRÉ autour du logement et retourne les bornes trouvées avec leur distance.

    Args:
        lodging: le logement de référence.
        max_distance: rayon de recherche en kilomètres.
    Returns:
        Liste de tuples (ChargingStation, distance_km).
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

def filter_lodging(results: dict[Lodging, list[tuple[ChargingStation, float]]], min_rating: float) -> dict[Lodging, list[tuple[ChargingStation, float]]]:
    """Filtre les logements selon une note minimale.

    Args:
        results: dictionnaire {Lodging: [(ChargingStation, distance_km), ...]}.
        min_rating: note minimale (0.0 = pas de filtre). Les logements sans note sont exclus si min_rating > 0.
    Returns:
        Dictionnaire filtré ne contenant que les logements dont la note est >= min_rating.
    """
    if min_rating != 0.0:
        return {key: value for key, value in results.items() if key.rating is not None and key.rating >= min_rating}
    return results

def filter_stations(results: dict[Lodging, list[tuple[ChargingStation, float]]], min_power: int, socket_types_wanted: list) -> dict[Lodging, list[tuple[ChargingStation, float]]]:
    """Filtre les bornes de chaque logement selon la puissance minimale et les types de prise souhaités.

    Les logements dont toutes les bornes sont filtrées sont retirés du résultat.

    Args:
        results: dictionnaire {Lodging: [(ChargingStation, distance_km), ...]}.
        min_power: puissance minimale en kW (0 = pas de filtre). Les bornes sans puissance renseignée passent le filtre.
        socket_types_wanted: liste de labels de types de prise (valeurs de SOCKET_TYPES_LABELS). Liste vide = aucune borne retenue.
    Returns:
        Dictionnaire filtré ne contenant que les logements ayant au moins une borne correspondant aux critères.
    """
    if min_power != 0 or len(socket_types_wanted) < len(SOCKET_TYPES_LABELS):
        filtered_results = {}
        for key, value in results.items():
            filtered_stations = []
            for station, distance in value:
                socket_types_available = [SOCKET_TYPES_LABELS[name] for name in station.socket_types_available]
                if any(s in socket_types_available for s in socket_types_wanted) and (station.nominal_power is None or station.nominal_power >= min_power):
                    filtered_stations.append((station, distance))
            if filtered_stations:
                filtered_results[key] = filtered_stations
        return filtered_results
    return results
