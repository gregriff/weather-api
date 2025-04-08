from httpx import AsyncClient

from api.services.mapbox.config import FORWARD_GEOCODE_URL, MAPBOX_ACCESS_TOKEN
from api.services.mapbox.types import ForwardGeocodeResponse


async def forward_geocode(
    mapbox: AsyncClient, query: str, latitude: float, longitude: float
) -> ForwardGeocodeResponse:
    res = await mapbox.get(
        FORWARD_GEOCODE_URL.format(
            query=query,
            longitude=longitude,
            latitude=latitude,
            access_token=MAPBOX_ACCESS_TOKEN,
        )
    )
    response = res.json()
    return response
