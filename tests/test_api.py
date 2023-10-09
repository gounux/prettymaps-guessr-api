import pytest
from httpx import Response

from tests import client


def test_status_ok():
    response: Response = client.get("/status/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_countries():
    response: Response = client.get("/countries")
    assert response.status_code == 200
    json = response.json()
    assert len(json) == 182
    assert "Belgium" in json
    assert "Germany" in json
    assert "Netherlands" in json
    assert "United Kingdom" in json
    assert "United States of America" in json


@pytest.mark.parametrize(
    "country,nb_picks,preset",
    [
        ("Belgium", 2, "minimal"),
        ("Germany", 4, "barcelona"),
        ("Spain", 3, "tijuca"),
        ("Netherlands", 2, "heerhugowaard"),
        ("France", 4, "default"),
    ],
)
def test_picks_response_ok(country: str, nb_picks: int, preset: str):
    response: Response = client.post(
        "/pick", json={"country": country, "nb_picks": nb_picks, "preset": preset}
    )
    assert response.status_code == 200
    json = response.json()
    assert json["request"]["country"] == country
    assert json["request"]["nb_picks"] == nb_picks
    assert json["request"]["preset"] == preset
