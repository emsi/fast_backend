"""User database."""
from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from .database import Base, get_async_session


class User(SQLAlchemyBaseUserTableUUID, Base):
    """User model."""


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """Get the user database."""
    yield SQLAlchemyUserDatabase(session, User)
