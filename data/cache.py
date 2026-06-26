from streamlit import cache_data
from data.lodging import search_lodgings as _search_lodgings
from data.charging_stations import search_charging_stations as _search_charging_stations
from services.geo import geocode_city as _geocode_city
from models.schemas import Lodging, ChargingStation

@cache_data(ttl=3600)
def geocode_city(city_name: str) -> tuple[float, float]:
    return _geocode_city(city_name)

@cache_data(ttl=3600)
def search_lodgings(search_coord: tuple[float, float], radius: int = 50000) -> list[Lodging]:
    return _search_lodgings(search_coord, radius)

@cache_data(ttl=3600)
def search_charging_stations(search_coord: tuple[float, float], radius: int = 50000) -> list[ChargingStation]:
    return _search_charging_stations(search_coord, radius)
