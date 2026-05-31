from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import (
    ForeignKey,
    String,
    UniqueConstraint,
    event,
    func,
)
from sqlalchemy.orm import (
    Mapped,
    Session,
    mapped_column,
    relationship,
)

from src.core.constants.departments import DepartmentsConst
from src.core.exceptions.database import DBUniqueViolationError
from src.core.logging import get_logger
from src.db.database import Model

logger = get_logger(__name__)
if TYPE_CHECKING:
    from src.models.employees import EmployeesORM


class DepartmentsORM(Model):
    """
    Represent an organizational department.

    Supports a self-referential hierarchical tree structure.
    Deleting a parent department triggers a cascade delete for
    all sub-departments and associated employees.

    Attributes:
        id (int): Unique identifier and primary key.
        name (str): The name of the department.
        parent_id (int, optional): Foreign key pointing to the
            parent department's ID. None for top-level root.
        created_at (datetime): Automatically generated timestamp
            indicating when the department record was created.
        parent (Department, optional): Relationship to the parent
            department object.
        sub_departments (list[Department]): Relationship to all
            child departments nested under this department.
        employees (list[Employee]): Relationship to all employees
            assigned to this specific department.
    """

    __tablename__ = 'departments'
    __table_args__ = (
        UniqueConstraint(
            'name',
            'parent_id',
            name='uq_department_name_by_parent',
        ),
    )

    name: Mapped[str] = mapped_column(
        String(length=DepartmentsConst.NAME_MAX_LEN),
        nullable=False,
    )
    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('departments.id', ondelete='CASCADE'),
        nullable=True,
        index=True,
        comment='Foreign key to parent department.',
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )

    parent: Mapped[Optional['DepartmentsORM']] = relationship(
        'DepartmentsORM',
        remote_side=lambda: DepartmentsORM.id,
        back_populates='children',
    )

    children: Mapped[List['DepartmentsORM']] = relationship(
        'DepartmentsORM', back_populates='parent'
    )

    employees: Mapped[List['EmployeesORM']] = relationship(
        'EmployeesORM',
        back_populates='department',
        cascade='all, delete-orphan',
    )

    def __repr__(self) -> str:
        """Technical representation of the object for debugging."""
        return (
            f'<Department('
            f'id={self.id!r}, '
            f'name={self.name!r}, '
            f'parent_id={self.parent_id!r}'
            f')>'
        )

    def __str__(self) -> str:
        """User-friendly string representation."""
        return self.name


@event.listens_for(DepartmentsORM, 'before_insert')
@event.listens_for(DepartmentsORM, 'before_update')
def validate_department_uniqueness(mapper, connection, target: DepartmentsORM):
    """Validate that no other department exists on the same level."""
    session = Session.object_session(target)
    if not session:
        return
    query = session.query(DepartmentsORM).filter(
        DepartmentsORM.name == target.name,
        DepartmentsORM.parent_id == target.parent_id,
    )
    if target.id:
        query = query.filter(DepartmentsORM.id != target.id)

    if query.first():
        logger.error(
            f"Department with name '{target.name}' and "
            f'parent_id {target.parent_id} already exists.'
        )
        raise DBUniqueViolationError()
