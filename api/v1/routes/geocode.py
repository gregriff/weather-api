from fastapi.routing import APIRouter

from api.dependencies import Mapbox
from api.services.mapbox.methods import forward_geocode
from api.v1.schemas.mapbox import GeocodeQueryData

router = APIRouter()


@router.get("/place")
async def geocode_place(query: GeocodeQueryData, mapbox: Mapbox):
    # TODO: parse out and return relevent data, create response schema for it
    return forward_geocode(mapbox, query.search_string, query.latitude, query.longitude)
