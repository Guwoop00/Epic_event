import datetime
from functools import wraps
from typing import Callable, Optional

import jwt
from rich.console import Console

from sentry_config import sentry_exception_handler
from models.models import User
import os
from dotenv import load_dotenv
from views.menu_view import MenuView


class InvalidTokenException(Exception):
    """Exception raised when the token is invalid or expired."""
    pass


class TokenManager:
    """Manages JWT tokens, including creation, validation, caching, and decoding."""
    load_dotenv()
    SECRET_KEY = os.getenv("SECRET_KEY")
    console: Console = Console()
    cache = None

    @classmethod
    def store_tokens(cls, access_token: Optional[str] = None) -> None:
        """Stores the user's token in the cache."""
        cls.cache = access_token
        MenuView.store_tokens_view()

    @classmethod
    def clear_cache(cls) -> None:
        """Clears the cached token."""
        cls.cache = None
        MenuView.clear_cache_view()

    @classmethod
    def create_token(cls, user: User) -> str:
        """Creates a JWT token for a given user."""
        payload = {
            'user_id': user.id,
            'user_email': user.email,
            'user_role': user.role.name,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=1)
        }
        return jwt.encode(payload, cls.SECRET_KEY, algorithm='HS256')

    @classmethod
    @sentry_exception_handler
    def decode_token(cls, token: str) -> Optional[int]:
        """Decodes a JWT token and returns the user ID if valid, otherwise returns None."""
        # import pdb; pdb.set_trace()
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=['HS256'])
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @classmethod
    def validate_token(cls, token: str) -> Optional[int]:
        """Validates a JWT token and returns the user ID if valid."""
        return cls.decode_token(token)

    @classmethod
    def check_token(cls, access_token: str) -> Optional[int]:
        """Checks if the provided token is valid for the given user."""
        user_id = cls.validate_token(access_token)
        if user_id:
            return user_id
        return None

    @staticmethod
    def token_required(f: Callable) -> Callable:
        """Decorator to ensure that a valid token is provided before accessing a function."""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = TokenManager.cache
            if not token:
                raise InvalidTokenException(MenuView.required_token_view())

            user_id_valid = TokenManager.check_token(token)

            if user_id_valid is None:
                raise InvalidTokenException(MenuView.invalid_token_view())

            return f(*args, **kwargs)

        return decorated_function
