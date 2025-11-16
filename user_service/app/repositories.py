from uuid import UUID
from app.models import User, UserStatus, UserRole
from app.security import get_password_hash

# Временное хранилище в памяти - ПУСТОЙ список
users: list[User] = []


class UserRepo:
    def get_users(self) -> list[User]:
        return [user for user in users if user.status != UserStatus.BLOCKED]

    def get_user_by_id(self, id: UUID) -> User:
        for user in users:
            if user.id == id and user.status != UserStatus.BLOCKED:
                return user
        raise KeyError(f"User with id={id} not found")

    def get_user_by_email(self, email: str) -> User:
        for user in users:
            if user.email == email and user.status != UserStatus.BLOCKED:
                return user
        raise KeyError(f"User with email={email} not found")

    def create_user(self, user: User) -> User:
        # Проверяем, нет ли пользователя с таким email
        try:
            self.get_user_by_email(user.email)
            raise ValueError(f"User with email={user.email} already exists")
        except KeyError:
            pass

        users.append(user)
        return user

    def update_user_status(self, user_id: UUID, status: UserStatus) -> User:
        for user in users:
            if user.id == user_id:
                user.status = status
                return user
        raise KeyError(f"User with id={user_id} not found")