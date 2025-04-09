from fastapi.routing import APIRouter

from api.dependencies import NWS
from api.services.nws.config import TEST_COORDS
from api.services.nws.methods import (
    get_forecast_raw,
    get_gridpoints_raw,
    get_hourly_forecast_raw,
)
from api.services.nws.utils import format_coordinates
from api.v1.schemas.nws import (
    ForecastResponse,
    HourlyForecastResponse,
    LocationData,
)

router = APIRouter()


@router.get("/")
async def test_forecast(nws: NWS):
    lat, long = format_coordinates(*TEST_COORDS)
    return await get_forecast_raw(nws, lat, long, None)


@router.get("/gridpoints")
async def test_gridpoints(nws: NWS):
    lat, long = format_coordinates(*TEST_COORDS)
    return await get_gridpoints_raw(nws, lat, long)


@router.post("/forecast")
async def get_forecast(
    location: LocationData,
    nws: NWS,
) -> ForecastResponse:
    lat, long = format_coordinates(location.latitude, location.longitude)
    return await get_forecast_raw(nws, lat, long, location.gridpoints)


@router.post("/forecast/hourly")
async def get_hourly_forecast(
    location: LocationData,
    nws: NWS,
) -> HourlyForecastResponse:
    lat, long = format_coordinates(location.latitude, location.longitude)
    return await get_hourly_forecast_raw(nws, lat, long, location.gridpoints)
