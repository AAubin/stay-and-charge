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

SOCKET_TYPES_LABELS = {
    'prise_type_combo_ccs': "CSS Combo 2", 
    'prise_type_chademo': "CHAdeMO",
    'prise_type_2': "Type 2 (Mennekes)", 
    'prise_type_ef': "Prise domestiques (E/F)", 
    'prise_type_autre': "Autre"
}
POWER_BOUNDS = (0, 300)

# Threshold lodgings found vs search center
THRESHOLD_KM = 5

# Default map display
DEFAULT_CENTER = (47.0811658, 2.399125)
DEFAULT_ZOOM_FRANCE = 5
DEFAULT_ZOOM_CITY = 12

#Map icons
ICON_ATLAS = "http://localhost:8501/app/static/spritesheet.png"
ICON_MAPPING = {
    "hotel": {"x": 0, "y": 0, "width": 64, "height": 64, "anchorY": 64, "mask": True},
    "station": {"x": 64, "y": 0, "width": 64, "height": 64, "anchorY": 64, "mask": True}
}
COLOR_HOTEL = [209, 4, 4] # RGB rouge
COLOR_STATION = [224, 219, 20] # RGB jaune