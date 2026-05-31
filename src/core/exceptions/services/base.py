from src.core.exceptions.base import AppError


class ServiceError(AppError):
    """Base exception for all service layer business logic."""

    msg = 'Business logic error occurred.'
