class THSDKError(RuntimeError):
    """Base error raised by the high-level THSDK facade."""


class AuthenticationError(THSDKError):
    """Authentication or persisted-session restoration failed."""


class NotAuthenticatedError(AuthenticationError):
    """No usable authenticated session is available."""


class APIError(THSDKError):
    """A typed public API call failed."""

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}" if code else message)
