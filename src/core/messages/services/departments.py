class DepartmentsLogMessages:
    LOG_CREATE_DEPT_ERR = 'Failed to create department: {error}'
    LOG_FETCH_ALL_DEPT_ERR = 'Failed to fetch all departments: {error}'
    LOG_FETCH_ID_DEPT_ERR = (
        'Failed to fetch department by id {dept_id}: {error}'
    )
    LOG_GET_DEPT_WITH_EMP_ERR = (
        'Failed to fetch department with employees: {error}'
    )
    LOG_CREATE_DEPT_SELF_PARENT_ERR = (
        'Department with ID {dept_id} cannot be its own parent.'
    )
    LOG_DEPT_CYCLE_ERR = (
        'Updating department ID {dept_id} to new parent ID '
        '{new_parent_id} would create a cycle.'
    )


class DepartmentsErrorMessages:
    ERR_CREATE_DEPT_FAILED = 'Could not create department.'
    ERR_FETCH_ALL_DEPT_FAILED = 'Could not retrieve departments list.'
    ERR_FETCH_ID_DEPT_FAILED = 'Could not retrieve department details.'
    ERR_UQ_DEPT_NAME_BY_PARENT = (
        "Department with the name '{name}' already exists at this "
        'hierarchy level.'
    )
    ERR_REASSIGN_DEPT_NOT_FOUND = (
        'Reassignment failed: target department with ID '
        '{department_id} not found.'
    )
    ERR_GET_DEPT_WITH_EMP_FAILED = (
        'Could not retrieve department with employees.'
    )
    ERR_UPDATE_DEPT_SAME_ID = (
        'Cannot update a department to have the same ID as itself.'
    )
    ERR_CREATE_DEPT_SELF_PARENT = (
        'Cannot create a department with itself as a parent.'
    )
    ERR_CREATE_DEPT_PARENT_NOT_FOUND = (
        'Cannot create a department with a non-existent parent.'
    )
    FK_PARENT_DEPT_NOT_FOUND = (
        'Parent department with the specified ID does not exist.'
    )
    ERR_REASSIGN_DEPT_ID_REQUIRED = (
        'Reassign department ID is required for this delete mode.'
    )
    ERR_REASSIGN_HIERARCHY = (
        'Cannot reassign to a department within the deleted hierarchy.'
    )
    ERR_DEL_DEPT_SAME_ID = (
        'Cannot reassign employees to the department for deletion.'
    )
