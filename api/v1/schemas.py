# used to validate http request bodies and responses
from typing import List, Literal

from pydantic import BaseModel


# Requests
class Gridpoints(BaseModel):
    office: str
    x: int
    y: int

    # if user provides gridpoints when requesting a forecast, they already have this data
    city: str
    state: str


class LocationData(BaseModel):
    latitude: float
    longitude: float
    gridpoints: Gridpoints | None = None


# Responses
class ForecastPeriod(BaseModel):
    number: int
    name: str
    startTime: str
    endTime: str
    isDaytime: bool
    temperature: int
    temperatureUnit: str
    temperatureTrend: str
    probabilityOfPrecipitation: dict[
        Literal["value", "unitCode"], float | int | str | None
    ]
    windSpeed: str
    windDirection: str
    shortForecast: str
    detailedForecast: str


class ForecastProperties(BaseModel):
    generatedAt: str  # ISO 8601 str repr
    updateTime: str
    periods: List[ForecastPeriod]


class ForecastResponse(BaseModel):
    properties: ForecastProperties
    gridpoints: Gridpoints


class HourlyForecastPrecipitationObject(BaseModel):
    value: int | float | None
    maxValue: int | None = None
    minValue: int | None = None
    unitCode: str


class HourlyForecastPeriod(BaseModel):
    number: int
    name: str
    startTime: str
    endTime: str
    isDaytime: bool
    temperatureTrend: str
    probabilityOfPrecipitation: HourlyForecastPrecipitationObject
    dewpoint: HourlyForecastPrecipitationObject
    relativeHumidity: HourlyForecastPrecipitationObject
    windDirection: str
    shortForecast: str
    detailedForecast: str


class HourlyForecastProperties(BaseModel):
    generatedAt: str  # ISO 8601 str repr
    updateTime: str
    periods: List[HourlyForecastPeriod]


class HourlyForecastResponse(BaseModel):
    properties: HourlyForecastProperties
