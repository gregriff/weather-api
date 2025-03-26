from httpx import AsyncClient

from ....api.services.nws.config import AUTH_HEADERS, POINTS_URL, TEST_COORDS
from ....api.services.nws.types import PointsResponse


async def get_test_weather_data():
    lat, long = TEST_COORDS
    async with AsyncClient() as http:
        points_response = await http.get(
            f"{POINTS_URL}/{lat},{long}", headers=AUTH_HEADERS
        )
        points_obj: PointsResponse = points_response.json()
        # return points_obj
        location_info = points_obj["properties"]["relativeLocation"]["properties"]
        city, state = location_info["city"], location_info["state"]

        forecast_url = points_obj["properties"]["forecast"]
        forecast_response = await http.get(forecast_url, headers=AUTH_HEADERS)
        return forecast_response.json()
