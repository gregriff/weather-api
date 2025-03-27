from fastapi import APIRouter

from api.v1.routes.weather import router as weather_router

api_v1 = APIRouter()

api_v1.include_router(weather_router, prefix="/weather", tags=["Weather"])


@api_v1.get("/", tags=["Root"])
async def root():
    return 'API is working, for interactive documentation, append "docs" to URL'
