from unittest.mock import patch
import pytest
from data.charging_stations import search_charging_stations
from models.schemas import ChargingStation
from math import cos, radians

def test_search_charging_stations_with_results(odre_response_1, odre_response_2):
    with patch('data.charging_stations.requests.get') as mock_orde:
        mock_orde.return_value.json.return_value = {
            'total_count': 2,
            'results': [odre_response_1, odre_response_2]
        }
        stations = search_charging_stations((0.0, 0.0), 5)
    assert len(stations) == 2
    assert isinstance(stations[0], ChargingStation)

def test_search_charging_stations_with_reserved_access():
    with patch('data.charging_stations.requests.get') as mock_orde:
        mock_orde.return_value.json.return_value = {'results': []}
        search_charging_stations((44.84, -0.57), 1000)

    where = mock_orde.call_args.kwargs['params']['where']
    assert "condition_acces != 'Accès réservé'" in where

def test_search_charging_stations_boundingbox():
    lat, lng, radius = 44.84, -0.57, 1000

    with patch('data.charging_stations.requests.get') as mock_orde:
        mock_orde.return_value.json.return_value = {'results': []}
        search_charging_stations((lat, lng), radius)

    where = mock_orde.call_args.kwargs['params']['where']
    lat_delta = radius / 111000
    lng_delta = radius / (111000 * cos(radians(lat)))
    assert f"{lat - lat_delta}" in where
    assert f"{lat + lat_delta}" in where
    assert f"{lng - lng_delta}" in where
    assert f"{lng + lng_delta}" in where

def test_search_charging_http_error():
    with patch('data.charging_stations.requests.get') as mock_google_place:
        mock_google_place.side_effect = Exception
        with pytest.raises(RuntimeError):
            search_charging_stations((0.0, 0.0), 5)
