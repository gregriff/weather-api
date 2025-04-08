# used to validate shape and types of Mapbox-related http request bodies and responses
from pydantic.main import BaseModel


class GeocodeQueryData(BaseModel):
    latitude: float
    longitude: float
    search_string: str
