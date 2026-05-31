from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from src.core.constants.employees import EmployeesConts


class SEmployeesCreate(BaseModel):
    """Schema for validating data on employee creation."""

    full_name: str = Field(
        ...,
        description='Full name of the employee',
        min_length=EmployeesConts.NAME_MIN_LENGTH,
        max_length=EmployeesConts.NAME_MAX_LENGTH,
    )
    position: str = Field(
        ...,
        description='Job title or position',
        min_length=EmployeesConts.POSITION_MIN_LENGTH,
        max_length=EmployeesConts.POSITION_MAX_LENGTH,
    )
    hired_at: Optional[date] = Field(None, description='Official hire date')
    model_config = ConfigDict(from_attributes=True)


class SEmployeeAdd(SEmployeesCreate):
    """Schema for adding an employee to a department."""

    department_id: int = Field(
        ...,
        description='FK for the department',
        gt=EmployeesConts.MIN_DEPARTMENT_ID,
    )


class SEmployees(SEmployeesCreate):
    """Base schema with shared employee attributes."""

    id: int = Field(..., description='Unique internal employee ID')
    department_id: int = Field(
        None,
        description='FK for the department',
        gt=EmployeesConts.MIN_DEPARTMENT_ID,
    )
    created_at: datetime = Field(..., description='Record creation timestamp')


class SEmployeesResponse(SEmployees):
    """Schema for serializing employee data for API responses."""

    pass
