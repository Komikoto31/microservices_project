from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from app.models import Delivery, CreateDeliveryRequest, UpdateDeliveryComment
from app.services import DeliveryService

delivery_router = APIRouter(prefix='/delivery', tags=['Delivery'])

def get_delivery_service() -> DeliveryService:
    return DeliveryService()

@delivery_router.get('/')
def get_deliveries(delivery_service: DeliveryService = Depends(get_delivery_service)) -> list[Delivery]:
    return delivery_service.get_deliveries()

@delivery_router.get('/{delivery_id}')
def get_delivery(delivery_id: UUID, delivery_service: DeliveryService = Depends(get_delivery_service)) -> Delivery:
    try:
        return delivery_service.get_delivery_by_id(delivery_id)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Delivery with id={delivery_id} not found")

@delivery_router.post('/')
def create_delivery(
    delivery_data: CreateDeliveryRequest,
    delivery_service: DeliveryService = Depends(get_delivery_service)
) -> Delivery:
    try:
        return delivery_service.create_delivery(
            delivery_data.order_id,
            delivery_data.date,
            delivery_data.address,
            delivery_data.comment
        )
    except KeyError as e:
        raise HTTPException(status_code=400, detail=str(e))

@delivery_router.post('/{delivery_id}/cancel')
def cancel_delivery(delivery_id: UUID, delivery_service: DeliveryService = Depends(get_delivery_service)) -> Delivery:
    try:
        return delivery_service.cancel_delivery(delivery_id)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Delivery with id={delivery_id} not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@delivery_router.put('/{delivery_id}/comment')
def update_comment(
    delivery_id: UUID,
    comment_data: UpdateDeliveryComment,
    delivery_service: DeliveryService = Depends(get_delivery_service)
) -> Delivery:
    try:
        return delivery_service.update_delivery_comment(delivery_id, comment_data.comment)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Delivery with id={delivery_id} not found")
