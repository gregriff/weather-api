from fastapi.exceptions import HTTPException
from httpx import AsyncClient

from api.services.mapbox.config import FORWARD_GEOCODE_URL, MAPBOX_ACCESS_TOKEN
from api.services.mapbox.types import ForwardGeocodeResponse


async def forward_geocode(
    mapbox: AsyncClient,
    search_text: str,
    latitude: float | None,
    longitude: float | None,
) -> ForwardGeocodeResponse:
    url = FORWARD_GEOCODE_URL.format(
        search_text=search_text,
        access_token=MAPBOX_ACCESS_TOKEN,
    )
    if longitude and latitude:
        url += f"&proximity={longitude}%2C{latitude}"

    res = await mapbox.get(url)
    response = res.json()

    if (status := res.status_code) != 200:
        raise HTTPException(status, response["message"])
    return response
