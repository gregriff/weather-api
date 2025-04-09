from fastapi.routing import APIRouter

from api.dependencies import Mapbox
from api.services.mapbox.methods import forward_geocode
from api.v1.schemas.mapbox import GeocodePlacesResponse, GeocodeQueryData

router = APIRouter()


@router.post("/place")
async def geocode_place(query: GeocodeQueryData, mapbox: Mapbox):
    mapbox_response = await forward_geocode(
        mapbox, query.search_text, query.latitude, query.longitude
    )

    place_data, coordinates, context = [], {}, {}
    for feature in mapbox_response["features"]:
        coordinates = dict(
            zip(["longitude", "latitude"], feature["geometry"]["coordinates"])
        )
        context = feature["properties"]["context"]
        place_data.append(
            dict(
                coordinates=coordinates,
                place_name=context["place"]["name"],
                region_name=context["region"]["name"],
                region_code=context["region"]["region_code"],
            )
        )
    return GeocodePlacesResponse(places=place_data)
