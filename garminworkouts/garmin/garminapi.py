import logging
import os
from getpass import getpass
from typing import Any

from garminconnect import Garmin
from requests import Response

# Import centralized garmin_client - use None as default for optional parameter
try:
    from account import garmin_client as default_garmin_client
except ImportError:
    default_garmin_client = None

logger = logging.getLogger(__name__)


class GarminApi:
    _GARMIN_SUBDOMAIN = "connectapi"
    _GARMIN_VERSION = "26.5.0.149"

    def __init__(self, email: str, password: str, client: Garmin | None = None) -> None:
        """Initialize GarminApi with optional client parameter.

        Args:
            email: Email address for backward compatibility (may not be used if client provided)
            password: Password for backward compatibility (may not be used if client provided)
            client: Optional Garmin client instance. Defaults to centralized account.garmin_client
        """
        self.email: str = email
        self.password: str = password

        # Use provided client, fall back to centralized client, or create a new one
        if client is not None:
            self._client: Garmin | None = client
        elif default_garmin_client is not None:
            self._client = default_garmin_client
        else:
            # Fallback: create a new client for backward compatibility (e.g., in tests)
            self._client = Garmin(email=email, password=password, prompt_mfa=self.get_mfa)

        # Initialize properties from client
        try:
            self.display_name: str = self._client.display_name or ""
            self.full_name: str = self._client.full_name or ""
        except Exception:
            self.display_name = ""
            self.full_name = ""
        logging.info("Logged in as %s (%s)", self.full_name, self.display_name)

        # Only call API endpoints that require authentication when the
        # underlying client is authenticated. This prevents test setup from
        # attempting network logins when running in non-interactive contexts.
        if self.is_authenticated:
            self.unit_system: str | None = self._client.unit_system

            try:
                self.version: str = self.get("/info-service/api/system/release-system").json()[0].get('version', '')
            except Exception:
                self.version = self._GARMIN_VERSION
            try:
                assert self.version == self._GARMIN_VERSION
            except AssertionError:
                logging.error('Updated version: ' + self.version + ' from ' + self._GARMIN_VERSION)
        else:
            self.unit_system = None
            self.version = self._GARMIN_VERSION

    def login(self, /, tokenstore: str | None = None) -> bool:
        """Login to Garmin Connect using tokenstore or credentials.

        Args:
            tokenstore: Path to token storage directory. If provided, attempts
                to load existing tokens first.

        Returns:
            bool: True if login successful, False otherwise.
        """
        try:
            if tokenstore and os.path.exists(tokenstore):
                # Try to load existing tokens
                self._client.login(tokenstore)
                return True
            elif self.email and self.password:
                # Credential-based login
                self._client.login()
                return True
            else:
                # No credentials available
                return False
        except Exception as e:
            logging.debug(f"GarminApi.login() failed: {e}")
            return False

    def get_mfa(self) -> str:
        """Get MFA."""
        return getpass("MFA one-time code: ")

    @property
    def is_authenticated(self) -> bool:
        try:
            return bool(self._client and self._client.client.is_authenticated)
        except Exception:
            return False

    def get(self, *args: Any, **kwargs: Any) -> Response:
        return self._client.client.request("GET", self._GARMIN_SUBDOMAIN, *args, **kwargs)

    def put(self, *args: Any, **kwargs: Any) -> Response:
        return self._client.client.put(self._GARMIN_SUBDOMAIN, *args, **kwargs)

    def post(self, *args: Any, **kwargs: Any) -> Response:
        return self._client.client.post(self._GARMIN_SUBDOMAIN, *args, **kwargs)

    def delete(self, *args: Any, **kwargs: Any) -> Response:
        return self._client.client.delete(self._GARMIN_SUBDOMAIN, *args, **kwargs)

    def download(self, path, **kwargs) -> bytes:
        return self._client.client.download(path, **kwargs)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        return None
