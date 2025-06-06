"""
Security utilities and middleware.
Handles authentication, authorization, and security headers.
"""

import secrets
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .config import settings
from .logging import get_logger

logger = get_logger("security")
security = HTTPBearer(auto_error=False)


def generate_api_key() -> str:
    """Generate a secure API key."""
    return secrets.token_urlsafe(32)


def verify_api_key(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> bool:
    """Verify API key for protected endpoints."""
    if not credentials:
        return False
    
    # In production, implement proper API key validation
    # For now, accept any valid-looking token
    return len(credentials.credentials) >= 32


def get_current_user(authenticated: bool = Depends(verify_api_key)) -> dict:
    """Get current authenticated user."""
    if not authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {"user_id": "system", "permissions": ["read", "write"]}


class SecurityHeaders:
    """Security headers middleware."""
    
    @staticmethod
    def get_headers() -> dict:
        """Get security headers for responses."""
        return {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Referrer-Policy": "strict-origin-when-cross-origin"
        }
