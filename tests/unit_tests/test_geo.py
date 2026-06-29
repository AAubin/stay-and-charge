import pytest
from services.geo import calculate_distance, results_are_distant
from models.schemas import Lodging

coordonnees_paris = (48.8566, 2.3522)
coordonnees_bordeaux = (44.8378, -0.5792)
close_lodgings = [
    Lodging('test1', 'test1', 44.8400, -0.5700, 'address1', 'link1', None, None, None),
    Lodging('test2', 'test2', 44.8410, -0.5710, 'address2', 'link2', None, None, None),
    Lodging('test3', 'test3', 44.8390, -0.5690, 'address3', 'link3', None, None, None),
]
far_lodgings = [
    Lodging('test4', 'test4', 45.5000, 2.1000, 'address4', 'link4', None, None, None),
    Lodging('test5', 'test5', 45.5010, 2.1010, 'address5', 'link5', None, None, None),
    Lodging('test6', 'test6', 45.4990, 2.0990, 'address6', 'link6', None, None, None),
]

def test_calculate_distance():
    assert calculate_distance(coordonnees_paris, coordonnees_bordeaux) == pytest.approx(500, abs=5)

def test_results_are_distant_empty_lodgings():
    assert not results_are_distant(coordonnees_bordeaux, [], 10)

def test_results_are_distant_close_lodgings():
    assert not results_are_distant(coordonnees_bordeaux, close_lodgings, 10)

def test_results_are_distant_far_lodgings():    
    assert results_are_distant(coordonnees_bordeaux, far_lodgings, 10)

def test_results_are_distant_mix_lodgings():  
    mix_lodgings = close_lodgings + far_lodgings  
    assert not results_are_distant(coordonnees_bordeaux, mix_lodgings, 10)
