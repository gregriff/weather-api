# used to validate http request bodies and responses
from typing import List, Literal

from pydantic import BaseModel


# Requests
class Coordinates(BaseModel):
    latitude: float
    longitude: float


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
    city: str
    state: str
    generatedAt: str  # ISO 8601 str repr
    updateTime: str
    periods: List[ForecastPeriod]


class ForecastResponse(BaseModel):
    properties: ForecastProperties


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
