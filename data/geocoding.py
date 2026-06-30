import logging
logger = logging.getLogger(__name__)

from config import GOOGLE_GEOCODE_URL, GOOGLE_PLACES_API_KEY
import requests

def geocode_location(city: str|int, country_codes: str = 'FR') -> tuple[float, float]:
    """Retourne les coordonnées d'une ville via google.

    Args:
        city: nom ou code postal de la ville à géocoder.
    Returns:
        (latitude, longitude) en degrés décimaux.
    Raises:
        ValueError: si la ville n'est pas trouvée.
        RuntimeError: en cas d'erreur réseau ou de timeout.
    """
    try:
        logger.info("Start geocoding")
        payload = {
            'address': city,
            'key': GOOGLE_PLACES_API_KEY,
            'language': 'fr',
            'components': f'country:{country_codes.upper()}'
        }
        logger.debug("Appel api google geocode")
        resp = requests.get(GOOGLE_GEOCODE_URL, params=payload)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        logger.error(f"Geocoding error: {e}")
        raise RuntimeError(f"Geocoding error: {e}") from e

    if data['status'] == 'OK':
        lat = data['results'][0]['geometry']['location']['lat']
        lng = data['results'][0]['geometry']['location']['lng']
        logger.info(f"Coordinates found for {city}: {lat}, {lng}")
        return (lat, lng)
    if data['status'] == 'ZERO_RESULTS':
        logger.warning("City not found")
        raise ValueError("City not found")
    raise RuntimeError(f"Geocoding error: {data['status']}")

