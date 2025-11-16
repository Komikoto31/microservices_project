from uuid import UUID
from datetime import datetime
from app.models import Delivery, DeliveryStatuses
from app.repositories import DeliveryRepo

class DeliveryService:
    def __init__(self):
        self.repo = DeliveryRepo()

    def get_deliveries(self) -> list[Delivery]:
        return self.repo.get_deliveries()

    def get_delivery_by_id(self, id: UUID) -> Delivery:
        return self.repo.get_delivery_by_id(id)

    def create_delivery(self, order_id: UUID, date: datetime, address: str,
                        comment: str | None = None, customer_id: UUID | None = None) -> Delivery:
        delivery = Delivery(
            id=order_id,
            address=address,
            date=date,
            status=DeliveryStatuses.CREATED,
            comment=comment,
            customer_id=customer_id or UUID('00000000-0000-0000-0000-000000000000')
        )
        return self.repo.create_delivery(delivery)

    def cancel_delivery(self, delivery_id: UUID) -> Delivery:
        return self.repo.cancel_delivery(delivery_id)

    def update_delivery_comment(self, delivery_id: UUID, comment: str) -> Delivery:
        return self.repo.update_comment(delivery_id, comment)
