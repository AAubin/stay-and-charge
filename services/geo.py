import logging
logger = logging.getLogger(__name__)

from models.schemas import Lodging
from geopy.distance import geodesic


def calculate_distance(coord_1: tuple[float, float], coord_2: tuple[float, float]) -> float:
    """Calcule la distance à vol d'oiseau entre deux points géographiques en kilomètres.

    Args:
        coord_1: (latitude, longitude) du premier point.
        coord_2: (latitude, longitude) du second point.
    Returns:
        Distance en kilomètres.
    """
    return geodesic(coord_1, coord_2).km

def results_are_distant(city_center: tuple[float, float], lodging_list: list[Lodging], threshold_km: int) -> bool:
    """Vérifie si tous les logements sont éloignés du centre-ville de référence.

    Args:
        city_center: (latitude, longitude) du centre-ville géocodé.
        lodging_list: liste de logements à évaluer.
        threshold_km: distance en km au-delà de laquelle un logement est considéré éloigné.
    Returns:
        True si tous les logements sont à plus de threshold_km du centre-ville, False sinon.
    """
    if not lodging_list:
        return False
    distances = [calculate_distance(city_center, (lodging.lat, lodging.lng)) for lodging in lodging_list]
    check = [d > threshold_km for d in distances]
    return all(check)

