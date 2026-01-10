"""API module for MSpread."""

try:
    from .api import create_app
except ImportError:
    from api import create_app

__all__ = ["create_app"]
