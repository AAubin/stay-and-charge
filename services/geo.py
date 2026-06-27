import logging
logger = logging.getLogger(__name__)

from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

geolocator = Nominatim(user_agent="stay-and-charge")

def geocode_city(city_name: str) -> tuple[float, float]:
    """Retourne les coordonnées d'une ville via Nominatim.

    Args:
        city_name: nom de la ville à géocoder.
    Returns:
        (latitude, longitude) en degrés décimaux.
    Raises:
        ValueError: si la ville n'est pas trouvée.
        RuntimeError: en cas d'erreur réseau ou de timeout.
    """
    try:
        location = geolocator.geocode(city_name)
        if location:
            logger.debug(f"Coordinates found for {city_name}: {location.latitude}, {location.longitude}")
            return (location.latitude, location.longitude)
        else:
            logger.warning("City not found")
            raise ValueError("City not found")
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        logger.error(f"Geocoding error: {e}")
        raise RuntimeError(f"Geocoding error: {e}") from e



def zoom_to_radius(zoom: int, lat: float) -> float:
    """Convertit un niveau de zoom pydeck en rayon de recherche en mètres.

    Args:
        zoom: niveau de zoom pydeck (plus le zoom est élevé, plus la zone est petite).
        lat: latitude du centre, nécessaire pour corriger la distorsion en longitude.
    Returns:
        rayon approximatif en mètres correspondant à la zone visible.
    """
    # A implémenter plus tard
    pass

def calculate_distance (coord_1: tuple[float, float], coord_2: tuple[float, float]) -> float:
    return geodesic(coord_1, coord_2).m
