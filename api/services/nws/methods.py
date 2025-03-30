from operator import itemgetter

from fastapi.exceptions import HTTPException
from httpx import AsyncClient

from api.services.nws.config import FORECAST_URL, POINTS_URL
from api.services.nws.types import ForecastResponse, PointsResponse


async def get_gridpoints_raw(
    nws: AsyncClient, latitude: float, longitude: float
) -> PointsResponse:
    response = await nws.get(POINTS_URL % (latitude, longitude))

    # TODO: handle case of non-US lat/long, since this will fail?
    if response.status_code != 200:
        raise HTTPException(response.status_code)

    return response.json()


async def get_gridpoints(
    nws: AsyncClient, latitude: float, longitude: float
) -> tuple[str, int, int]:
    gridpoint_data = await get_gridpoints_raw(nws, latitude, longitude)
    return itemgetter("cwa", "gridX", "gridY")(gridpoint_data["properties"])
    # location_info = points_obj["properties"]["relativeLocation"]["properties"]
    # city, state = location_info["city"], location_info["state"]
    # forecast_url = points_obj["properties"]["forecast"]


async def get_forecast_raw(
    nws: AsyncClient, latitude: float, longitude: float
) -> ForecastResponse:
    gridpoints = await get_gridpoints(nws, latitude, longitude)
    forecast_response = await nws.get(FORECAST_URL % gridpoints)
    return forecast_response.json()
