from typing import Annotated, Any, Literal
from fastapi import Depends, HTTPException, Query, status

from src.core.constants.departments import DepartmentsConst
from src.core.messages.api.base import ApiErrorMessages


async def get_department_delete_params(
    mode: str = DepartmentsConst.CASCADE_DELETE_MODE,
    reassign_to_department_id: int | None = None,
) -> dict[str, Any]:
    """Validate and return parameters for department deletion."""
    if (
        mode == DepartmentsConst.REASSIGN_DELETE_MODE
        and reassign_to_department_id is None
    ):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                ApiErrorMessages.DEPARATMENT_ID_FOR_REASSIGNMENT_REQUIRED.format(
                    param='reassign_to_department_id',
                    mode=DepartmentsConst.REASSIGN_DELETE_MODE,
                )
            ),
        )
    if mode == DepartmentsConst.CASCADE_DELETE_MODE:
        reassign_to_department_id = None
    return {
        'mode': mode,
        'reassign_to_department_id': reassign_to_department_id,
    }


DeleteDepartmentParamsDep = Annotated[
    dict[str, Any], Depends(get_department_delete_params)
]
