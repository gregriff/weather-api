from fastapi.exceptions import HTTPException
from httpx import AsyncClient

from api.services.nws.config import FORECAST_URL, HOURLY_FORECAST_URL, POINTS_URL
from api.services.nws.types import PointsResponse
from api.v1.schemas import (
    ForecastResponse,
    Gridpoints,
    HourlyForecastResponse,
)


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


async def get_gridpoints(nws: AsyncClient, latitude: str, longitude: str) -> Gridpoints:
    """Expects str coords returned by `format_coordinates`"""
    res = await get_gridpoints_raw(nws, latitude, longitude)

    location_info = (  # test
        (gridpoint_info := res.get("properties"))
        .get("relativeLocation")
        .get("properties")
    )
    return Gridpoints(
        office=gridpoint_info["cwa"],
        x=gridpoint_info["gridX"],
        y=gridpoint_info["gridY"],
        city=location_info["city"],
        state=location_info["state"],
    )


async def get_forecast_raw(
    nws: AsyncClient,
    latitude: str,
    longitude: str,
    gridpoints: Gridpoints | None,
) -> ForecastResponse:
    """Expects str coords returned by `format_coordinates`"""
    if gridpoints is None:
        gridpoints = await get_gridpoints(nws, latitude, longitude)

    res = await nws.get(FORECAST_URL % (gridpoints.office, gridpoints.x, gridpoints.y))
    response = res.json()
    response["gridpoints"] = gridpoints

    if res.status_code != 200:
        print(response["detail"])
        raise HTTPException(res.status_code, detail=response["detail"])
    return response


async def get_hourly_forecast_raw(
    nws: AsyncClient,
    latitude: str,
    longitude: str,
    gridpoints: Gridpoints | None,
) -> HourlyForecastResponse:
    """Expects str coords returned by `format_coordinates`"""
    if gridpoints is None:
        gridpoints = await get_gridpoints(nws, latitude, longitude)

    res = await nws.get(
        HOURLY_FORECAST_URL % (gridpoints.office, gridpoints.x, gridpoints.y),
    )
    response = res.json()

    if res.status_code != 200:
        print(response["detail"])
        raise HTTPException(res.status_code, detail=response["detail"])
    return response
