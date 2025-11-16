import enum
from uuid import UUID, uuid4
from typing import Optional


class UserRole(enum.Enum):
    CUSTOMER = 'customer'
    MANAGER = 'manager'
    COURIER = 'courier'


class UserStatus(enum.Enum):
    UNVERIFIED = 'unverified'
    VERIFIED = 'verified'
    BLOCKED = 'blocked'


class User:
    def __init__(self, id: UUID, email: str, name: str, role: UserRole,
                 status: UserStatus, hashed_password: str, address: Optional[str] = None):
        self.id = id
        self.email = email
        self.name = name
        self.role = role
        self.status = status
        self.address = address
        self.hashed_password = hashed_password

    def to_dict(self):
        return {
            "id": str(self.id),
            "email": self.email,
            "name": self.name,
            "role": self.role.value,
            "status": self.status.value,
            "address": self.address
        }


class UserPublic:
    def __init__(self, id: UUID, email: str, name: str, role: UserRole,
                 status: UserStatus, address: Optional[str] = None):
        self.id = id
        self.email = email
        self.name = name
        self.role = role
        self.status = status
        self.address = address

    def to_dict(self):
        return {
            "id": str(self.id),
            "email": self.email,
            "name": self.name,
            "role": self.role.value,
            "status": self.status.value,
            "address": self.address
        }