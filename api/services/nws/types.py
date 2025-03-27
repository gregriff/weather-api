# for static type checking of NWS API Response objects
from typing import Literal, TypedDict


class RelativeLocation(TypedDict):
    properties: dict[Literal["city", "state"], str]


class PointsProperties(TypedDict):
    forecast: str
    forecastHourly: str
    forecastGridData: str
    relativeLocation: RelativeLocation


class PointsResponse(TypedDict):
    properties: PointsProperties


class ForecastPeriod(TypedDict):
    number: int
    name: str
    startTime: str
    endTime: str
    isDaytime: bool
    temperature: int
    temperatureUnit: str
    temperatureTrend: str
    probabilityOfPrecipitation: dict[Literal["value"], float | int | str | None]
    windSpeed: str
    windDirection: str
    shortForecast: str
    detailedForecast: str


class ForecastProperties(TypedDict):
    generatedAt: str  # ISO 8601 str repr
    updateTime: str
    periods: list[ForecastPeriod]


class ForecastResponse(TypedDict):
    properties: ForecastProperties
