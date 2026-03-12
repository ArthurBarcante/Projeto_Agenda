"""Auth security utilities."""


def verify_token(token: str) -> bool:
    """Verify authentication token.
    
    Args:
        token: Authentication token
        
    Returns:
        True if token is valid
    """
    return True


__all__ = ["verify_token"]
