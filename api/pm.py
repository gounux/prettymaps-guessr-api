import json
import logging
import os
import random
from datetime import datetime
from typing import Any, Dict, Tuple

import requests
from requests import Response
from shapely.geometry import Point, Polygon, shape

import prettymaps

OPENTRIPMAP_URL = "https://api.opentripmap.com/0.1/en/places/radius"
OPENTRIPMAP_API_KEY = os.getenv("OPENTRIPMAP_API_KEY")
NOMINATIM_URL = "https://nominatim.openstreetmap.org"


def pick_country(country: str) -> Dict[str, Any]:
    with open("data/world_countries.geojson", "r") as file:
        geojson = json.loads(file.read())
        assert geojson["type"] == "FeatureCollection"
        if country == "random":
            return random.choice(geojson["features"])
        countries = {c["properties"]["ADMIN"].upper(): c for c in geojson["features"]}
        return countries[country.upper()]


def generate_random_point(polygon: Polygon) -> Point:
    minx, miny, maxx, maxy = polygon.bounds
    point = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
    if polygon.contains(point):
        return point
    return generate_random_point(polygon)


def get_otm_place(
    polygon: Polygon, radius_km: int, rate: int = 3, limit: int = 50
) -> Dict[str, Any]:
    # generate a random point inside polygon
    rnd_point = generate_random_point(polygon)

    # get a place from OpenTripMap, see https://opentripmap.io/docs
    r: Response = requests.get(
        OPENTRIPMAP_URL,
        params={
            "lon": rnd_point.x,
            "lat": rnd_point.y,
            "radius": radius_km * 1000,
            "rate": rate,
            "src_attr": "osm",
            "limit": limit,
            "apikey": OPENTRIPMAP_API_KEY,
        },
    )
    assert r.status_code == 200
    features = r.json()["features"]

    # retry if no OpenTripMap place around point
    if len(features) == 0:
        return get_otm_place(polygon, radius_km, rate, limit)

    feature = random.choice(features)
    assert feature["geometry"]["type"] == "Point"
    logging.debug(
        f"OpenTripMap feature: {feature['properties']['name']} {feature['geometry']['coordinates']}"
    )
    return feature


def get_nominatim_address(feature: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    point: Point = shape(feature["geometry"])
    nominatim_r: Response = requests.get(
        f"{NOMINATIM_URL}/reverse",
        params={"lon": point.x, "lat": point.y, "format": "geojson"},
    )
    assert len(nominatim_r.json()["features"]) == 1
    nmntm_feat = nominatim_r.json()["features"][0]
    return nmntm_feat["properties"]["display_name"], nmntm_feat["properties"]["address"]


def create_poll_option(name: str, address: Dict[str, Any], max_length: int = 50) -> str:
    city = address.get("municipality", address.get("town", "somewhere"))
    region = address.get("state", address.get("region", "somewhere"))
    opt = f"{name}, {city}, {region}"
    return opt if len(opt) <= max_length else f"{name}, {city}"


def generate_prettymaps_image(address: str, country: str, preset: str) -> str:
    path = f"prettymaps/pm_{datetime.now().strftime('%Y%m%d-%H%M%S')}_{country.lower().replace(' ', '')}_{preset}.png"
    prettymaps.plot(query=address, preset=preset, save_as=path)
    return path
