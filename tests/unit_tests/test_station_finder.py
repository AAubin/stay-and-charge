from unittest.mock import patch, MagicMock
import pytest
from services.station_finder import find_nearby_stations, find_all_nearby_stations, filter_lodging, filter_stations, count_grouped_stations, create_stations_data, most_common_or_none
from models.schemas import ChargingStation, Lodging
from config import SOCKET_TYPES_LABELS
@pytest.fixture
def lodging_1(google_place_response_1):
    return Lodging.from_api_response(google_place_response_1)

@pytest.fixture
def lodging_2(google_place_response_2):
    return Lodging.from_api_response(google_place_response_2)

@pytest.fixture
def station_1(odre_response_1):
    return ChargingStation.from_api_response(odre_response_1)

@pytest.fixture
def station_2(odre_response_2):
    return ChargingStation.from_api_response(odre_response_2)

@pytest.fixture
def station_4(odre_response_4):
    return ChargingStation.from_api_response(odre_response_4)

@pytest.fixture
def results(lodging_1, lodging_2, station_1, station_2, station_4):
    return {
        lodging_1: [(station_1, 5), (station_2, 10), (station_4, 15)],
        lodging_2: [(station_1, 5)],
    }

def test_find_nearby_stations(lodging_1, station_1, station_2):
    with patch('services.station_finder.search_charging_stations') as mock_station:
        mock_station.return_value = [station_1, station_2]
        results = find_nearby_stations(lodging_1, 5)
    res = results[-1]
    assert len(results) == 2
    assert isinstance(res[0], ChargingStation)
    assert isinstance(res[1], float)
    assert res[1] == pytest.approx(500, abs=5)

def test_find_all_nearby_stations(lodging_1, lodging_2, station_1):
    with patch('services.station_finder.find_nearby_stations') as mock_find:
        mock_find.return_value = [(station_1, 5.0)]
        results = find_all_nearby_stations([lodging_1, lodging_2], 10)
    assert lodging_1 in results.keys()
    assert lodging_2 in results.keys()

def test_filter_lodging(results, lodging_1, lodging_2):
    test = filter_lodging(results, 2.0)
    assert lodging_1 in test.keys()
    assert lodging_2 not in test.keys()

def test_filter_lodging_without_filter(results):
    res = filter_lodging(results, 0.0)
    assert res == results

def test_filter_stations_by_power(results, lodging_1, station_1, station_2, station_4):
    test = filter_stations(results, 100, SOCKET_TYPES_LABELS.values())
    res = test[lodging_1]
    assert (station_1, 5) in res
    assert (station_2, 10) not in res
    assert (station_4, 15) in res

def test_filter_stations_without_filter(results):
    res = filter_stations(results, 0, SOCKET_TYPES_LABELS.values())
    assert res == results

def test_filter_stations_by_socket(results, lodging_1, station_1, station_2, station_4):
    test = filter_stations(results, 0, ["CSS Combo 2"])
    res = test[lodging_1]
    assert (station_1, 5) in res
    assert (station_2, 10) not in res
    assert (station_4, 15) not in res

def test_count_grouped_stations(results, lodging_1):
    count = count_grouped_stations(results[lodging_1])
    assert count == 2

def test_create_stations_data(results, lodging_1, station_1, station_4):
    data = create_stations_data(results)[0]
    assert data['lat'] == 44.8378
    assert data['lng'] == -0.5792
    assert data['name'] == 'Station Test'
    assert data['store_name'] == 'Tesla'
    assert data['address'] == '1 Rue Test'
    assert data['schedule'] == '24/7'
    assert data['nb_spots'] == 10
    assert data['powers'] == '200 / 220'
    assert data['tarification'] == "0.30€/kWh, 0.5€/kWh"
    assert data['socket_types_available'] == ['prise_type_2', 'prise_type_combo_ccs', 'prise_type_ef']
    assert data['distance'] == 5
    assert data['icon'] == 'station'

def test_most_common_or_none():
    assert most_common_or_none(['a', 'b', 'a']) == 'a'
    assert most_common_or_none([]) is None
