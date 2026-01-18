class UserAlreadyExistsException(Exception):
    pass

class InvalidCredentialsException(Exception):
    pass

class TokenExpiredException(Exception):
    pass

class InvalidTokenException(Exception):
    pass

class UserNotFoundException(Exception):
    pass

class DatabaseException(Exception):
    pass
