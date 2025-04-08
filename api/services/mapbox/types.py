# for static type inference of Mapbox API Response objects

from typing import Literal, TypedDict


class Geometry(TypedDict):
    type: Literal["Point"]
    coordinates: list[float]


class FeatureProperties(TypedDict):
    mapbox_id: str
    feature_type: str
    full_address: str
    name: str
    name_preferred: str
    coordinates: dict[Literal["longitude", "latitude"], float]
    place_formatted: str
    bbox: list[float]


class Feature(TypedDict):
    type: Literal["Feature"]
    id: str
    geometry: Geometry
    properties: FeatureProperties


class ForwardGeocodeResponse(TypedDict):
    type: Literal["FeatureCollection"]
    features: list[Feature]
