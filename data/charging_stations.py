from config import OPENDATASOFT_URL, FIELDS_SELECT
from models.schemas import ChargingStation
from math import cos, radians
import requests
import logging
logger = logging.getLogger(__name__)

def search_charging_stations(search_coord: tuple[float, float], radius: int) -> list[ChargingStation]:
    try:
        lat, lng = search_coord
        lat_delta = radius / 111000  # 1 degré ≈ 111 km
        lng_delta = radius / (111000 * cos(radians(lat)))
        where = (
            f"consolidated_latitude > {lat - lat_delta} AND "
            f"consolidated_latitude < {lat + lat_delta} AND "
            f"consolidated_longitude > {lng - lng_delta} AND "
            f"consolidated_longitude < {lng + lng_delta}"
        )

        payload = {
            'where': where,
            'select': FIELDS_SELECT,
            'limit': 100,
            'order_by': f"distance(coordonneesxy, GEOM'POINT({lng} {lat})') ASC, puissance_nominale DESC"
        }

        logger.debug(f'Opendatasoft requests with location {search_coord} with {radius} meters radius.')
        resp = requests.get(OPENDATASOFT_URL, params=payload)

        resp.raise_for_status()

        logger.debug("Request OK")
        data = resp.json()
        logger.debug(f"total_count: {data.get('total_count')}")
        logger.debug(data['results'][0])
        return [ChargingStation.from_api_response(res) for res in data['results']]

    except Exception as e:
        logger.error(f"Opendatasoft error: {e}")
        raise RuntimeError(f"Opendatasoft error: {e}") from e
    
    