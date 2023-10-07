from typing import List, Optional

from pydantic import BaseModel


class Status(BaseModel):
    status: str


class PicksRequest(BaseModel):
    country: Optional[str]
    nb_picks: int


class PrettymapsImage(BaseModel):
    url: str


class Pick(BaseModel):
    name: str


class PicksResponse(BaseModel):
    request: PicksRequest
    image_url: str
    picks: List[Pick]
    correct_pick_index: int
