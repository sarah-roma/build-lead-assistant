import pytest
from unittest.mock import patch, MagicMock
from utils.ingestion.mural_authentication import AuthenticateMural, ServerHandler


# Test ServerHandler
def test_server_handler_do_get():
    class FakeServer:
        auth_response = None


    class TestServerHandler(ServerHandler):
        def __init__(self):
            self.server = FakeServer()
            self.requestline = "GET /callback?code=1234 HTTP/1.1"
            self.send_response = MagicMock()
            self.end_headers = MagicMock()

    handler = TestServerHandler()

    handler.do_GET()

    handler.send_response.assert_called_once_with(200)
    handler.end_headers.assert_called_once()
    assert handler.server.auth_response == "/callback?code=1234"



# Test missing env variables
def test_missing_oauth_settings():
    with pytest.raises(ValueError):
        AuthenticateMural(
            client_id=None,
            client_secret=None,
            redirect_uri=None,
            auth_base_url=None,
            token_url=None,
        )


# Test authenticate flow
@patch("utils.ingestion.mural_authentication.webbrowser.open")
@patch("utils.ingestion.mural_authentication.HTTPServer")
@patch("utils.ingestion.mural_authentication.OAuth2Session")
def test_authenticate_success(mock_oauth, mock_http, mock_browser):
    mock_session = MagicMock()
    mock_session.authorization_url.return_value = ("http://auth", "state")
    mock_session.fetch_token.return_value = {"token": "ok"}

    mock_oauth.return_value = mock_session

    mock_server = MagicMock()
    mock_server.auth_response = "/callback?code=999"
    mock_http.return_value = mock_server

    auth = AuthenticateMural(
        client_id="id",
        client_secret="secret",
        redirect_uri="http://localhost",
        auth_base_url="http://authbase",
        token_url="http://token",
    )

    token = auth.authenticate()

    assert token == {"token": "ok"}
    mock_session.fetch_token.assert_called_once()
