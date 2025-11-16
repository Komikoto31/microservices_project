from uuid import UUID
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Delivery, DeliveryStatuses
from app.schemas.delivery import Delivery as DBDelivery

class DeliveryRepo:
    db: Session

    def __init__(self) -> None:
        self.db = next(get_db())

    def get_deliveries(self) -> list[Delivery]:
        return [
            Delivery(
                id=d.id,
                address=d.address,
                date=d.date,
                status=d.status,
                comment=d.comment,
                customer_id=d.customer_id
            )
            for d in self.db.query(DBDelivery).all()
        ]

    def get_delivery_by_id(self, id: UUID) -> Delivery:
        d = self.db.query(DBDelivery).filter(DBDelivery.id == id).first()
        if d is None:
            raise KeyError(f"Delivery with id={id} not found")
        return Delivery(
            id=d.id,
            address=d.address,
            date=d.date,
            status=d.status,
            comment=d.comment,
            customer_id=d.customer_id
        )

    def create_delivery(self, delivery: Delivery) -> Delivery:
        delivery_db = DBDelivery(
            id=delivery.id,
            address=delivery.address,
            date=delivery.date,
            status=delivery.status,
            comment=delivery.comment,
            customer_id=delivery.customer_id
        )
        self.db.add(delivery_db)
        self.db.commit()
        self.db.refresh(delivery_db)
        return delivery

    def cancel_delivery(self, delivery_id: UUID) -> Delivery:
        d = self.db.query(DBDelivery).filter(DBDelivery.id == delivery_id).first()
        if not d:
            raise KeyError(f"Delivery with id={delivery_id} not found")
        if d.status == DeliveryStatuses.DONE:
            raise ValueError("Cannot cancel completed delivery")
        d.status = DeliveryStatuses.CANCELED
        self.db.commit()
        return self.get_delivery_by_id(delivery_id)

    def update_comment(self, delivery_id: UUID, comment: str) -> Delivery:
        d = self.db.query(DBDelivery).filter(DBDelivery.id == delivery_id).first()
        if not d:
            raise KeyError(f"Delivery with id={delivery_id} not found")
        d.comment = comment
        self.db.commit()
        return self.get_delivery_by_id(delivery_id)
