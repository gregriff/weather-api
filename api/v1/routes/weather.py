from fastapi import APIRouter

from api.dependencies import NWS
from api.services.nws.config import TEST_COORDS
from api.services.nws.methods import (
    get_forecast_raw,
    get_gridpoints_raw,
    get_hourly_forecast_raw,
)
from api.services.nws.utils import format_coordinates
from api.v1.schemas import Coordinates, ForecastResponse, HourlyForecastResponse

router = APIRouter()


@router.get("/")
async def test_forecast(nws: NWS):
    lat, long = format_coordinates(*TEST_COORDS)
    return await get_forecast_raw(nws, lat, long)


@router.get("/gridpoints")
async def test_gridpoints(nws: NWS):
    lat, long = format_coordinates(*TEST_COORDS)
    return await get_gridpoints_raw(nws, lat, long)


@router.post("/forecast")
async def create_forecast_from_coordinates(
    coordinates: Coordinates, nws: NWS
) -> ForecastResponse:
    lat, long = format_coordinates(coordinates.latitude, coordinates.longitude)
    return await get_forecast_raw(nws, lat, long)


@router.post("/forecast/hourly")
async def create_hourly_forecast_from_coordinates(
    coordinates: Coordinates, nws: NWS
) -> HourlyForecastResponse:
    lat, long = format_coordinates(coordinates.latitude, coordinates.longitude)
    return await get_hourly_forecast_raw(nws, lat, long)
