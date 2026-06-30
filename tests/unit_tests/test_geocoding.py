from unittest.mock import patch
import pytest
from data.geocoding import geocode_location

def test_geocode_location_knwon_city():
    with patch('data.geocoding.requests.get') as mock_geocoding:
        mock_geocoding.return_value.json.return_value = {
            'status': 'OK', 
            'results': [{'geometry': {'location': {'lat': 44.8378, 'lng': -0.5792}}}]
        }
        location = geocode_location(33000)

    assert location == (44.8378, -0.5792)

def test_geocode_location_unknwon_city():
    with patch('data.geocoding.requests.get') as mock_geocoding:
        mock_geocoding.return_value.json.return_value = {
            'status': 'ZERO_RESULTS', 
        }
        with pytest.raises(ValueError):
            geocode_location('tartempion')

def test_geocode_location_api_timeout():
    with patch('data.geocoding.requests.get') as mock_geocoding:
        mock_geocoding.return_value.json.return_value = {
            'status': 'REQUEST_DENIED', 
        }
        with pytest.raises(RuntimeError):
            geocode_location(33000)

def test_geocode_location_serice_error():
    with patch('data.geocoding.requests.get') as mock_geocoding:
        mock_geocoding.side_effect = Exception
        with pytest.raises(RuntimeError):
            geocode_location(33000)
