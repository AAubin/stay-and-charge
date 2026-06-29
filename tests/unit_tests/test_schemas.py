from models.schemas import Lodging, ChargingStation

def test_lodging_from_api_response(google_place_response_1, google_place_response_2):
    lodging = Lodging.from_api_response(google_place_response_1)
    lodging_2 = Lodging.from_api_response(google_place_response_2)
    assert lodging.name == 'Hotel Test'
    assert lodging.address == '27 Rue Test, Bordeaux'
    assert lodging.extern_link == "https://www.google.com/maps/place/?q=place_id:test_id_123"
    assert lodging_2.rating is None

def test_lodging_hash(google_place_response_1, google_place_response_3):
    lodging = Lodging.from_api_response(google_place_response_1)
    lodging_3 = Lodging.from_api_response(google_place_response_3)
    assert hash(lodging) == hash(lodging_3)

def test_lodging_eq(google_place_response_1, google_place_response_2, google_place_response_3, odre_response_1):
    lodging = Lodging.from_api_response(google_place_response_1)
    lodging_2 = Lodging.from_api_response(google_place_response_2)
    lodging_3 = Lodging.from_api_response(google_place_response_3)
    station = ChargingStation.from_api_response(odre_response_1)
    assert lodging != lodging_2
    assert lodging == lodging_3
    assert lodging != station

def test_charging_station_from_api_response(odre_response_1, odre_response_2):
    station = ChargingStation.from_api_response(odre_response_1)
    station_2 = ChargingStation.from_api_response(odre_response_2)
    assert station.name == 'Station Test'
    assert station.address == '1 Rue Test'
    assert station.nominal_power == 220.0
    assert set(station.socket_types_available) == {'prise_type_combo_ccs', 'prise_type_2'}
    assert station_2.socket_types_available == []

def test_charging_station_hash(odre_response_1, odre_response_3):
    station = ChargingStation.from_api_response(odre_response_1)
    station_3 = ChargingStation.from_api_response(odre_response_3)
    assert hash(station) == hash(station_3)

def test_charging_station_eq(odre_response_1, odre_response_2, odre_response_3, google_place_response_1):
    station = ChargingStation.from_api_response(odre_response_1)
    station_2 = ChargingStation.from_api_response(odre_response_2)
    station_3 = ChargingStation.from_api_response(odre_response_3)
    lodging = Lodging.from_api_response(google_place_response_1)
    assert station != station_2
    assert station == station_3
    assert lodging != station
