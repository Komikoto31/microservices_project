import json
import traceback
from aio_pika import connect_robust, IncomingMessage
from app.services import DeliveryService
from app.settings import settings

async def process_created_order(msg: IncomingMessage):
    """Обработка события создания заказа"""
    try:
        data = json.loads(msg.body.decode())
        print(f"Received order_created event: {data}")
        service = DeliveryService()
        service.create_delivery(
            data['order_id'],
            data['date'],
            data['address'],
            data.get('comment')
        )
        await msg.ack()
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        await msg.ack()

async def setup_rabbitmq():
    """Настройка RabbitMQ"""
    try:
        connection = await connect_robust(settings.amqp_url, timeout=10)
        channel = await connection.channel()
        queue = await channel.declare_queue('order_created_queue', durable=True)
        await queue.consume(process_created_order)
        print("RabbitMQ consuming started successfully!")
        return connection
    except Exception as e:
        print(f"Failed to connect to RabbitMQ: {e}")
        return None
