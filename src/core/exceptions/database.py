from src.core.exceptions.base import AppError


class DatabaseError(AppError):
    """Base exception for all database layer operations."""

    msg = 'Database operation failed.'


class DBUniqueViolationError(DatabaseError):
    """Raised when a unique constraint or index is violated."""

    msg = 'Database record with the same unique value already exists.'


class DBIntegrityError(DatabaseError):
    """Raised when foreign key or check constraints fail."""

    msg = 'Database integrity constraint violated.'


class DBForeignKeyViolationError(DatabaseError):
    """Raised when a foreign key constraint is violated."""

    msg = 'Foreign key constraint violation.'


class DbDepartmentSelfReferenceError(DatabaseError):
    """Raised when a department is set as its own parent."""

    msg = 'Department cannot reference itself as parent.'
