"""Account and authentication configuration for the application.

Single source of Garmin credentials and token store location, shared by the CLI,
the Docker bot and the GitHub workflows.

Environment variables (environment or ``.env``):
    GARMIN_USERNAME / GARMIN_PASSWORD  Garmin credentials (``EMAIL`` / ``PASSWORD`` are a
                                       deprecated fallback)
    GARMINTOKENS                       Token store path, default ``~/.garminconnect``
"""

import logging
from getpass import getpass
from pathlib import Path
from typing import Optional
from garminworkouts.models.pace import Pace
from garminworkouts.models.power import Power
from decouple import config

__all__ = ['get_credentials', 'get_tokenstore', 'get_intervals_config', 'get_athlete_config', 'locale']

# Locale used for Garmin external workouts and training plans
locale = 'en-US'

DEFAULT_TOKENSTORE = '~/.garminconnect'

# Module-level cache for lazy-initialized objects
_intervals_config: Optional[dict] = None


def get_mfa() -> str:
    """Prompt for Garmin MFA one-time code.

    Returns:
        str: The MFA one-time code entered by the user.
    """
    return getpass("MFA one-time code: ")


def get_tokenstore() -> str:
    """Return the Garmin token store path (``GARMINTOKENS``, default ``~/.garminconnect``)."""
    return str(Path(str(config('GARMINTOKENS', default=DEFAULT_TOKENSTORE))).expanduser())


def get_credentials() -> tuple[Optional[str], Optional[str]]:
    """Load Garmin credentials from ``GARMIN_USERNAME`` / ``GARMIN_PASSWORD``.

    The deprecated ``EMAIL`` / ``PASSWORD`` names are used as a fallback, with a warning.
    Missing values are returned as ``None``.

    Returns:
        tuple: (username, password), each ``None`` when not configured
    """
    username = config('GARMIN_USERNAME', default=None) or None
    password = config('GARMIN_PASSWORD', default=None) or None
    legacy_username = config('EMAIL', default=None) or None
    legacy_password = config('PASSWORD', default=None) or None

    if (username is None and legacy_username) or (password is None and legacy_password):
        logging.warning("EMAIL/PASSWORD are deprecated; use GARMIN_USERNAME/GARMIN_PASSWORD instead.")

    return (username or legacy_username, password or legacy_password)


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
