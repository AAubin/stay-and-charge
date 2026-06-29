import logging
logger = logging.getLogger(__name__)

from models.schemas import Lodging, ChargingStation
from services.geo import calculate_distance
from data.cache import search_charging_stations
from config import SOCKET_TYPES_LABELS
from collections import defaultdict, Counter

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


def count_grouped_stations(stations: list[tuple[ChargingStation, float]]) -> int:
    """Compte le nombre de sites physiques distincts parmi une liste de bornes.

    Deux bornes sont considérées au même site si leurs coordonnées sont identiques
    une fois arrondies à 4 décimales (±11 mètres).

    Args:
        stations: liste de tuples (ChargingStation, distance_km).
    Returns:
        Nombre de sites distincts.
    """
    return len({(round(s.lat, 4), round(s.lng, 4)) for s, _ in stations})


def create_stations_data(results: dict[Lodging, list[tuple[ChargingStation, float]]]) -> list[dict]:
    """Agrège les bornes de tous les logements en groupes par coordonnées arrondies.

    Les stations au même emplacement physique (±0.0001°) sont fusionnées : valeurs les plus
    fréquentes pour les champs texte, maximum pour nb_spots, minimum pour la distance.

    Args:
        results: dictionnaire {Lodging: [(ChargingStation, distance_km), ...]}.
    Returns:
        Liste de dicts agrégés prêts pour l'affichage (carte ou liste).
    """
    groups = defaultdict(list)
    distance_stations = defaultdict(list)
    for stations in results.values():
        for station, distance in stations:
            key = (round(station.lat, 4), round(station.lng, 4))
            groups[key].append(station)
            distance_stations[key].append(distance)
    stations_data = []
    for (key, group), dist in zip(groups.items(), distance_stations.values()):
        stations_data.append({
            'lat': key[0],
            'lng': key[1],
            'name': most_common_or_none(s.name for s in group),
            'store_name': most_common_or_none(s.store_name for s in group),
            'address': most_common_or_none(s.address for s in group if s .address),
            'schedule': most_common_or_none(s.schedule for s in group if s.schedule),
            'nb_spots': max((s.nb_spots for s in group if s.nb_spots), default=None),
            'powers': " / ".join(str(p) for p in sorted({s.nominal_power for s in group if s.nominal_power})),
            'tarification': ", ".join(sorted(set(s.tarification for s in group if s.tarification))),
            'socket_types_available': sorted({t for s in group for t in s.socket_types_available}),
            'distance': min(dist, default=None),
            'icon': 'station'
        })
    return stations_data

def most_common_or_none(values):
    """Retourne la valeur la plus fréquente d'un itérable, ou None si vide.

    Args:
        values: itérable de valeurs.
    Returns:
        Valeur la plus fréquente, ou None si l'itérable est vide.
    """
    counter = Counter(values).most_common(1)
    if counter:
        return counter[0][0]
    return None

