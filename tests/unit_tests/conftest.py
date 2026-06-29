import pytest

@pytest.fixture
def google_place_response_1():
    return {
        'place_id': 'test_id_123',
        'name': 'Hotel Test',
        'geometry': {'location': {'lat': 44.8378, 'lng': -0.5792}},
        'vicinity': '27 Rue Test, Bordeaux',
        'rating': 4.2,
        'user_rating_totals': 150,
    }
@pytest.fixture
def google_place_response_2():
    return {
        'place_id': 'test_id_456',
        'name': 'Hotel Test 2',
        'geometry': {'location': {'lat': 48.8566, 'lng': 2.3522}},
        'vicinity': '27 Rue Test, Pétaouchnok',
    }

@pytest.fixture
def google_place_response_3():
    return {
        'place_id': 'test_id_123',
        'name': 'Hotel Test 3',
        'geometry': {'location': {'lat': 54.84, 'lng': -2.57}},
        'vicinity': '27 bis Rue Test, Pétaouchnok',
    }

@pytest.fixture
def odre_response_1():
    return {
        'id_station_itinerance': 'FRS63E0001',
        'nom_station': 'Station Test',
        'nom_enseigne': 'Tesla',
        'consolidated_latitude': 44.83781,
        'consolidated_longitude': -0.57922,
        'adresse_station': '1 Rue Test',
        'puissance_nominale': 220,
        'nbre_pdc': 2,
        'condition_acces': 'Accès libre',
        'horaires': '24/7',
        'gratuit': 'false',
        'paiement_cb': 'true',
        'tarification': '0.30€/kWh',
        'prise_type_combo_ccs': 'True',
        'prise_type_chademo': 'False',
        'prise_type_2': 'True',
        'prise_type_ef': 'False',
        'prise_type_autre': 'False',
    }

@pytest.fixture
def odre_response_2():
    return {
        'id_station_itinerance': 'FRS63E0002',
        'nom_station': 'Station Test 2',
        'nom_enseigne': 'Pouet',
        'consolidated_latitude': 48.8566,
        'consolidated_longitude': 2.3522,
        'adresse_station': '2 Rue Test',
        'puissance_nominale': 22,
    }

@pytest.fixture
def odre_response_3():
    return {
        'id_station_itinerance': 'FRS63E0001',
        'nom_station': 'Station Test 3',
        'nom_enseigne': 'Pouet²',
        'consolidated_latitude': 54.84,
        'consolidated_longitude': -2.57,
        'adresse_station': '2 bis Rue Test',
    }

@pytest.fixture
def odre_response_4():
    return {
        'id_station_itinerance': 'FRS63E0004',
        'nom_station': 'Station Test 4',
        'nom_enseigne': 'Pouet',
        'consolidated_latitude': 44.83784,
        'consolidated_longitude': -0.57923,
        'adresse_station': '2 Rue Test',
        'puissance_nominale': 200,
        'prise_type_ef': 'True',
        'nbre_pdc': 10,
        'condition_acces': 'Accès libre',
        'horaires': '24/7',
        'tarification': '0.5€/kWh',
    }