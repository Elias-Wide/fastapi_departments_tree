from src.core.exceptions.services.base import ServiceError


class EmployeeServiceError(ServiceError):
    """Base exception for employee business logic."""


class EmployeeNotFoundError(EmployeeServiceError):
    msg = 'Employee with this ID does not exist.'


class EmployeeAlreadyExistsError(EmployeeServiceError):
    msg = 'Employee with this email or passport already exists.'


class EmployeeValidationError(EmployeeServiceError):
    msg = 'Provided employee data violates business rules.'
