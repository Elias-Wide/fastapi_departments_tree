class AppError(Exception):
    """Base application error."""

    msg = 'An unexpected application error occurred.'

    def __init__(self, message: str = None):
        super().__init__(message or self.msg)
        if message:
            self.msg = message

    def __str__(self):
        return self.msg
