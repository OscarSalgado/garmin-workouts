import logging
from typing import Any, Optional

from garminconnect import Garmin
from requests import Response

# Import centralized garmin_client - use None as default for optional parameter
try:
    from account import garmin_client as default_garmin_client
except ImportError:
    default_garmin_client = None

logger = logging.getLogger(__name__)


class GarminApi(object):
    _GARMIN_SUBDOMAIN = "connectapi"
    _GARMIN_VERSION = "26.5.0.149"

    def __init__(self, email: str, password: str, client: Optional[Garmin] = None) -> None:
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
            self._client: Optional[Garmin] = client
        elif default_garmin_client is not None:
            self._client = default_garmin_client
        else:
            # Fallback: create a new client for backward compatibility (e.g., in tests)
            self._client = Garmin(email=email, password=password, prompt_mfa=self.get_mfa)

        # Initialize properties from client
        self.display_name: str = self._client.display_name or ""
        self.full_name: str = self._client.full_name or ""
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

    def login(self, /, tokenstore: Optional[str] = None) -> bool:
        """Deprecated: login is now handled by the centralized account.garmin_client.

        This method is kept for backward compatibility but is now a no-op since
        authentication is handled in account.py during module initialization.

        Args:
            tokenstore: Ignored. Kept for backward compatibility.

        Returns:
            bool: Always returns True.
        """
        logging.debug("GarminApi.login() is deprecated. Authentication is now handled by account.garmin_client")
        return True

    def get_mfa(self) -> str:
        """Get MFA."""

        return input("MFA one-time code: ")

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
