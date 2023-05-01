"""Authentication module."""
import uuid

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    """User schema used for GET methods."""


class UserCreate(schemas.BaseUserCreate):
    """User schema used for POST methods."""


class UserUpdate(schemas.BaseUserUpdate):
    """User schema used for PUT methods."""
