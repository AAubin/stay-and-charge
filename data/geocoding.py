import logging
logger = logging.getLogger(__name__)

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

geolocator = Nominatim(user_agent="stay-and-charge", timeout=10)

def geocode_location(city: str|int, country_codes: str = 'fr') -> tuple[float, float]:
    """Retourne les coordonnées d'une ville via Nominatim.

    Args:
        city: nom ou code postal de la ville à géocoder.
    Returns:
        (latitude, longitude) en degrés décimaux.
    Raises:
        ValueError: si la ville n'est pas trouvée.
        RuntimeError: en cas d'erreur réseau ou de timeout.
    """
    try:
        location = geolocator.geocode(city, country_codes=country_codes)
        if location:
            logger.debug(f"Coordinates found for {city}: {location.latitude}, {location.longitude}")
            return (location.latitude, location.longitude)
        else:
            logger.warning("City not found")
            raise ValueError("City not found")
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        logger.error(f"Geocoding error: {e}")
        raise RuntimeError(f"Geocoding error: {e}") from e
    
    