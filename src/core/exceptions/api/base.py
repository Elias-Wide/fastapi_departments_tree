from fastapi import HTTPException, status

from src.core.messages.api.base import ApiErrorMessages


class APIException(HTTPException):
    """
    Base HTTP exception for consistent application API responses.
    """

    STATUS_CODE: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL: str = ApiErrorMessages.INTERNAL_SERVER_ERROR

    def __init__(self, detail: str = None, status_code: int = None):
        self.status_code = status_code or self.STATUS_CODE
        self.detail = detail or self.DETAIL
        super().__init__(status_code=self.status_code, detail=self.detail)
