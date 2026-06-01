from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.endpoints.v1.routers import api_router_v1 as main_router
from src.core.exceptions.handler import service_error_handler
from src.core.exceptions.services.base import ServiceError
from src.core.logging import get_logger, setup_logging

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging() 
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(main_router, prefix='/api')
app.add_exception_handler(ServiceError, service_error_handler)
