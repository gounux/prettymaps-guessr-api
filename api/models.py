from typing import List

from pydantic import BaseModel
from pydantic.v1 import Field, validator

from prettymaps import presets as pm_presets

PRETTYMAPS_PRESETS = [
    p.strip()
    for p in pm_presets()["preset"].to_string(index=False).split("\n")
    if "barcelona-plotter" not in p
]


class Status(BaseModel):
    status: str


class PicksRequest(BaseModel):
    country: str | None = Field(default="random")
    nb_picks: int = Field(default=3, ge=2, le=4)
    preset: str | None = Field(default="random")

    # FIXME: the validators are not applied
    @validator("nb_picks")
    def nb_picks_check(cls, nb_picks: int) -> int:
        if 2 <= nb_picks <= 4:
            raise ValueError(f"wrong nb_picks {nb_picks}, must be between 2 and 4")
        return nb_picks

    @validator("preset")
    def preset_known(cls, preset: str) -> str:
        presets = PRETTYMAPS_PRESETS + ["random"]
        if preset not in presets:
            raise ValueError(
                f"unknown preset '{preset}', must be one of {','.join(presets)}"
            )
        return preset


class Pick(BaseModel):
    name: str


class PicksResponse(BaseModel):
    request: PicksRequest
    image_url: str
    picks: List[Pick]
    correct_pick_index: int
