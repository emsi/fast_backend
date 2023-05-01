"""Main router for API."""
from fastapi import APIRouter

from .auth_router import api_router as fastapi_user_router

api_router = APIRouter()
api_router.include_router(fastapi_user_router)
