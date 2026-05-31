from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from src.core.constants.departments import DepartmentsConst
from src.schemas.employees import SEmployeesResponse


class SDepartmentsCreate(BaseModel):
    """Schema for validating data on department creation."""

    name: str = Field(
        ...,
        description='The name of the department',
        min_length=DepartmentsConst.NAME_MIN_LEN,
        max_length=DepartmentsConst.NAME_MAX_LEN,
    )
    parent_id: Optional[int] = Field(
        None,
        description='Parent department ID if nested',
        gt=DepartmentsConst.MIN_PARENT_ID,
    )
    model_config = ConfigDict(from_attributes=True)


class SDepartments(SDepartmentsCreate):
    """Base schema with shared department attributes."""

    id: int = Field(..., description='Unique department ID')
    created_at: datetime = Field(
        ..., description='Timestamp when the department was created'
    )
    model_config = ConfigDict(from_attributes=True)


class SDepartmentsResponse(SDepartments):
    """Schema for serializing flat department data."""

    model_config = ConfigDict(from_attributes=True)


class SDepartmentsUpdate(BaseModel):
    """Schema for validating data on department updates."""

    name: Optional[str] = Field(
        None,
        description='The new name of the department',
        min_length=DepartmentsConst.NAME_MIN_LEN,
        max_length=DepartmentsConst.NAME_MAX_LEN,
    )
    parent_id: Optional[int] = Field(
        None,
        description='Parent department ID if nested',
        gt=DepartmentsConst.MIN_PARENT_ID,
    )


class SDepartmentsResponseExtended(SDepartmentsResponse):
    """Schema for flat department data including its employee records."""

    employees: List[SEmployeesResponse] = Field(
        default_factory=list, description='List of employees in the department'
    )


class SDepartmentsTreeResponse(SDepartmentsResponse):
    """Schema for department tree where employees are optional."""

    employees: Optional[List[SEmployeesResponse]] = Field(
        None, description='List of employees (None if not requested)'
    )
    children: List['SDepartmentsTreeResponse'] = Field(
        default_factory=list, description='List of child departments'
    )
    model_config = ConfigDict(from_attributes=True)


SDepartmentsTreeResponse.model_rebuild()
