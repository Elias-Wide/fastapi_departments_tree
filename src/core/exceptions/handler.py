from fastapi import Request
from fastapi.responses import JSONResponse

from src.core.exceptions.api.departments import APIException
from src.core.exceptions.mappers import BaseExceptionsMapper, get_mapper
from src.core.exceptions.services.base import ServiceError


async def service_error_handler(request: Request, exc: ServiceError):
    """
    Global handler mapping service exceptions directly to API responses.
    """
    mapper: BaseExceptionsMapper | None = await get_mapper(exc)
    if mapper:
        api_exc: APIException = mapper.convert(exc)
        return JSONResponse(
            status_code=api_exc.status_code,
            content={'detail': api_exc.detail},
        )
    return JSONResponse(
        status_code=APIException.STATUS_CODE,
        content={'detail': APIException.DETAIL},
    )
