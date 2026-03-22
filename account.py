from garminworkouts.models.pace import Pace
from garminworkouts.models.power import Power
from decouple import config

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
