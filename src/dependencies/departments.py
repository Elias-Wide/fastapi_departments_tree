from typing import Annotated, Any

from fastapi import Depends, HTTPException, status

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


async def get_department_search_params(
    depth: int = None, include_employees: bool = True
):
    """Validate and return parameters for department search."""
    if not depth:
        depth = 1
    if depth < DepartmentsConst.MIN_DEPTH:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                ApiErrorMessages.DEPARTMENT_SEARCH_DEPTH_TOO_LOW.format(
                    param='depth',
                    min_depth=DepartmentsConst.MIN_DEPTH,
                )
            ),
        )
    if depth > DepartmentsConst.MAX_DEPTH:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                ApiErrorMessages.DEPARTMENT_SEARCH_DEPTH_TOO_HIGH.format(
                    param='depth',
                    max_depth=DepartmentsConst.MAX_DEPTH,
                )
            ),
        )
    return {
        'depth': depth,
        'include_employees': include_employees,
    }


DeleteDepartmentParamsDep = Annotated[
    dict[str], Depends(get_department_delete_params)
]
GetDepartmentSearchParamsDep = Annotated[
    dict[str], Depends(get_department_search_params)
]
