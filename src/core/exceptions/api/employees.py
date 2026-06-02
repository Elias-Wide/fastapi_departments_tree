from fastapi import status

from src.core.exceptions.api.base import APIException


class EmployeeServiceAPIException(APIException):
    """
    Generic API exception for unhandled employee service errors.
    """

    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = 'Employee service violation occurred.'


class EmployeeNotFoundAPIException(EmployeeServiceAPIException):
    """
    API exception when the requested employee cannot be found.
    """

    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = 'Employee with provided ID does not exist.'


class EmployeeConflictAPIException(EmployeeServiceAPIException):
    """
    API exception when an employee email or passport already exists.
    """

    STATUS_CODE = status.HTTP_409_CONFLICT
    DETAIL = 'Employee with provided data already exists.'


class EmployeeAPIException(EmployeeServiceAPIException):
    """
    API exception when the provided employee data violates rules.
    """

    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = 'Provided employee data violates business rules.'
