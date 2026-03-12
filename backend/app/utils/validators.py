"""Utility validators."""


def validate_email(email: str) -> bool:
    """Validate email format.
    
    Args:
        email: Email string to validate
        
    Returns:
        True if email is valid
    """
    return "@" in email and "." in email


__all__ = ["validate_email"]
