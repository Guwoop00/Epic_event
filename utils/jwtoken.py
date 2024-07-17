import jwt
import datetime
from utils.config import SECRET_KEY
from rich.console import Console
from models.models import User


class TokenManager:
    SECRET_KEY = SECRET_KEY
    console = Console()

    def create_token(self, user):
        payload = {
            'user_id': user.id,
            'user_email': user.email,
            'user_role': user.role.name,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
        }
        token = jwt.encode(payload, self.SECRET_KEY, algorithm='HS256')
        return token

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=['HS256'])
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def validate_token(self, token, session):
        user_id = self.decode_token(token)
        if not user_id:
            self.console.print("[bold red]Token invalide ou expiré.[/bold red]")
            return

        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            self.console.print("[bold red]Utilisateur non trouvé.[/bold red]")
            return

        return user_id
