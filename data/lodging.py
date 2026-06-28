import logging
logger = logging.getLogger(__name__)

from config import GOOGLE_PLACES_API_KEY, GOOGLE_PLACES_URL
from models.schemas import Lodging
import requests
import time

def search_lodgings(search_coord: tuple[float, float], radius: int) -> list[Lodging]:
    """Recherche des logements via Google Places Nearby Search autour des coordonnées données.

    Pagine automatiquement jusqu'à 3 pages (max 60 résultats) via next_page_token.

    Args:
        search_coord: (latitude, longitude) du centre de recherche.
        radius: rayon de recherche en mètres (max 50 000).
    Returns:
        liste de Lodging triée par pertinence Google (jusqu'à 60 résultats).
    Raises:
        RuntimeError: en cas d'erreur API ou réseau.
    """
    try:
        lat, lng = search_coord
        total_lodging = []
        page_counter = 0
        token_present = False
        token = None
        new_search = True

        while new_search:
            new_search = False
            payload = {
                'location': f"{lat},{lng}",
                'radius': radius,
                'type': "lodging",
                'key': GOOGLE_PLACES_API_KEY,
                'language': "fr"
            }
            if token_present:
                payload['pagetoken'] = token
                token_present = False
            logger.debug(f'Nearbysearch requests n°{page_counter+1} with location {payload["location"]} with {payload["radius"]} meters radius.')
            resp = requests.get(GOOGLE_PLACES_URL, params=payload)
            resp.raise_for_status()
            data = resp.json()

            if data["status"] == "OK":
                logger.debug("Request OK")
                lodging_found = [Lodging.from_api_response(res) for res in data['results']]
                total_lodging.extend(lodging_found)
            elif data["status"] == "ZERO_RESULTS":
                logger.debug("No results")

            page_counter += 1
            if 'next_page_token' in data and page_counter < 3:
                token = data['next_page_token']
                time.sleep(2)
                token_present = True
                new_search = True
            
        logger.debug(f"Nb de logements: {len(total_lodging)}")
        return total_lodging
    
    except Exception as e:
        logger.error(f"Nearbysearch error: {e}")
        raise RuntimeError(f"Nearbysearch error: {e}") from e
    
    