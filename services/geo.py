from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import logging
logger = logging.getLogger(__name__)

geolocator = Nominatim(user_agent="stay-and-charge")

def geocode_city(city_name: str) -> tuple[float, float]:
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
    # A implémenter plus tard
    pass

