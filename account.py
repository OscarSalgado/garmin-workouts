from garminworkouts.models.pace import Pace
from garminworkouts.models.power import Power
from decouple import config


def get_mfa() -> str:
	"""Prompt for Garmin MFA one-time code.

	Returns:
		str: The MFA one-time code entered by the user.
	"""
	return input("MFA one-time code: ")


EMAIL: str | bool = config('GARMIN_USERNAME')
PASSWORD: str | bool = config('GARMIN_PASSWORD')
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
