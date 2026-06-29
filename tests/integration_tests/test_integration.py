import pytest
from config import GOOGLE_PLACES_API_KEY
from data.geocoding import geocode_location
from data.lodging import search_lodgings
from data.charging_stations import search_charging_stations

@pytest.mark.integration
def test_geocode_location():
    coord_bordeaux = geocode_location('Bordeaux')
    coord_st_brevin = geocode_location(44250)
    assert coord_bordeaux[0] == pytest.approx(44.8378, abs=0.01)
    assert coord_bordeaux[1] == pytest.approx(-0.5792, abs=0.01)
    assert coord_st_brevin[0] == pytest.approx(47.2377, abs=0.01)
    assert coord_st_brevin[1] == pytest.approx(-2.1521, abs=0.01)

@pytest.mark.integration
def test_search_lodgings_bordeaux():
    coord_bordeaux = geocode_location('Bordeaux')
    lodgings = search_lodgings(coord_bordeaux, 3000)
    assert len(lodgings) > 0

@pytest.mark.integration
def test_search_charging_stations_bordeaux():
    if not GOOGLE_PLACES_API_KEY:
        pytest.skip("GOOGLE_PLACES_API_KEY missing")
    coord_bordeaux = geocode_location('Bordeaux')
    stations = search_charging_stations(coord_bordeaux, 3000)
    assert len(stations) > 0
