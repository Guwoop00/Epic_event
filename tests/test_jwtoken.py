import jwt
from datetime import datetime, timedelta, timezone

from views.menu_view import MenuView


def test_store_tokens(token_manager, mock_user, mocker):
    """Test pour vérifier que les tokens sont correctement stockés."""
    mock_view = mocker.spy(MenuView, 'store_tokens_view')
    token_manager.store_tokens(mock_user.id, 'fake_token')
    assert token_manager.cache[mock_user.id] == 'fake_token'
    mock_view.assert_called_once_with(mock_user.id)


def test_get_tokens(token_manager, mock_user, mocker):
    """Test pour vérifier que les tokens sont correctement récupérés."""
    token_manager.cache[mock_user.id] = 'fake_token'
    mock_view = mocker.spy(MenuView, 'get_tokens_view')
    token = token_manager.get_tokens(mock_user.id)
    assert token == 'fake_token'
    mock_view.assert_called_once_with(mock_user.id)


def test_create_token(token_manager, mock_user):
    """Test pour vérifier la création d'un token JWT."""
    token = token_manager.create_token(mock_user)
    payload = jwt.decode(token, token_manager.SECRET_KEY, algorithms=['HS256'])
    assert payload['user_id'] == mock_user.id
    assert payload['user_email'] == mock_user.email
    assert payload['user_role'] == mock_user.role.name
    assert 'exp' in payload


def test_decode_token_valid(token_manager, mock_user):
    """Test pour vérifier que le décodage d'un token valide retourne l'user_id."""
    token = token_manager.create_token(mock_user)
    user_id = token_manager.decode_token(token)
    assert user_id == mock_user.id


def test_decode_token_expired(token_manager, mock_user, mocker):
    """Test pour vérifier que le décodage d'un token expiré retourne None et que l'exception est capturée."""
    expired_payload = {
        'user_id': mock_user.id,
        'exp': datetime.now(timezone.utc) - timedelta(minutes=1)
    }
    expired_token = jwt.encode(expired_payload, token_manager.SECRET_KEY, algorithm='HS256')

    user_id = token_manager.decode_token(expired_token)
    assert user_id is None


def test_decode_token_invalid(token_manager, mocker):
    """Test pour vérifier que le décodage d'un token invalide retourne None et que l'exception est capturée."""
    invalid_token = 'this.is.an.invalid.token'

    user_id = token_manager.decode_token(invalid_token)
    assert user_id is None


def test_validate_token(token_manager, mock_user):
    """Test pour vérifier la validation d'un token valide."""
    token = token_manager.create_token(mock_user)
    user_id = token_manager.validate_token(token)
    assert user_id == mock_user.id


def test_check_token_valid(token_manager, mock_user):
    """Test pour vérifier que check_token retourne l'user_id pour un token valide."""
    token = token_manager.create_token(mock_user)
    user_id = token_manager.check_token(token, mock_user)
    assert user_id == mock_user.id


def test_check_token_invalid(token_manager, mock_user):
    """Test pour vérifier que check_token retourne None pour un token invalide."""
    invalid_token = 'this.is.an.invalid.token'
    user_id = token_manager.check_token(invalid_token, mock_user)
    assert user_id is None
