class DepartmentsConst:
    NAME_MAX_LEN: int = 200
    NAME_MIN_LEN: int = 1
    MIN_PARENT_ID: int = 0
    DELETE_MODES: set[str] = {'cascade', 'reassign'}
    CASCADE_DELETE_MODE: str = 'cascade'
    REASSIGN_DELETE_MODE: str = 'reassign'
    MIN_DEPTH: int = 1
    MAX_DEPTH: int = 5
    DEFAULT_DEPTH: int = 1
