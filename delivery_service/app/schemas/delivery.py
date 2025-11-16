from sqlalchemy import Column, String, DateTime, Enum, Text
from sqlalchemy.dialects.postgresql import UUID
from app.schemas.base_schema import Base
from app.models import DeliveryStatuses

class Delivery(Base):
    __tablename__ = 'deliveries'

    id = Column(UUID(as_uuid=True), primary_key=True)
    address = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    status = Column(Enum(DeliveryStatuses), nullable=False)
    comment = Column(Text, nullable=True)
    customer_id = Column(UUID(as_uuid=True), nullable=False)
