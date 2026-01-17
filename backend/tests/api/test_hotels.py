from datetime import date, timedelta

def test_create_hotel(client, admin_headers):
    response = client.post("/hotels/", json={"name": "Grand Budapest", "location": "Zubrowka"}, headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Grand Budapest"
    assert "id" in data
    return data["id"]

def test_create_room_type(client, admin_headers):
    # Setup Hotel
    hotel_res = client.post("/hotels/", json={"name": "Overlook", "location": "Colorado"}, headers=admin_headers)
    hotel_id = hotel_res.json()["id"]

    response = client.post("/room-types/", json={"name": "Suite", "base_rate": 100.0, "hotel_id": hotel_id}, headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Suite"
    assert data["base_rate"] == 100.0
    return data["id"]

def test_rate_adjustment_flow(client, admin_headers):
    # Setup Hotel & Room
    hotel_id = client.post("/hotels/", json={"name": "Ritz", "location": "Paris"}, headers=admin_headers).json()["id"]
    room_id = client.post("/room-types/", json={"name": "Deluxe", "base_rate": 200.0, "hotel_id": hotel_id}, headers=admin_headers).json()["id"]

    # 1. Check Base Rate
    response = client.get(f"/room-types/{room_id}/effective-rate", headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["effective_rate"] == 200.0

    # 2. Add Adjustment (+50)
    today = date.today().isoformat()
    client.post("/rate-adjustments/", json={
        "room_type_id": room_id,
        "adjustment_amount": 50.0,
        "effective_date": today,
        "reason": "Peak"
    }, headers=admin_headers)

    # 3. Check New Rate
    response = client.get(f"/room-types/{room_id}/effective-rate", headers=admin_headers)
    assert response.json()["effective_rate"] == 250.0
