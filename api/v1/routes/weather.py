from fastapi import APIRouter

from api.dependencies import NWS
from api.services.nws.config import TEST_COORDS
from api.services.nws.methods import (
    get_forecast_raw,
    get_gridpoints_raw,
)
from api.services.nws.utils import format_coord
from api.v1.schemas import Coordinates, ForecastResponse

router = APIRouter()


@router.get("/")
async def test_forecast(nws: NWS):
    return await get_forecast_raw(nws, *TEST_COORDS)


@router.get("/gridpoints")
async def test_gridpoints(nws: NWS):
    lat, long = format_coord(TEST_COORDS[0]), format_coord(TEST_COORDS[1])
    return await get_gridpoints_raw(nws, lat, long)


@router.post("/forecast")
async def create_forecast_from_coordinates(
    coordinates: Coordinates, nws: NWS
) -> ForecastResponse:
    return await get_forecast_raw(nws, coordinates.latitude, coordinates.longitude)
