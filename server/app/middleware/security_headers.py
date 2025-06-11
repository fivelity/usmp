"""Security headers middleware for FastAPI.
Adds common security-related HTTP headers to every response.
"""
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response
from typing import Callable, Awaitable, Dict


_DEFAULT_HEADERS: Dict[str, str] = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Referrer-Policy": "strict-origin-when-cross-origin",
}


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware that appends secure HTTP headers to every outgoing response."""

    def __init__(self, app, headers: Dict[str, str] | None = None):  # type: ignore[override]
        super().__init__(app)
        self.headers = headers or _DEFAULT_HEADERS

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        response = await call_next(request)
        for key, value in self.headers.items():
            # Do not overwrite if header already set elsewhere
            if key not in response.headers:
                response.headers[key] = value
        return response
