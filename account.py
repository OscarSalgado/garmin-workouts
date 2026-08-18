import logging
import sys
import os
from garminworkouts.models.pace import Pace
from garminworkouts.models.power import Power
from decouple import config
from garminconnect import Garmin


def get_mfa() -> str:
	"""Prompt for Garmin MFA one-time code.

	Returns:
		str: The MFA one-time code entered by the user.
	"""
	return input("MFA one-time code: ")


EMAIL: str | bool = config('GARMIN_USERNAME')
PASSWORD: str | bool = config('GARMIN_PASSWORD')

# Centralized Garmin API client used throughout the application
# Initialized with credentials and MFA callback for interactive authentication
garmin_client = Garmin(
	email=EMAIL,
	password=PASSWORD,
	prompt_mfa=get_mfa
)

# Configure token storage and login
tokenstore = "./.garminworkouts-cache/garmin"

# Check if we're in an interactive environment
is_interactive = sys.stdin.isatty() if hasattr(sys.stdin, 'isatty') else False

if is_interactive:
	# Check if tokenstore directory can be created/accessed
	tokenstore_dir = os.path.dirname(tokenstore)
	try:
		os.makedirs(tokenstore_dir, exist_ok=True)
		# Attempt login only in interactive environments
		garmin_client.login(tokenstore)
	except OSError as e:
		logging.warning("Cannot access tokenstore directory '%s': %s - skipping Garmin login", tokenstore_dir, e)
	except Exception as e:
		logging.warning("Garmin login failed: %s", e)
else:
	logging.info("Skipping Garmin login in non-interactive environment (CI/CD, tests, or background job)")

locale = 'en-US'
vV02 = Pace(config('vV02'))  # type: ignore


fmin = int(config('fmin'))
rfmax = int(config('rfmax'))
cfmax = int(config('cfmax'))
sfmax = int(config('sfmax'))
rflt = int(config('rflt'))
cflt = int(config('cflt'))
sflt = int(config('sflt'))
rFTP = Power(config('rFTP'))  # type: ignore
cFTP = Power(config('cFTP'))  # type: ignore
BOT_TOKEN: str | bool = config('BOT_TOKEN')
intervals_api_key = config('intervals_api_key')
intervals_athlete_id = config('intervals_athlete_id')
