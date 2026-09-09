def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    body = response.get_json()
    assert body["success"] is True
    assert body["data"]["status"] == "ok"


def test_get_weather_for_known_city(client):
    response = client.get("/api/weather?city=Amman")
    assert response.status_code == 200
    body = response.get_json()
    assert body["success"] is True
    assert body["data"]["city"] == "Amman"
    assert body["data"]["temperature"] == 24.5


def test_get_weather_missing_city(client):
    response = client.get("/api/weather")
    assert response.status_code == 400
    assert response.get_json()["success"] is False


def test_get_weather_unknown_city(client):
    response = client.get("/api/weather?city=Atlantis")
    assert response.status_code == 404
    assert response.get_json()["error"] == "City not found"


def test_create_list_and_delete_city(client):
    created = client.post("/api/cities", json={"city_name": "London"})
    assert created.status_code == 201
    city_id = created.get_json()["data"]["id"]

    listed = client.get("/api/cities")
    assert listed.status_code == 200
    assert listed.get_json()["data"][0]["city_name"] == "London"

    deleted = client.delete(f"/api/cities/{city_id}")
    assert deleted.status_code == 200
    assert client.get("/api/cities").get_json()["data"] == []


def test_create_duplicate_city(client):
    client.post("/api/cities", json={"city_name": "Amman"})
    response = client.post("/api/cities", json={"city_name": "Amman"})
    assert response.status_code == 409


def test_get_city_by_id(client, saved_city):
    response = client.get(f"/api/cities/{saved_city.id}")
    assert response.status_code == 200
    assert response.get_json()["data"]["city_name"] == "London"


def test_update_city(client, saved_city):
    response = client.put(f"/api/cities/{saved_city.id}", json={"city_name": "Amman"})
    assert response.status_code == 200
    assert response.get_json()["data"]["city_name"] == "Amman"


def test_delete_missing_city(client):
    response = client.delete("/api/cities/999")
    assert response.status_code == 404
