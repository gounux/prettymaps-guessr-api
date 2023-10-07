import json
from typing import Dict, List

from fastapi import FastAPI

app = FastAPI()


@app.get("/status", description="Get the status of the API")
def get_status() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/countries", description="Get available countries")
def get_available_countries() -> List[str]:
    with open("data/world_countries.geojson", "r") as file:
        geojson = json.loads(file.read())
        assert geojson["type"] == "FeatureCollection"
        return sorted([c["properties"]["ADMIN"] for c in geojson["features"]])
