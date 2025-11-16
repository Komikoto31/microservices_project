import sys
import os

# Добавляем путь к корню delivery_service
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services import DeliveryService
from app.database import create_tables
import sys
import os

# Добавляем путь к корню user_service, чтобы Python видел пакет app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Перед запуском тестов пересоздаём таблицы"""
    create_tables()

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def delivery_service():
    return DeliveryService()
