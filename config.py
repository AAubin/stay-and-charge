import os
from dotenv import load_dotenv

"""
Environment variables
"""
load_dotenv()
GOOGLE_PLACES_API_KEY = os.getenv('GOOGLE_PLACES_API_KEY')


"""
Config variables
"""
# Google Place API
GOOGLE_PLACES_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

# OpendataSoft API
OPENDATASOFT_URL = "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/bornes-irve/records"
FIELDS_SELECT = 'id_station_itinerance,nom_station,adresse_station,consolidated_latitude,consolidated_longitude,puissance_nominale,nbre_pdc,condition_acces,horaires,gratuit,paiement_cb,tarification,prise_type_combo_ccs,prise_type_chademo,prise_type_2,prise_type_ef,prise_type_autre,nom_enseigne,id_station_itinerance'
SOCKET_TYPES = ['prise_type_combo_ccs', 'prise_type_chademo', 'prise_type_2', 'prise_type_ef', 'prise_type_autre']

# Default map displayed
DEFAULT_CENTER = (47.0811658, 2.399125)
DEFAULT_ZOOM_FRANCE = 5
DEFAULT_ZOOM_CITY = 12