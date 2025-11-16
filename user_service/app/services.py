from uuid import UUID, uuid4
from datetime import timedelta
from typing import Optional
from app.models import User, UserRole, UserStatus, UserPublic
from app.security import verify_password, get_password_hash, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES


class UserService:
    def __init__(self):
        from app.repositories import UserRepo
        self.user_repo = UserRepo()

    def get_users(self) -> list[UserPublic]:
        users = self.user_repo.get_users()
        return [UserPublic(
            id=user.id,
            email=user.email,
            name=user.name,
            role=user.role,
            status=user.status,
            address=user.address
        ) for user in users]

    def get_user_by_id(self, id: UUID) -> UserPublic:
        user = self.user_repo.get_user_by_id(id)
        return UserPublic(
            id=user.id,
            email=user.email,
            name=user.name,
            role=user.role,
            status=user.status,
            address=user.address
        )

    def create_user(self, email: str, name: str, password: str, role: UserRole,
                    address: Optional[str] = None) -> UserPublic:
        user = User(
            id=uuid4(),
            email=email,
            name=name,
            role=role,
            status=UserStatus.UNVERIFIED,
            address=address,
            hashed_password=get_password_hash(password)
        )
        created_user = self.user_repo.create_user(user)
        return UserPublic(
            id=created_user.id,
            email=created_user.email,
            name=created_user.name,
            role=created_user.role,
            status=created_user.status,
            address=created_user.address
        )

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        try:
            user = self.user_repo.get_user_by_email(email)
            if not verify_password(password, user.hashed_password):
                return None
            return user
        except KeyError:
            return None

    def login_user(self, email: str, password: str) -> dict:
        user = self.authenticate_user(email, password)
        if not user:
            raise ValueError("Invalid email or password")

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": str(user.id)
        }

    def verify_user(self, user_id: UUID) -> UserPublic:
        user = self.user_repo.update_user_status(user_id, UserStatus.VERIFIED)
        return UserPublic(
            id=user.id,
            email=user.email,
            name=user.name,
            role=user.role,
            status=user.status,
            address=user.address
        )

    # Вложенная функция для демонстрации (требование из задания)
    def validate_user_data(self, email: str, name: str, password: str) -> bool:
        """Вложенная функция для валидации данных пользователя"""

        def is_valid_email(email: str) -> bool:
            return '@' in email and '.' in email.split('@')[1]

        def is_valid_name(name: str) -> bool:
            return len(name.strip()) > 1

        def is_valid_password(password: str) -> bool:
            return len(password) >= 6

        return (is_valid_email(email) and
                is_valid_name(name) and
                is_valid_password(password))