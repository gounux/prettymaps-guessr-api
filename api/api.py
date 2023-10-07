import json
from typing import List

from fastapi import FastAPI

from api.models import PicksRequest, PicksResponse, Status

app = FastAPI()


@app.get("/status", description="Get the status of the API")
def get_status() -> Status:
    return Status(status="ok")


@app.get(
    "/countries",
    description="Get available countries",
    response_description="List of available countries",
)
def get_available_countries() -> List[str]:
    with open("data/world_countries.geojson", "r") as file:
        geojson = json.loads(file.read())
        assert geojson["type"] == "FeatureCollection"
        return sorted([c["properties"]["ADMIN"] for c in geojson["features"]])


@app.get("/pick", description="Get some picks to guess an image")
def get_image_picks(q: PicksRequest) -> PicksResponse:
    raise NotImplementedError
