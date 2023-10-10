import json
import logging
import os
import random
import time
from typing import Set

from fastapi import BackgroundTasks, FastAPI, Request
from shapely.geometry import shape

from api.models import PRETTYMAPS_PRESETS, Pick, PicksRequest, PicksResponse, Status
from api.pm import (
    create_poll_option,
    generate_prettymaps_image,
    get_nominatim_address,
    get_otm_place,
    pick_country,
)

RADIUS_KM = 50
IMAGE_DELETION_TIMEOUT_SECONDS = 60


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


def delete_prettymaps_image(path: str) -> None:
    time.sleep(IMAGE_DELETION_TIMEOUT_SECONDS)
    os.remove(path)
    logging.getLogger().info(f"Deleted {path}")


@app.post(
    "/pick",
    description="Get some picks to guess an image",
    response_model=PicksResponse,
    response_description="A set of picks",
)
async def get_image_picks(
    q: PicksRequest, request: Request, background_tasks: BackgroundTasks
) -> PicksResponse:
    # select country
    country = pick_country(q.country)
    country_name = country["properties"]["ADMIN"]
    polygon = shape(country["geometry"])
    logging.getLogger().info(f"Country: {country_name}")

    # generate picks
    otm_places = [get_otm_place(polygon, RADIUS_KM) for _ in range(q.nb_picks)]
    otm_names = [f["properties"]["name"] for f in otm_places]
    names, addresses = zip(*(get_nominatim_address(f) for f in otm_places))
    poll_options = [
        create_poll_option(otm_names[i - 1], addresses[i - 1], max_length=255)
        for i in range(1, q.nb_picks + 1)
    ]
    logging.getLogger().info(f"Random picks: {' -- '.join(poll_options)}")

    # randomly select the correct pick
    idx_pick = random.randint(1, q.nb_picks) - 1
    logging.getLogger().info(f"Correct pick: {otm_names[idx_pick]}")
    logging.getLogger().info(f"Correct pick: {names[idx_pick]}")

    # generate prettymaps image
    preset = random.choice(PRETTYMAPS_PRESETS) if q.preset == "random" else q.preset
    map_path = generate_prettymaps_image(names[idx_pick], country_name, preset)

    # program image deletion task
    background_tasks.add_task(delete_prettymaps_image, map_path)

    return PicksResponse(
        request=q,
        image_url=f"{request.base_url}prettymaps/{os.path.basename(map_path)}",
        picks=[
            Pick(
                name=poll_options[i],
                osm_display_name=names[i],
                osm_address=addresses[i],
            )
            for i in range(q.nb_picks)
        ],
        correct_pick_index=idx_pick,
    )
