from dataclasses import dataclass
from typing import Optional
from config import SOCKET_TYPES

@dataclass
class Lodging:
    place_id:str
    name: str
    lat: float
    lng: float
    address:str
    extern_link: str
    rating: Optional[float]
    user_rating_totals:Optional[int]
    image_url: Optional[str]

    @classmethod
    def from_api_response(cls, data: dict) -> 'Lodging':
        place_id = data['place_id']
        name = data['name']
        lat = data['geometry']['location']['lat']
        lng = data['geometry']['location']['lng']
        address = data['vicinity']
        extern_link = f"https://www.google.com/maps/place/?q=place_id:{place_id}"
        rating = data.get('rating')
        user_rating_totals = data.get('user_rating_totals')
        image_url = None
        return cls(place_id, name, lat, lng, address, extern_link, rating, user_rating_totals, image_url)
    
    def __hash__(self):
        return hash(self.place_id)
    
    def __eq__(self, other):
        return self.place_id == other.place_id
    
    
@dataclass
class ChargingStation:
    station_id: str
    name: str
    store_name: str
    lat: float
    lng: float
    address: str
    nominal_power: Optional[float]
    nb_spots: Optional[int]
    socket_types_available: list[str]
    access: Optional[str]
    schedule: Optional[str]
    free: Optional[str]
    paiement_cb: Optional[str]
    tarification: Optional[str]

    @classmethod
    def from_api_response(cls, data: dict) -> 'ChargingStation':
        station_id = data['id_station_itinerance']
        name = data['nom_station']
        store_name = data['nom_enseigne']
        lat = data['consolidated_latitude']
        lng = data['consolidated_longitude']
        address = data['adresse_station']
        nominal_power = data.get('puissance_nominale')
        nb_spots = data.get('nbre_pdc')
        socket_types_available = [socket for socket in SOCKET_TYPES if data.get(socket) == 'True' or data.get(socket) == 'true']
        access = data.get('condition_acces')
        schedule = data.get('horaires')
        free = data.get('gratuit')
        paiement_cb = data.get('paiement_cb')
        tarification = data.get('tarification')
        return cls(station_id, name, store_name, lat, lng, address, nominal_power, nb_spots, socket_types_available, access, schedule, free, paiement_cb, tarification)

    def __hash__(self):
        return hash(self.station_id)
    
    def __eq__(self, other):
        return self.station_id == other.station_id
