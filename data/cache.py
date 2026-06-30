from streamlit import cache_data
from data.lodging import search_lodgings as _search_lodgings
from data.charging_stations import search_charging_stations as _search_charging_stations
from data.geocoding import geocode_location as _geocode_location
from models.schemas import Lodging, ChargingStation

@cache_data(ttl=3600)
def geocode_location(city_name: str, country_codes:str = 'FR') -> tuple[float, float]:
    return _geocode_location(city_name, country_codes=country_codes)

@cache_data(ttl=3600)
def search_lodgings(search_coord: tuple[float, float], radius: int = 50000) -> list[Lodging]:
    return _search_lodgings(search_coord, radius)

@cache_data(ttl=3600)
def search_charging_stations(search_coord: tuple[float, float], radius: int = 50000) -> list[ChargingStation]:
    return _search_charging_stations(search_coord, radius)
