import json
from typing import List, Set

from fastapi import FastAPI

from api.models import PicksRequest, PicksResponse, Status

app = FastAPI()


@app.get("/status", description="Get the status of the API")
async def get_status() -> Status:
    return Status(status="ok")


@app.get(
    "/countries",
    description="Get available countries",
    response_description="List of available countries",
)
async def get_available_countries() -> Set[str]:
    with open("data/world_countries.geojson", "r") as file:
        geojson = json.loads(file.read())
        assert geojson["type"] == "FeatureCollection"
        return set(sorted([c["properties"]["ADMIN"] for c in geojson["features"]]))


@app.post(
    "/pick",
    description="Get some picks to guess an image",
    response_model=PicksResponse,
    response_description="A set of picks",
)
async def get_image_picks(q: PicksRequest) -> PicksResponse:
    # TODO: generate prettymaps image and picks
    return PicksResponse(
        request=q, image_url=f"{q.country}-{q.preset}", picks=[], correct_pick_index=1
    )
