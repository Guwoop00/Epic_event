import jwt
import datetime
import sentry_sdk
from views.menu_view import MenuView
from rich.console import Console
from models.models import User
from utils.config import SECRET_KEY
from functools import wraps
from typing import Optional, Dict, Tuple, Callable


class TokenManager:
    _instance = None
    SECRET_KEY = SECRET_KEY
    console = Console()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TokenManager, cls).__new__(cls)
            cls._instance.cache = {}
        return cls._instance

    def store_tokens(self, user_id: str, access_token: Optional[str] = None,
                     refresh_token: Optional[str] = None) -> None:
        self.cache[user_id] = (access_token, refresh_token)
        MenuView.store_tokens_view(user_id)

    def get_tokens(self, user_id: str) -> Optional[Tuple[Optional[str], Optional[str]]]:
        tokens = self.cache.get(user_id)
        if tokens:
            MenuView.get_tokens_view(user_id)
        return tokens

    def clear_cache(self, user_id: str) -> None:
        if user_id in self.cache:
            del self.cache[user_id]
            MenuView.clear_cache_view()

    def create_token(self, user: User) -> str:
        payload = {
            'user_id': user.id,
            'user_email': user.email,
            'user_role': user.role.name,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
        }
        return jwt.encode(payload, self.SECRET_KEY, algorithm='HS256')

    def create_refresh_token(self, user: User) -> str:
        payload = {
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
        }
        return jwt.encode(payload, self.SECRET_KEY, algorithm='HS256')

    def decode_token(self, token: str) -> Optional[int]:
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=['HS256'])
            return payload['user_id']
        except jwt.ExpiredSignatureError as e:
            sentry_sdk.capture_exception(e)
            return None
        except jwt.InvalidTokenError as e:
            sentry_sdk.capture_exception(e)
            return None

    def validate_token(self, token: str) -> Optional[int]:
        return self.decode_token(token)

    def refresh_tokens(self, user) -> Optional[Dict[str, str]]:
        try:
            print(user)
            access_token = self.create_token(user)
            refresh_token = self.create_refresh_token(user)
            self.store_tokens(user_id=user.id, access_token=access_token, refresh_token=refresh_token)
            return {"access_token": access_token, "refresh_token": refresh_token}

        except Exception as e:
            sentry_sdk.capture_exception(e)
            MenuView.refresh_tokens_view()
            return None

    def check_token(self, access_token: str, refresh_token: str, user) -> Optional[int]:
        user_id = self.validate_token(access_token)
        if user_id:
            return user_id

        user_id = self.validate_token(refresh_token)
        if user_id:
            tokens = self.refresh_tokens(user)
            if tokens:
                return user_id

        MenuView.check_token_view()
        return None

    @staticmethod
    def token_required(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(self, user):
            tokens = TokenManager().get_tokens(user.id)
            if not tokens:
                MenuView.required_token_view()
                return None

            access_token, refresh_token = tokens
            print(access_token, refresh_token)

            if not access_token or not refresh_token:
                MenuView.missing_token_view()
                return None

            user_id_valid = TokenManager().check_token(access_token, refresh_token, user)
            print(user_id_valid)
            if user_id_valid is None:
                MenuView.invalid_token_view()
                return None

            return f(self, user)

        return decorated_function
