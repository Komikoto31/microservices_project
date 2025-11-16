from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Body
from app.services import UserService
from app.models import UserRole
from app.auth import get_current_user, get_current_active_user, require_role

user_router = APIRouter(prefix='/users', tags=['Users'])


def get_user_service() -> UserService:
    return UserService()


# Публичные эндпоинты (не требуют аутентификации)
@user_router.post('/')
def create_user(
        email: str = Body(...),
        name: str = Body(...),
        password: str = Body(...),
        role: str = Body("customer"),
        address: str = Body(None),
        user_service: UserService = Depends(get_user_service)
):
    # Использование вложенной функции (требование из задания)
    if not user_service.validate_user_data(email, name, password):
        raise HTTPException(status_code=400, detail="Invalid user data")

    try:
        # Конвертируем строку в UserRole
        user_role = UserRole(role)
        user = user_service.create_user(email, name, password, user_role, address)
        return user.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_router.post('/login')
def login_user(
        email: str = Body(...),
        password: str = Body(...),
        user_service: UserService = Depends(get_user_service)
):
    try:
        return user_service.login_user(email, password)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


# Защищенные эндпоинты (требуют аутентификации)
@user_router.get('/me')
def get_current_user_info(current_user=Depends(get_current_active_user)):
    return current_user.to_dict()


@user_router.get('/')
def get_users(
        user_service: UserService = Depends(get_user_service),
        current_user=Depends(require_role('manager'))
):
    users = user_service.get_users()
    return [user.to_dict() for user in users]


@user_router.get('/{user_id}')
def get_user(
        user_id: UUID,
        user_service: UserService = Depends(get_user_service),
        current_user=Depends(get_current_active_user)
):
    try:
        user = user_service.get_user_by_id(user_id)
        return user.to_dict()
    except KeyError:
        raise HTTPException(status_code=404, detail=f"User with id={user_id} not found")


@user_router.post('/{user_id}/verify')
def verify_user(
        user_id: UUID,
        user_service: UserService = Depends(get_user_service),
        current_user=Depends(require_role('manager'))
):
    try:
        user = user_service.verify_user(user_id)
        return user.to_dict()
    except KeyError:
        raise HTTPException(status_code=404, detail=f"User with id={user_id} not found")