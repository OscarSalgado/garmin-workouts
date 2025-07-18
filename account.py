from garminworkouts.models.pace import Pace
from garminworkouts.models.power import Power
from decouple import config

EMAIL: str | bool = config('GARMIN_USERNAME')
PASSWORD: str | bool = config('GARMIN_PASSWORD')
locale = 'en-US'
vV02 = Pace(config('vV02'))  # type: ignore


fmin = int(config('fmin'))
rfmax = int(config('rfmax'))
rflt = int(config('rflt'))
rFTP = Power(config('rFTP'))  # type: ignore
cfmax = int(config('cfmax'))
cflt = int(config('cflt'))
cFTP = Power(config('cFTP'))  # type: ignore
sfmax = int(config('sfmax'))
sflt = int(config('sflt'))
BOT_TOKEN: str | bool = config('BOT_TOKEN')
intervals_api_key = config('intervals_api_key')
intervals_athlete_id = config('intervals_athlete_id')
