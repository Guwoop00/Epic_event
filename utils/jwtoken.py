import datetime
from functools import wraps
from typing import Callable, Optional

import jwt
from rich.console import Console

from sentry_config import sentry_exception_handler
from models.models import User
from utils.config import SECRET_KEY
from views.menu_view import MenuView


class TokenManager:
    """Manages JWT tokens, including creation, validation, caching, and decoding."""

    _instance = None
    SECRET_KEY: str = SECRET_KEY
    console: Console = Console()

    def __new__(cls) -> 'TokenManager':
        """Implements singleton pattern to ensure only one instance of TokenManager."""
        if cls._instance is None:
            cls._instance = super(TokenManager, cls).__new__(cls)
            cls._instance.cache = {}
        return cls._instance

    def store_tokens(self, user_id: str, access_token: Optional[str] = None) -> None:
        """Stores the user's token in the cache."""
        self.cache[user_id] = access_token
        MenuView.store_tokens_view(user_id)

    def get_tokens(self, user_id: str) -> Optional[str]:
        """Retrieves the stored token for a given user ID."""
        tokens = self.cache.get(user_id)
        if tokens:
            MenuView.get_tokens_view(user_id)
        return tokens

    def clear_cache(self, user_id: str) -> None:
        """Clears the cached token for a given user ID."""
        if user_id in self.cache:
            del self.cache[user_id]
            MenuView.clear_cache_view()

    def create_token(self, user: User) -> str:
        """Creates a JWT token for a given user."""
        payload = {
            'user_id': user.id,
            'user_email': user.email,
            'user_role': user.role.name,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=1)
        }
        return jwt.encode(payload, self.SECRET_KEY, algorithm='HS256')

    @sentry_exception_handler
    def decode_token(self, token: str) -> Optional[int]:
        """Decodes a JWT token and returns the user ID if valid, otherwise returns None."""
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=['HS256'])
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def validate_token(self, token: str) -> Optional[int]:
        """Validates a JWT token and returns the user ID if valid."""
        return self.decode_token(token)

    def check_token(self, access_token: str, user: User) -> Optional[int]:
        """Checks if the provided token is valid for the given user."""
        user_id = self.validate_token(access_token)
        if user_id:
            return user_id
        return None

    @staticmethod
    def token_required(f: Callable) -> Callable:
        """Decorator to ensure that a valid token is provided before accessing a function."""
        @wraps(f)
        def decorated_function(self, user: User):
            token = TokenManager().get_tokens(user.id)
            if not token:
                MenuView.required_token_view()
                return None

            user_id_valid = TokenManager().check_token(token, user)

            if user_id_valid is None:
                MenuView.invalid_token_view()
                return None

            return f(self, user)

        return decorated_function
