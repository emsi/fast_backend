"""Backend entry point"""
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from .configuration import settings
# from .api.router import api_router


app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

# static files with generated client app
app.mount("/client", StaticFiles(directory="client"), name="client")

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# app.include_router(api_router)
# simplify_operation_ids(app)


@app.get("/health")
def health():
    """
    Health check
    :return:
    """
    return "OK"