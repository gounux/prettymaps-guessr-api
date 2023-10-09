from typing import List, Optional

from pydantic import BaseModel


class Status(BaseModel):
    status: str


class PicksRequest(BaseModel):
    country: str | None = "random"
    nb_picks: int
    preset: str | None = "random"


class Pick(BaseModel):
    name: str


class PicksResponse(BaseModel):
    request: PicksRequest
    image_url: str
    picks: List[Pick]
    correct_pick_index: int
