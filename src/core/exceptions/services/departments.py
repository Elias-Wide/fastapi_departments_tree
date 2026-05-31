from src.core.exceptions.services.base import ServiceError


class DepartmentServiceError(ServiceError):
    """Base exception for department business logic."""


class DepartmentNotFoundError(DepartmentServiceError):
    msg = 'Department with this ID does not exist.'


class DepartmentAlreadyExistsError(DepartmentServiceError):
    msg = 'Department with this name already exists in this branch.'


class DepartmentSelfReferenceError(DepartmentServiceError):
    msg = 'A department cannot be its own parent.'


class DepartmentCycleError(DepartmentServiceError):
    msg = 'Cannot set parent department due to cyclical reference.'


class DepartmentValidationError(DepartmentServiceError):
    msg = 'Provided department data is invalid.'


class ParentDepartmentError(DepartmentServiceError):
    msg = 'The specified parent department does not exist.'
