from fastapi import APIRouter

from api.dependencies import NWS
from api.services.nws.config import TEST_COORDS
from api.services.nws.methods import (
    get_forecast_raw,
    get_gridpoints_raw,
)

router = APIRouter()


@router.get("/")
async def test_forecast(nws: NWS):
    return await get_forecast_raw(nws, *TEST_COORDS)


@router.get("/gridpoints")
async def get_gridpoint_data(nws: NWS):
    return await get_gridpoints_raw(nws, *TEST_COORDS)
