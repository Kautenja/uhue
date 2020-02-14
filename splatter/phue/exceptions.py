"""Exceptions used by the package."""


class PhueException(Exception):
    """An abstract base class for Phue errors."""

    def __init__(self, id_, message):
        """Initialize the error message."""
        self.id = id_
        self.message = message


class PhueRegistrationException(PhueException):
    """An error for failing to register."""


class PhueRequestTimeout(PhueException):
    """An error for a network timeout."""
