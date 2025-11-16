import sys
import os
import warnings

# Подавление deprecation warning от passlib/argon2
warnings.filterwarnings("ignore", category=DeprecationWarning, module="passlib")

# Добавляем путь к user_service (на уровень выше tests)
CURRENT_DIR = os.path.dirname(__file__)
SERVICE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..'))
sys.path.insert(0, SERVICE_DIR)

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services import UserService

@pytest.fixture
def client():
    """Создаёт тестового клиента FastAPI"""
    return TestClient(app)

@pytest.fixture
def user_service():
    """Возвращает экземпляр сервиса пользователей"""
    return UserService()