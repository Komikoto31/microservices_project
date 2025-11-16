import logging
from fastapi import FastAPI
from app.endpoints import delivery_router
from app.database import create_tables
from app.rabbitmq import setup_rabbitmq

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title='Delivery Service',
    description='Service for delivery management',
    version='2.0.0'
)

@app.on_event("startup")
async def startup_event():
    try:
        logger.info("Starting Delivery Service...")
        create_tables()
        logger.info("Database tables created successfully")

        logger.info("Setting up RabbitMQ...")
        await setup_rabbitmq()
        logger.info("RabbitMQ setup completed")

        logger.info("Delivery Service started successfully!")
    except Exception as e:
        logger.error(f"Startup error: {e}")
        raise

app.include_router(delivery_router, prefix='/api')

@app.get("/")
def read_root():
    return {"message": "Delivery Service is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
