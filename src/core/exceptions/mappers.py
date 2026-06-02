# src/core/exceptions/mappers.py
from typing import Dict, Type

from src.core.exceptions.api.departments import (
    APIException,
    DepartmentConflictAPIException,
    DepartmentNotFoundAPIException,
    DepartmentParentInvalidException,
    DepartmentSelfReferenceAPIException,
    DepartmentValidationAPIException,
)
from src.core.exceptions.api.employees import (
    EmployeeAPIException,
    EmployeeConflictAPIException,
    EmployeeNotFoundAPIException,
)
from src.core.exceptions.services.departments import (
    DepartmentAlreadyExistsError,
    DepartmentNotFoundError,
    DepartmentSelfReferenceError,
    DepartmentServiceError,
    DepartmentValidationError,
    ParentDepartmentError,
    ServiceError,
)
from src.core.exceptions.services.employees import (
    EmployeeAlreadyExistsError,
    EmployeeNotFoundError,
    EmployeeServiceError,
    EmployeeValidationError,
)


class BaseExceptionsMapper:
    """
    Base mapper for registering service to API exception relations.
    """

    MAP: Dict[Type[ServiceError], Type[APIException]] = {}

    @classmethod
    def convert(cls, exc: ServiceError) -> APIException:
        """
        Find and return matching API exception for given service error.
        """
        for service_class, api_class in cls.MAP.items():
            if isinstance(exc, service_class):
                return api_class()
        return APIException()


class DepartmentsExcMapper(BaseExceptionsMapper):
    """Exception mapper dedicated to department module business errors."""

    MAP = {
        DepartmentAlreadyExistsError: DepartmentConflictAPIException,
        DepartmentNotFoundError: DepartmentNotFoundAPIException,
        DepartmentSelfReferenceError: DepartmentSelfReferenceAPIException,
        DepartmentValidationError: DepartmentValidationAPIException,
        ParentDepartmentError: DepartmentParentInvalidException,
    }


class EmployeesExcMapper(BaseExceptionsMapper):
    """Exception mapper dedicated to employee module business errors."""

    MAP = {
        EmployeeNotFoundError: EmployeeNotFoundAPIException,
        EmployeeAlreadyExistsError: EmployeeConflictAPIException,
        EmployeeValidationError: EmployeeAPIException,
    }


async def get_mapper(exc: ServiceError) -> BaseExceptionsMapper | None:
    if isinstance(exc, DepartmentServiceError):
        return DepartmentsExcMapper()
    if isinstance(exc, EmployeeServiceError):
        return EmployeesExcMapper()
    return None
