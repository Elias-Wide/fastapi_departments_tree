class DbLogMessages:
    LOG_INTEGRITY_ERR = 'Integrity error in add_one: {error}'
    LOG_CREATE_ERR = 'Unexpected error in add_one: {error}'
    LOG_FETCH_ERR = 'Database error in get_all: {error}'
    LOG_DELETE_ERR = 'Database error in delete: {error}'


class DbErrorMessages:
    ERR_RECORD_EXISTS = 'Record already exists.'
    ERR_DB_ERROR = 'Internal database error.'
    ERR_FETCH_FAILED = 'Failed to fetch records.'
    ERR_DELETE_FAILED = 'Failed to delete record.'
