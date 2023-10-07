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
