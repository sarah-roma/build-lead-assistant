from requests_oauthlib import OAuth2Session
from http.server import HTTPServer, BaseHTTPRequestHandler
import webbrowser
import os
from typing import Optional, cast

# Mural documentation: https://developers.mural.co/public/docs/python-example


class OAuthHTTPServer(HTTPServer):
    auth_response: Optional[str] = None


class ServerHandler(BaseHTTPRequestHandler):
    """ Handle OAuth2 redirect callback """
    def do_GET(self) -> None:
        try:
            self.send_response(200)
            self.end_headers()

            server = cast(OAuthHTTPServer, self.server)
            server.auth_response = self.requestline[4:-9]

        except Exception as e:
            self.send_error(500, f"Error processing callback: {e}")


class AuthenticateMural:
    """Mural OAuth2 Authentication"""

    def __init__(
        self,
        client_id: str = os.environ.get("CLIENT_ID"),
        client_secret: str = os.environ.get("CLIENT_SECRET"),
        redirect_uri: str = os.environ.get("REDIRECT_URI"),
        auth_base_url: str = os.environ.get("AUTHORIZATION_BASE_URL"),
        token_url: str = os.environ.get("TOKEN_URL"),
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.auth_base_url = auth_base_url
        self.token_url = token_url

        self.scopes = [
            "murals:read", "murals:write", "rooms:read", "rooms:write",
            "templates:read", "templates:write", "workspaces:read",
            "users:read", "workspaces:write", "identity:read",
        ]

        # Validate required settings
        missing = []
        for key, value in [
            ("CLIENT_ID", client_id),
            ("CLIENT_SECRET", client_secret),
            ("REDIRECT_URI", redirect_uri),
            ("AUTHORIZATION_BASE_URL", auth_base_url),
            ("TOKEN_URL", token_url)
        ]:
            if not value:
                missing.append(key)
        if missing:
            raise ValueError(f"Missing required OAuth settings: {', '.join(missing)}")

    def authenticate(self):
        """Authenticate with Mural and obtain an access token."""
        try:
            mural = OAuth2Session(
                self.client_id,
                scope=self.scopes,
                redirect_uri=self.redirect_uri,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to create OAuth2 session: {e}")

        try:
            authorization_url, _ = mural.authorization_url(self.auth_base_url)
        except Exception as e:
            raise RuntimeError(f"Failed to generate authorization URL: {e}")

        try:
            webbrowser.open(authorization_url)
        except Exception:
            print("Could not open browser")
            print(authorization_url)

        try:
            httpd = HTTPServer(("127.0.0.1", 8081), ServerHandler)
        except Exception as e:
            raise RuntimeError(f"Failed to start local HTTP server: {e}")

        try:
            httpd.handle_request()
        except Exception as e:
            raise RuntimeError(f"Error handling redirect callback: {e}")

        if not getattr(httpd, "auth_response", None):
            raise RuntimeError("No authorization response received from redirect callback.")

        redirect_response = (
            "http export OAUTHLIB_INSECURE_TRANSPORT=1://127.0.0.1:8081"
            + httpd.auth_response
        )

        try:
            token = mural.fetch_token(
                self.token_url,
                client_secret=self.client_secret,
                authorization_response=redirect_response,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to fetch access token: {e}")

        return token
