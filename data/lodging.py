import logging
logger = logging.getLogger(__name__)

from config import GOOGLE_PLACES_API_KEY, GOOGLE_PLACES_URL
from models.schemas import Lodging
import requests

def search_lodgings(search_coord: tuple[float, float], radius: int) -> list[Lodging]:
    """Recherche des logements via Google Places Nearby Search autour des coordonnées données.

    Args:
        search_coord: (latitude, longitude) du centre de recherche.
        radius: rayon de recherche en mètres (max 50 000).
    Returns:
        liste de Lodging triée par pertinence Google.
    Raises:
        RuntimeError: en cas d'erreur API ou réseau.
    """
    try:
        lat, lng = search_coord
        payload = {
            'location': f"{lat},{lng}",
            'radius': radius,
            'type': "lodging",
            'key': GOOGLE_PLACES_API_KEY,
            'language': "fr"
        }

        logger.debug(f'Nearbysearch requests with location {payload["location"]} with {payload["location"]} meters radius.')
        resp = requests.get(GOOGLE_PLACES_URL, params=payload)

        resp.raise_for_status()

        data = resp.json()
        if data["status"] == "OK":
            logger.debug("Request OK")
            return [Lodging.from_api_response(res) for res in data['results']]
        elif data["status"] == "ZERO_RESULTS":
            logger.debug("No results") 
            return []
        
    except Exception as e:
        logger.error(f"Nearbysearch error: {e}")
        raise RuntimeError(f"Nearbysearch error: {e}") from e
    
    