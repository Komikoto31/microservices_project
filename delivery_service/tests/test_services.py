
from uuid import uuid4
from datetime import datetime

def test_create_delivery(delivery_service):
    """Проверка создания новой доставки"""
    order_id = uuid4()
    delivery = delivery_service.create_delivery(
        order_id=order_id,
        address="г. Москва, Ленина, 5",
        date=datetime.now(),
        comment="Осторожно с коробкой"
    )
    assert delivery.id == order_id
    assert delivery.status.value == "created"

def test_cancel_delivery(delivery_service):
    """Проверка отмены доставки"""
    order_id = uuid4()
    delivery_service.create_delivery(order_id, "г. Москва", datetime.now())
    delivery = delivery_service.cancel_delivery(order_id)
    assert delivery.status.value == "canceled"
