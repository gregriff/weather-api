from operator import itemgetter

from fastapi.exceptions import HTTPException
from httpx import AsyncClient

from api.services.nws.config import FORECAST_URL, POINTS_URL
from api.services.nws.types import PointsResponse
from api.v1.schemas import ForecastResponse


async def get_gridpoints_raw(
    nws: AsyncClient, latitude: str, longitude: str
) -> PointsResponse:
    """Expects str coords returned by `format_coordinates`"""
    res = await nws.get(POINTS_URL % (latitude, longitude))
    response = res.json()

    # TODO: handle case of non-US lat/long, since this will fail?
    if res.status_code != 200:
        print(response["detail"])
        raise HTTPException(res.status_code, detail=response["detail"])
    return response


async def get_gridpoints(
    nws: AsyncClient, latitude: str, longitude: str
) -> tuple[tuple[str, int, int], tuple[str, str]]:
    """Expects str coords returned by `format_coordinates`"""
    res = await get_gridpoints_raw(nws, latitude, longitude)

    gridpoint_data = itemgetter("cwa", "gridX", "gridY")(res["properties"])
    location_info = res["properties"]["relativeLocation"]["properties"]
    city, state = location_info["city"], location_info["state"]
    return gridpoint_data, (city, state)


async def get_forecast_raw(
    nws: AsyncClient, latitude: str, longitude: str
) -> ForecastResponse:
    """Expects str coords returned by `format_coordinates`"""
    gridpoint_data, location_data = await get_gridpoints(nws, latitude, longitude)
    res = await nws.get(FORECAST_URL % gridpoint_data)
    response = res.json()
    response["properties"]["city"] = location_data[0]
    response["properties"]["state"] = location_data[1]

    if res.status_code != 200:
        print(response["detail"])
        raise HTTPException(res.status_code, detail=response["detail"])
    return response
