from dataclasses import dataclass
from typing import Optional

@dataclass
class Lodging:
    place_id:str
    name: str
    latitude: float
    longitude: float
    address:str
    extern_link: str
    rating: Optional[float]
    user_rating_totals:Optional[int]
    image_url: Optional[str]

    @classmethod
    def from_api_response(cls, data: dict):
        place_id = data['place_id']
        name = data['name']
        latitude = data['geometry']['location']['lat']
        longitude = data['geometry']['location']['lng']
        address = data['vicinity']
        extern_link = f"https://www.google.com/maps/place/?q=place_id:{place_id}"
        rating = data.get('rating')
        user_rating_totals = data.get('user_rating_totals')
        image_url = None
        return cls(place_id, name, latitude, longitude, address, extern_link, rating, user_rating_totals, image_url)
    
