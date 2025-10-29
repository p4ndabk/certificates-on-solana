"""Middleware package"""

from .auth import api_key_middleware

__all__ = ["api_key_middleware"]
