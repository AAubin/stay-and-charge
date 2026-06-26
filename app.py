from logging_manager import setup_logging
setup_logging()
from data.cache import geocode_city, search_lodgings, search_charging_stations

test_city = 'Bordeaux'
test_coord = geocode_city(test_city)

# test_lodgings = search_lodgings(test_coord)
# nb_lodgings = len(test_lodgings)
# print(nb_lodgings)
# if nb_lodgings > 0:
#     print(test_lodgings[0])

test_stations = search_charging_stations(test_coord)
nb_stations = len(test_stations)
print(nb_stations)
if nb_stations > 0:
    print(test_stations[0])

