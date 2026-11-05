import logging
from getpass import getpass
from typing import Any

from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)
from requests import Response

logger = logging.getLogger(__name__)


class GarminApi:
    _GARMIN_SUBDOMAIN = "connectapi"
    _GARMIN_VERSION = "26.21.3.0"

    def __init__(self, email: str, password: str, client: Garmin | None = None) -> None:
        """Initialize GarminApi with optional client parameter.

        Args:
            email: Email address for backward compatibility (may not be used if client provided)
            password: Password for backward compatibility (may not be used if client provided)
            client: Optional Garmin client instance. A new one is created when omitted
        """
        self.email: str = email
        self.password: str = password

        # Use the provided client or create a new one
        if client is not None:
            self._client: Garmin | None = client
        else:
            self._client = Garmin(email=email, password=password, prompt_mfa=self.get_mfa)

        # The profile (full_name, display_name, unit_system) is filled in by the client's
        # login(), so it is read through properties instead of copied here. The release
        # version is only queried once the client is authenticated.
        self.version: str = self._GARMIN_VERSION
        if self.is_authenticated:
            self._refresh_version()

    @property
    def display_name(self) -> str:
        return getattr(self._client, "display_name", None) or ""

    @property
    def full_name(self) -> str:
        return getattr(self._client, "full_name", None) or ""

    @property
    def unit_system(self) -> str | None:
        return getattr(self._client, "unit_system", None)

    def _refresh_version(self) -> None:
        """Query the Garmin release version, falling back to the built-in default."""
        try:
            self.version = self.get("/info-service/api/system/release-system").json()[0].get('version', '')
        except Exception:
            self.version = self._GARMIN_VERSION
        if self.version != self._GARMIN_VERSION:
            logger.error('Updated version: %s from %s', self.version, self._GARMIN_VERSION)

    def login(self, /, tokenstore: str | None = None) -> bool:
        """Login to Garmin Connect using tokenstore or credentials.

        Args:
            tokenstore: Path to token storage directory. If provided, attempts
                to load existing tokens first.

        Returns:
            bool: True if login successful, False if there is nothing to log in with
            or an unexpected error occurred.

        Raises:
            GarminConnectAuthenticationError: Garmin rejected the credentials.
            GarminConnectConnectionError: Garmin could not be reached.
            GarminConnectTooManyRequestsError: Garmin rate limited the login.
        """
        try:
            if tokenstore:
                # Garmin.login(tokenstore) loads cached tokens when present and
                # falls back to credentials (saving the new tokens there) otherwise.
                self._client.login(tokenstore)
                self._on_login_success()
                return True
            elif self.email and self.password:
                # Credential-based login
                self._client.login()
                self._on_login_success()
                return True
            else:
                # No credentials available
                return False
        except (GarminConnectAuthenticationError, GarminConnectConnectionError, GarminConnectTooManyRequestsError):
            # Callers need to tell these apart (e.g. stop on a rate limit), so never hide them.
            raise
        except Exception as e:
            logger.warning(f"GarminApi.login() failed: {e}")
            return False

    def _on_login_success(self) -> None:
        """Report the account identity and resolve the release version after a login."""
        logger.info("Logged in as %s (%s)", self.full_name, self.display_name)
        if self.is_authenticated:
            self._refresh_version()

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
