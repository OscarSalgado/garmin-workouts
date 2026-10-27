"""Account and authentication configuration for the application.

Provides centralized Garmin API client initialization and credentials
management. Use this module to access the authenticated garmin_client.

Example:
    from account import get_garmin_client
    client = get_garmin_client()
    workouts = client.get_activities()
"""

import logging
import sys
import os
from typing import Optional
from garminworkouts.models.pace import Pace
from garminworkouts.models.power import Power
from decouple import config
from garminconnect import Garmin

__all__ = ['get_garmin_client', 'get_credentials', 'get_intervals_config', 'get_athlete_config', 'garmin_client', 'tokenstore', 'is_interactive']

# Token storage path for Garmin authentication
tokenstore = "./.garminworkouts-cache/garmin"

# Check if we're in an interactive environment
is_interactive = sys.stdin.isatty() if hasattr(sys.stdin, 'isatty') else False

# Module-level cache for lazy-initialized objects
_garmin_client: Optional[Garmin] = None
_credentials: Optional[tuple] = None
_intervals_config: Optional[dict] = None


def get_mfa() -> str:
    """Prompt for Garmin MFA one-time code.

    Returns:
        str: The MFA one-time code entered by the user.
    """
    return input("MFA one-time code: ")


def get_credentials() -> tuple:
    """Load Garmin credentials from environment variables.
    
    Credentials are loaded lazily on first call and cached for subsequent calls.
    This allows tests to mock environment variables before importing this module.
    
    Returns:
        tuple: (email, password) tuple
    """
    global _credentials
    if _credentials is None:
        EMAIL: str | bool = config('GARMIN_USERNAME')
        PASSWORD: str | bool = config('GARMIN_PASSWORD')
        _credentials = (EMAIL, PASSWORD)
    return _credentials


def get_intervals_config() -> dict:
    """Load Intervals.icu configuration from environment variables.
    
    Configuration is loaded lazily on first call and cached.
    
    Returns:
        dict: Dictionary with 'api_key' and 'athlete_id' keys
    """
    global _intervals_config
    if _intervals_config is None:
        _intervals_config = {
            'api_key': config('intervals_api_key'),
            'athlete_id': config('intervals_athlete_id')
        }
    return _intervals_config


def get_garmin_client() -> Garmin:
    """Get or create the centralized Garmin API client.
    
    Client is initialized lazily on first call and cached for subsequent calls.
    This allows tests to mock authentication before the client is created.
    
    Returns:
        Garmin: Authenticated Garmin client instance
    """
    global _garmin_client
    if _garmin_client is None:
        EMAIL, PASSWORD = get_credentials()
        _garmin_client = Garmin(
            email=EMAIL,
            password=PASSWORD,
            prompt_mfa=get_mfa
        )
        
        if is_interactive:
            # Check if tokenstore directory can be created/accessed
            tokenstore_dir = os.path.dirname(tokenstore)
            try:
                os.makedirs(tokenstore_dir, exist_ok=True)
                # Attempt login only in interactive environments
                # At this point _garmin_client is guaranteed to be set (just created above)
                _garmin_client.login(tokenstore)  # type: ignore[union-attr]
            except OSError as e:
                logging.warning("Cannot access tokenstore directory '%s': %s - skipping Garmin login", tokenstore_dir, e)
            except Exception as e:
                logging.warning("Garmin login failed: %s", e)
        else:
            logging.info("Skipping Garmin login in non-interactive environment (CI/CD, tests, or background job)")
    
    return _garmin_client


# Backward compatibility: provide garmin_client as a property-like access
# For code that imports 'garmin_client' directly, this provides the same interface
# Note: For testability, new code should use get_garmin_client() instead
def _garmin_client_property() -> Garmin:
    """Deprecated: use get_garmin_client() instead."""
    logging.warning("Direct access to 'garmin_client' is deprecated. Use get_garmin_client() function instead.")
    return get_garmin_client()


# For backward compatibility with existing imports
# This allows `from account import garmin_client` to work, but triggers lazy loading
garmin_client = None  # Will be set on first access via __getattr__


def __getattr__(name: str):
    """Lazy loading of garmin_client for backward compatibility."""
    if name == 'garmin_client':
        return get_garmin_client()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


# Athlete performance profile - loaded lazily via functions
def get_athlete_config() -> dict:
    """Load athlete performance configuration from environment.
    
    Returns:
        dict: Athlete configuration with vV02, fmin, zones, FTP values
    """
    return {
        'vV02': Pace(config('vV02')),
        'fmin': int(config('fmin')),
        'rfmax': int(config('rfmax')),
        'cfmax': int(config('cfmax')),
        'sfmax': int(config('sfmax')),
        'rflt': int(config('rflt')),
        'cflt': int(config('cflt')),
        'sflt': int(config('sflt')),
        'rFTP': Power(config('rFTP')),
        'cFTP': Power(config('cFTP')),
        'BOT_TOKEN': config('BOT_TOKEN'),
    }


# Convenience exports for common config values (lazy-loaded)
def get_vV02():
    """Get critical velocity (vVO2) pace."""
    return get_athlete_config()['vV02']


def get_fmin():
    """Get minimum resting heart rate."""
    return get_athlete_config()['fmin']
