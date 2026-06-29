from unittest.mock import patch, MagicMock
import pytest
from data.geocoding import geocode_location
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

def test_geocode_location_knwon_city():
    with patch('data.geocoding.Nominatim.geocode') as mock_nominating:
        mock_nominating.return_value = MagicMock(latitude = 44.8378, longitude = -0.5792)
        location = geocode_location(33000)

    assert location == (44.8378, -0.5792)

def test_geocode_location_unknwon_city():
    with patch('data.geocoding.Nominatim.geocode') as mock_nominating:
        mock_nominating.return_value = None
        with pytest.raises(ValueError):
            geocode_location('tartempion')

def test_geocode_location_api_timeout():
    with patch('data.geocoding.Nominatim.geocode') as mock_nominating:
        mock_nominating.side_effect = GeocoderTimedOut
        with pytest.raises(RuntimeError):
            geocode_location(33000)

def test_geocode_location_serice_error():
    with patch('data.geocoding.Nominatim.geocode') as mock_nominating:
        mock_nominating.side_effect = GeocoderServiceError
        with pytest.raises(RuntimeError):
            geocode_location(33000)
