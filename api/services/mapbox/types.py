# for static type inference of Mapbox API Response objects

from typing import Literal, TypedDict


class Geometry(TypedDict):
    type: Literal["Point"]
    coordinates: list[float]


class Context(TypedDict):
    region: dict[Literal["name", "region_code"], str]
    place: dict[Literal["name", "mapbox_id"], str]


class FeatureProperties(TypedDict):
    mapbox_id: str
    feature_type: str
    full_address: str
    name: str
    name_preferred: str
    coordinates: dict[Literal["longitude", "latitude"], float]
    place_formatted: str
    bbox: list[float]
    context: Context


class Feature(TypedDict):
    type: Literal["Feature"]
    id: str
    geometry: Geometry
    properties: FeatureProperties


class ForwardGeocodeResponse(TypedDict):
    type: Literal["FeatureCollection"]
    features: list[Feature]
