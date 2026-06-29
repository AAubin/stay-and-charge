from unittest.mock import patch, MagicMock
import pytest
from data.lodging import search_lodgings
from models.schemas import Lodging

def test_search_lodgings_with_results(google_place_response_1, google_place_response_2):
    with patch('data.lodging.requests.get') as mock_google_place:
        mock_google_place.return_value.json.return_value = {
            'status': "OK",
            'results': [google_place_response_1, google_place_response_2]
        }
        lodgings = search_lodgings((0.0, 0.0), 5)
    assert len(lodgings) == 2
    assert isinstance(lodgings[0], Lodging) 

def test_search_lodgings_without_results():
    with patch('data.lodging.requests.get') as mock_google_place:
        mock_google_place.return_value.json.return_value = {
            'status': "ZERO_RESULTS",
        }
        lodgings = search_lodgings((0.0, 0.0), 5)
    assert not lodgings

def test_search_lodgings_pagination(google_place_response_1, google_place_response_2):
    page1 = MagicMock()
    page1.json.return_value = {
        'status': 'OK',
        'results': [google_place_response_1],
        'next_page_token': 'token_abc'
    }
    page2 = MagicMock()
    page2.json.return_value = {
        'status': 'OK',
        'results': [google_place_response_2],
    }

    with patch('data.lodging.requests.get', side_effect=[page1, page2]) as mock_google_place:
        with patch('data.lodging.time.sleep'):
            result = search_lodgings((44.84, -0.57), 5000)

    assert mock_google_place.call_count == 2
    assert len(result) == 2

def test_search_lodgings_runtime_error():
    with patch('data.lodging.requests.get') as mock_google_place:
        mock_google_place.side_effect = Exception
        with pytest.raises(RuntimeError):
            search_lodgings((0.0, 0.0), 5)
