from streamlit import cache_data
from data.lodging import search_lodgings as _search_lodgings
from models.schemas import Lodging

@cache_data(ttl=3600)
def search_lodgings(city_name: str, radius: int = 10000) -> list[Lodging]:
    return _search_lodgings(city_name, radius)

