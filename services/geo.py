import logging
logger = logging.getLogger(__name__)

from models.schemas import Lodging
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

geolocator = Nominatim(user_agent="stay-and-charge")

def geocode_location(city_name: str) -> tuple[float, float]:
    """Retourne les coordonnées d'une ville via Nominatim.

    Args:
        city_name: nom ou code postal de la ville à géocoder.
    Returns:
        (latitude, longitude) en degrés décimaux.
    Raises:
        ValueError: si la ville n'est pas trouvée.
        RuntimeError: en cas d'erreur réseau ou de timeout.
    """
    try:
        location = geolocator.geocode(city_name, country_codes="fr")
        if location:
            logger.debug(f"Coordinates found for {city_name}: {location.latitude}, {location.longitude}")
            return (location.latitude, location.longitude)
        else:
            logger.warning("City not found")
            raise ValueError("City not found")
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        logger.error(f"Geocoding error: {e}")
        raise RuntimeError(f"Geocoding error: {e}") from e

def calculate_distance(coord_1: tuple[float, float], coord_2: tuple[float, float]) -> float:
    """Calcule la distance à vol d'oiseau entre deux points géographiques.

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

