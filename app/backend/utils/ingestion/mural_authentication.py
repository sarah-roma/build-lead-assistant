# from requests_oauthlib import OAuth2Session
# from http.server import HTTPServer, BaseHTTPRequestHandler
# import webbrowser
# import os
# from typing import Optional, cast

# # Mural documentation: https://developers.mural.co/public/docs/python-example


# class OAuthHTTPServer(HTTPServer):
#     auth_response: Optional[str] = None


# class ServerHandler(BaseHTTPRequestHandler):
#     """ Handle OAuth2 redirect callback """
#     def do_GET(self) -> None:
#         try:
#             self.send_response(200)
#             self.end_headers()

#             server = cast(OAuthHTTPServer, self.server)
#             server.auth_response = self.requestline[4:-9]

#         except Exception as e:
#             self.send_error(500, f"Error processing callback: {e}")


# class AuthenticateMural:
#     """Mural OAuth2 Authentication"""

#     def __init__(
#         self,
#         client_id: str = os.environ.get("CLIENT_ID"),
#         client_secret: str = os.environ.get("CLIENT_SECRET"),
#         redirect_uri: str = os.environ.get("REDIRECT_URI"),
#         auth_base_url: str = os.environ.get("AUTHORIZATION_BASE_URL"),
#         token_url: str = os.environ.get("TOKEN_URL"),
#     ):
#         self.client_id = client_id
#         self.client_secret = client_secret
#         self.redirect_uri = redirect_uri
#         self.auth_base_url = auth_base_url
#         self.token_url = token_url

#         self.scopes = [
#             "murals:read", "murals:write", "rooms:read", "rooms:write",
#             "templates:read", "templates:write", "workspaces:read",
#             "users:read", "workspaces:write", "identity:read",
#         ]

#         # Validate required settings
#         missing = []
#         for key, value in [
#             ("CLIENT_ID", client_id),
#             ("CLIENT_SECRET", client_secret),
#             ("REDIRECT_URI", redirect_uri),
#             ("AUTHORIZATION_BASE_URL", auth_base_url),
#             ("TOKEN_URL", token_url)
#         ]:
#             if not value:
#                 missing.append(key)
#         if missing:
#             raise ValueError(f"Missing required OAuth settings: {', '.join(missing)}")

#     def authenticate(self):
#         """Authenticate with Mural and obtain an access token."""
#         try:
#             mural = OAuth2Session(
#                 self.client_id,
#                 scope=self.scopes,
#                 redirect_uri=self.redirect_uri,
#             )
#         except Exception as e:
#             raise RuntimeError(f"Failed to create OAuth2 session: {e}")

#         try:
#             authorization_url, _ = mural.authorization_url(self.auth_base_url)
#         except Exception as e:
#             raise RuntimeError(f"Failed to generate authorization URL: {e}")

#         try:
#             webbrowser.open(authorization_url)
#         except Exception:
#             print("Could not open browser")
#             print(authorization_url)

#         try:
#             httpd = HTTPServer(("127.0.0.1", 8081), ServerHandler)
#         except Exception as e:
#             raise RuntimeError(f"Failed to start local HTTP server: {e}")

#         try:
#             httpd.handle_request()
#         except Exception as e:
#             raise RuntimeError(f"Error handling redirect callback: {e}")

#         if not getattr(httpd, "auth_response", None):
#             raise RuntimeError("No authorization response received from redirect callback.")

#         redirect_response = (
#             "http export OAUTHLIB_INSECURE_TRANSPORT=1://127.0.0.1:8081"
#             + httpd.auth_response
#         )

#         try:
#             token = mural.fetch_token(
#                 self.token_url,
#                 client_secret=self.client_secret,
#                 authorization_response=redirect_response,
#             )
#         except Exception as e:
#             raise RuntimeError(f"Failed to fetch access token: {e}")

#         return token



# from requests_oauthlib import OAuth2Session
# import os

# class AuthenticateMural:
#     def __init__(self):
#         self.client_id = os.environ["CLIENT_ID"]
#         self.client_secret = os.environ["CLIENT_SECRET"]
#         self.redirect_uri = os.environ["REDIRECT_URI"]
#         self.auth_base_url = os.environ["AUTHORIZATION_BASE_URL"]
#         self.token_url = os.environ["TOKEN_URL"]

#         self.scopes = [
#             "murals:read", "murals:write", "rooms:read", "rooms:write",
#             "templates:read", "templates:write", "workspaces:read",
#             "users:read", "workspaces:write", "identity:read",
#         ]

#     def get_authorization_url(self):
#         mural = OAuth2Session(
#             self.client_id,
#             scope=self.scopes,
#             redirect_uri=self.redirect_uri,
#         )
#         authorization_url, state = mural.authorization_url(self.auth_base_url)
#         return authorization_url, state

#     def fetch_token(self, authorization_response: str):
#         mural = OAuth2Session(
#             self.client_id,
#             redirect_uri=self.redirect_uri,
#         )
#         token = mural.fetch_token(
#             self.token_url,
#             client_secret=self.client_secret,
#             authorization_response=authorization_response,
#         )
#         return token


from requests_oauthlib import OAuth2Session
import os
import time


class AuthenticateMural:
    """
    - generates the auth URL
    - exchanges the callback code for a token
    - refreshes tokens when they expire
    """

    def __init__(self):
        # Required OAuth config (must exist in .env)
        self.client_id = os.environ["CLIENT_ID"]
        self.client_secret = os.environ["CLIENT_SECRET"]
        self.redirect_uri = os.environ["REDIRECT_URI"]
        self.auth_base_url = os.environ["AUTHORIZATION_BASE_URL"]
        self.token_url = os.environ["TOKEN_URL"]

        # Permissions requested from Mural
        self.scopes = [
            "murals:read", "murals:write",
            "rooms:read", "rooms:write",
            "templates:read", "templates:write",
            "workspaces:read", "workspaces:write",
            "users:read", "identity:read",
        ]

    def get_authorization_url(self):
        """
        Creates the URL the user must open to authenticate with Mural.
        """
        mural = OAuth2Session(
            self.client_id,
            scope=self.scopes,
            redirect_uri=self.redirect_uri,
        )

        authorization_url, state = mural.authorization_url(self.auth_base_url)
        return authorization_url, state

    def fetch_token(self, authorization_response: str) -> dict:
        """
        Exchanges the OAuth callback URL for an access token.
        """
        mural = OAuth2Session(
            self.client_id,
            redirect_uri=self.redirect_uri,
        )

        token = mural.fetch_token(
            self.token_url,
            client_secret=self.client_secret,
            authorization_response=authorization_response,
        )

        return token

    def get_valid_access_token(self, stored_token: dict) -> dict:
        """
        Returns a valid access token.
        If expired, attempts to refresh it.
        Raises RuntimeError if re-auth is required.
        """

        # Token still valid
        if stored_token.get("expires_at", 0) > time.time():
            return stored_token

        # Cannot refresh without a refresh token
        if "refresh_token" not in stored_token:
            raise RuntimeError("REAUTH_REQUIRED")

        mural = OAuth2Session(
            self.client_id,
            token=stored_token,
            redirect_uri=self.redirect_uri,
        )

        try:
            new_token = mural.refresh_token(
                self.token_url,
                client_id=self.client_id,
                client_secret=self.client_secret,
            )
            return new_token
        except Exception:
            raise RuntimeError("REAUTH_REQUIRED")
