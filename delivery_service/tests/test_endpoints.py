from uuid import uuid4
from datetime import datetime

def test_create_delivery_endpoint(client):
    """Тест POST /api/delivery"""
    response = client.post("/api/delivery/", json={
        "order_id": str(uuid4()),
        "address": "г. Москва, ул. Ленина, д. 5",
        "date": datetime.now().isoformat(),
        "comment": "Без лука"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "created"

def test_get_all_deliveries(client):
    """Тест GET /api/delivery"""
    response = client.get("/api/delivery/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_comment(client):
    """Тест PUT /api/delivery/{id}/comment"""
    # создаём новую доставку
    delivery = client.post("/api/delivery/", json={
        "order_id": str(uuid4()),
        "address": "г. Москва",
        "date": datetime.now().isoformat(),
        "comment": "Тест"
    }).json()

    response = client.put(f"/api/delivery/{delivery['id']}/comment", json={
        "comment": "Обновлённый комментарий"
    })
    assert response.status_code == 200
    assert response.json()["comment"] == "Обновлённый комментарий"
