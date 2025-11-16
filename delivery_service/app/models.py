import enum
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class DeliveryStatuses(enum.Enum):
    CREATED = 'created'
    CANCELED = 'canceled'
    DONE = 'done'

class Delivery(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    address: str
    date: datetime
    status: DeliveryStatuses
    comment: str | None = None
    customer_id: UUID

class CreateDeliveryRequest(BaseModel):
    order_id: UUID
    address: str
    date: datetime
    comment: str | None = None

class UpdateDeliveryComment(BaseModel):
    comment: str
