class ApiErrorMessages:
    INTERNAL_SERVER_ERROR = (
        'An unexpected error occurred. Please try again later.'
    )
    DEPARTMENT_ID_FOR_REASSIGNMENT_REQUIRED = (
        'The {param} parameter is requiredwhen mode is set to {mode}'
    )
    DEPARTMENT_SEARCH_DEPTH_TOO_LOW = (
        'The {param} parameter must be at least {min_depth} '
        'to perform a search.'
    )
    DEPARTMENT_SEARCH_DEPTH_TOO_HIGH = (
        'The {param} parameter must be at most {max_depth} '
        'to perform a search.'
    )
