# for static type inference of NWS API Response objects
from typing import Literal, TypedDict


class RelativeLocation(TypedDict):
    properties: dict[Literal["city", "state"], str]


class PointsProperties(TypedDict):
    cwa: str  # is this or the gridId the office info?
    forecastOffice: str  # office API endpoint
    gridId: str
    gridX: int
    gridY: int
    forecast: str
    forecastHourly: str
    forecastGridData: str
    relativeLocation: RelativeLocation


class PointsResponse(TypedDict):
    properties: PointsProperties
