import pytest
from unittest.mock import patch, MagicMock

from utils.ingestion.mural_authentication import AuthenticateMural




def test_authenticate_mural_init_success(monkeypatch):
    monkeypatch.setenv("CLIENT_ID", "client-id")
    monkeypatch.setenv("CLIENT_SECRET", "client-secret")
    monkeypatch.setenv("REDIRECT_URI", "http://localhost/oauth/mural/callback")
    monkeypatch.setenv("AUTHORIZATION_BASE_URL", "https://auth.mural.co")
    monkeypatch.setenv("TOKEN_URL", "https://api.mural.co/oauth/token")

    auth = AuthenticateMural()

    assert auth.client_id == "client-id"
    assert auth.client_secret == "client-secret"


def test_missing_oauth_environment_variables(monkeypatch):
    monkeypatch.delenv("CLIENT_ID", raising=False)
    monkeypatch.delenv("CLIENT_SECRET", raising=False)
    monkeypatch.delenv("REDIRECT_URI", raising=False)
    monkeypatch.delenv("AUTHORIZATION_BASE_URL", raising=False)
    monkeypatch.delenv("TOKEN_URL", raising=False)

    with pytest.raises(KeyError):
        AuthenticateMural()


@patch("utils.ingestion.mural_authentication.OAuth2Session")
def test_get_authorization_url(mock_oauth):
    mock_session = MagicMock()
    mock_session.authorization_url.return_value = (
        "https://mural.co/oauth/authorize",
        "test-state",
    )

    mock_oauth.return_value = mock_session

    auth = AuthenticateMural()

    url, state = auth.get_authorization_url()

    assert url == "https://mural.co/oauth/authorize"
    assert state == "test-state"

    mock_session.authorization_url.assert_called_once()


@patch("utils.ingestion.mural_authentication.OAuth2Session")
def test_fetch_token_success(mock_oauth):
    mock_session = MagicMock()
    mock_session.fetch_token.return_value = {
        "access_token": "access-token",
        "refresh_token": "refresh-token",
        "expires_in": 3600,
        "token_type": "Bearer",
    }

    mock_oauth.return_value = mock_session

    auth = AuthenticateMural()

    callback_url = (
        "http://localhost/oauth/mural/callback"
        "?code=abc123&state=test-state"
    )

    token = auth.fetch_token(callback_url)

    assert token["access_token"] == "access-token"
    assert token["refresh_token"] == "refresh-token"

    mock_session.fetch_token.assert_called_once()


def test_oauth_scopes_are_set():
    auth = AuthenticateMural()

    assert "murals:read" in auth.scopes
    assert "workspaces:read" in auth.scopes
    assert "identity:read" in auth.scopes


@patch("utils.ingestion.mural_authentication.OAuth2Session")
def test_fetch_token_failure(mock_oauth):
    mock_session = MagicMock()
    mock_session.fetch_token.side_effect = Exception("OAuth failed")

    mock_oauth.return_value = mock_session

    auth = AuthenticateMural()

    with pytest.raises(Exception):
        auth.fetch_token("http://localhost/callback?code=bad")


# import pytest
# from unittest.mock import patch, MagicMock
# from utils.ingestion.mural_authentication import AuthenticateMural, ServerHandler


# # Test ServerHandler
# def test_server_handler_do_get():
#     class FakeServer:
#         auth_response = None


#     class TestServerHandler(ServerHandler):
#         def __init__(self):
#             self.server = FakeServer()
#             self.requestline = "GET /callback?code=1234 HTTP/1.1"
#             self.send_response = MagicMock()
#             self.end_headers = MagicMock()

#     handler = TestServerHandler()

#     handler.do_GET()

#     handler.send_response.assert_called_once_with(200)
#     handler.end_headers.assert_called_once()
#     assert handler.server.auth_response == "/callback?code=1234"



# # Test missing env variables
# def test_missing_oauth_settings():
#     with pytest.raises(ValueError):
#         AuthenticateMural(
#             client_id=None,
#             client_secret=None,
#             redirect_uri=None,
#             auth_base_url=None,
#             token_url=None,
#         )


# # Test authenticate flow
# @patch("utils.ingestion.mural_authentication.webbrowser.open")
# @patch("utils.ingestion.mural_authentication.HTTPServer")
# @patch("utils.ingestion.mural_authentication.OAuth2Session")
# def test_authenticate_success(mock_oauth, mock_http, mock_browser):
#     mock_session = MagicMock()
#     mock_session.authorization_url.return_value = ("http://auth", "state")
#     mock_session.fetch_token.return_value = {"token": "ok"}

#     mock_oauth.return_value = mock_session

#     mock_server = MagicMock()
#     mock_server.auth_response = "/callback?code=999"
#     mock_http.return_value = mock_server

#     auth = AuthenticateMural(
#         client_id="id",
#         client_secret="secret",
#         redirect_uri="http://localhost",
#         auth_base_url="http://authbase",
#         token_url="http://token",
#     )

#     token = auth.authenticate()

#     assert token == {"token": "ok"}
#     mock_session.fetch_token.assert_called_once()
