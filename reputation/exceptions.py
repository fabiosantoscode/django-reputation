"""
exceptions for django-reputation
"""

class ReputationError(Exception):
    """A generic exception for all others to extend."""
    pass

class AlreadyRegistered(ReputationError):
    """Raised when a model is already registered with a site."""
    pass

class NotRegistered(ReputationError):
    """Raised when a model is not registered with a site."""
    pass
