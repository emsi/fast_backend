"""API router for authentication and user management."""
from fastapi import APIRouter, Depends

from .auth import auth_backend, current_active_user, fastapi_users
from ..db.database import create_db_and_tables
from ..db.user import User
from ..schemas.user import UserRead, UserCreate, UserUpdate

api_router = APIRouter()
api_router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
api_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
api_router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
api_router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
api_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@api_router.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    """Example authenticated route."""
    return {"message": f"Hello {user.email}!"}


@api_router.on_event("startup")
async def on_startup():
    """Create the initial database tables."""
    # Not needed if you set up a migration system like Alembic
    await create_db_and_tables()
