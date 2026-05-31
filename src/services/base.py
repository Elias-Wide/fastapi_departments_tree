from src.db.manager import DBManager


class BaseService:
    """Service layer for business logic."""

    def __init__(self, db: DBManager):
        """Initialize the service with a task repository."""
        self.db: DBManager = db
