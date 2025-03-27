from fastapi import APIRouter

from api.services.nws.methods import get_test_weather_data

router = APIRouter()


@router.get("/")
async def test_forecast():
    return await get_test_weather_data()
