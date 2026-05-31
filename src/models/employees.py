from datetime import date, datetime
from typing import Optional

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.database import Model
from src.models.departments import DepartmentsORM


class EmployeesORM(Model):
    """
    Represent a company employee.

    Each employee is strictly linked to a specific department.
    The database enforces a RESTRICT constraint, preventing the
    deletion of a department if it contains active employees.

    Attributes:
        department_id (int): Foreign key linking the employee
            to their assigned department.
        full_name (str): Full name of the employee.
        position (str): Job title or position within the company.
        hired_at (date, optional): Date when the employee was
            officially hired.
        created_at (datetime): Automatically generated timestamp
            indicating when the employee record was created.
        department (Department): Relationship to the department
            object this employee belongs to.
    """

    full_name: Mapped[str] = mapped_column(nullable=False)
    position: Mapped[str] = mapped_column(nullable=False)
    hired_at: Mapped[Optional[date]] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    department_id: Mapped[int] = mapped_column(
        ForeignKey('departments.id', ondelete='RESTRICT'),
        nullable=True,
        index=True,
    )
    department: Mapped['DepartmentsORM'] = relationship(
        'DepartmentsORM', back_populates='employees'
    )

    def __repr__(self) -> str:
        """Technical representation of the object for debugging."""
        return (
            f'<Employee('
            f'id={self.id!r}, '
            f'full_name={self.full_name!r}, '
            f'position={self.position!r}, '
            f'department_id={self.department_id!r}'
            f')>'
        )

    def __str__(self) -> str:
        """User-friendly string representation."""
        return f'{self.full_name} ({self.position})'
