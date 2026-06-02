from fastapi import status

from src.core.exceptions.api.base import APIException


class DepartmentServiceAPIException(APIException):
    """
    Generic API exception for unhandled department service errors.
    """

    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = 'Department business rule violation occurred.'


class DepartmentNotFoundAPIException(DepartmentServiceAPIException):
    """
    API exception when the requested department cannot be found.
    """

    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = 'Department with this ID does not exist.'


class DepartmentForeignKeyAPIException(DepartmentServiceAPIException):
    """
    API exception when a department cannot create or update.
    """

    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = 'Department cannot be deleted due to existing references.'


class DepartmentConflictAPIException(DepartmentServiceAPIException):
    """
    API exception when a department name already exists on the level.
    """

    STATUS_CODE = status.HTTP_409_CONFLICT
    DETAIL = 'Department with this name already exists on that level.'


class DepartmentSelfReferenceAPIException(DepartmentServiceAPIException):
    """
    API exception when a department attempts to set itself as a parent.
    """

    STATUS_CODE = status.HTTP_409_CONFLICT
    DETAIL = (
        'A department cannot be its own parent or a child of his own tree.'
    )


class DepartmentValidationAPIException(DepartmentServiceAPIException):
    """
    API exception when the provided department data is invalid.
    """

    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = 'Provided department data is invalid.'


class DepartmentParentInvalidException(DepartmentServiceAPIException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = 'Provided parent id is invalid (not exist).'
