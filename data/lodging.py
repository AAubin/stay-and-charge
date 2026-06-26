from config import GOOGLE_PLACES_API_KEY
from services.geo import geocode_city
from models.schemas import Lodging
import requests
import logging
logger = logging.getLogger(__name__)

def search_lodgings(city_name: str, radius: int = 10000) -> list[Lodging]:
    try:
        google_place_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        lat, lng = geocode_city(city_name)
        payload = {
            'location': f"{lat},{lng}",
            'radius': radius,
            'type': "lodging",
            'key': GOOGLE_PLACES_API_KEY,
            'language': "fr"
        }
        logger.debug(f'Nearbysearch requests with location {payload["location"]} with {payload["location"]} meters radius.')
        resp = requests.get(google_place_url, params=payload)
        resp.raise_for_status()
        data = resp.json()
        if data["status"] == "OK":
            logger.debug("Request OK")
            results = []
            for res in data['results']:
                results.append(Lodging.from_api_response(res))
            return results
        elif data["status"] == "ZERO_RESULTS": 
            return []
    except Exception as e:
        logger.error(f"Nearbysearch error: {e}")
        raise RuntimeError(f"Nearbysearch error: {e}") from e
    
    