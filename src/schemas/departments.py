from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from src.core.constants.departments import DepartmentsConst


class SDepartmentsCreate(BaseModel):
    """Schema for validating data on department creation."""

    name: str = Field(
        ...,
        description='The name of the department',
        min_length=DepartmentsConst.NAME_MIN_LEN,
        max_length=DepartmentsConst.NAME_MAX_LEN,
    )
    parent_id: Optional[int] = Field(
        None, description='Parent department ID if nested', gt=0
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
    """Schema for serializing department data for API responses."""

    pass


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
