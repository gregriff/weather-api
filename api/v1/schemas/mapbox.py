# used to validate shape and types of Mapbox-related http request bodies and responses
from typing import List, Literal

from pydantic.main import BaseModel


# Requests
class GeocodeQueryData(BaseModel):
    search_text: str
    latitude: float | None = None
    longitude: float | None = None


# Responses
class PlaceData(BaseModel):
    place_name: str
    region_name: str
    region_code: str
    coordinates: dict[Literal["longitude", "latitude"], float]


class GeocodePlacesResponse(BaseModel):
    """Lowest index is highest relevance"""

    places: List[PlaceData]
