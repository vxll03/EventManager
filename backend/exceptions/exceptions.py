class UserAlreadyExistsError(Exception):
    def __init__(self, username: str, message="User already exists") -> None:
        super().__init__(message)
        self.username = username


class NotFoundError(Exception):
    pass


class TokenNotFoundError(Exception):
    pass


class BadCredentialsError(Exception):
    pass
