"""Authentication module."""
import uuid
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend, BearerTransport, JWTStrategy
)
from fastapi_users.db import SQLAlchemyUserDatabase

from ..configuration import secret_key, settings
from ..db.user import User, get_user_db

ALGORITHM = "HS256"


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    """Custom user manager to support UUID IDs."""
    reset_password_token_secret = secret_key
    verification_token_secret = secret_key

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    """Create an instance of UserManager with the user database."""
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    """Create an instance of JWTStrategy with the secret key from the configuration."""
    return JWTStrategy(
        secret=secret_key,
        lifetime_seconds=60 * settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        algorithm=ALGORITHM,
    )


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
