from app.models import UserRole
from uuid import UUID

def test_user_creation(user_service):
    """Тест успешного создания пользователя"""
    user = user_service.create_user(
        email="test@example.com",
        name="Иван",
        password="123456",
        role=UserRole.CUSTOMER
    )
    assert user.email == "test@example.com"
    assert user.status.value == "unverified"

def test_duplicate_user_email(user_service):
    """Проверка ошибки при повторной регистрации"""
    user_service.create_user("dup@mail.com", "Петр", "pass123", UserRole.CUSTOMER)
    try:
        user_service.create_user("dup@mail.com", "Петр", "pass123", UserRole.CUSTOMER)
        assert False, "Ожидалось исключение ValueError"
    except ValueError:
        assert True

def test_user_validation_valid(user_service):
    """Тест валидации корректных данных"""
    assert user_service.validate_user_data("mail@mail.com", "User", "123456")

def test_user_validation_invalid(user_service):
    """Тест валидации некорректных данных"""
    assert not user_service.validate_user_data("invalid", " ", "12")
