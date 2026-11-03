from datetime import date

from requests import Response

import account
from garminworkouts.garmin.garmintypes import GarminTypes
from garminworkouts.models.power import Power
from garminworkouts.models.workout import Workout


class GarminBiometric(GarminTypes):
    _BIOMETRIC_SERVICE_ENDPOINT = "/biometric-service"

    def get_hr_zones(self) -> dict:
        url: str = f"{self._BIOMETRIC_SERVICE_ENDPOINT}/heartRateZones"
        return self.get(url).json()

    def save_hr_zones(self, zones) -> Response:
        url: str = f"{self._BIOMETRIC_SERVICE_ENDPOINT}/heartRateZones"
        return self.put(url, json=zones)

    def get_power_zones(self) -> dict:
        url: str = f"{self._BIOMETRIC_SERVICE_ENDPOINT}/powerZones/sports/all"
        return self.get(url).json()

    def save_power_zones(self, zones) -> Response:
        url: str = f"{self._BIOMETRIC_SERVICE_ENDPOINT}/powerZones/all"
        return self.put(url, json=zones)

    def user_zones(self) -> None:
        athlete_config = account.get_athlete_config()
        _, _, data = Workout(
            [],
            [],
            athlete_config['vV02'],
            athlete_config['fmin'],
            athlete_config['rfmax'],
            athlete_config['rflt'],
            athlete_config['rFTP'],
            athlete_config['cfmax'],
            athlete_config['cflt'],
            athlete_config['cFTP'],
            athlete_config['sfmax'],
            athlete_config['sflt'],
            '',
            date.today()).hr_zones()

        _, _, _, pdata = Power.power_zones(athlete_config['rFTP'], athlete_config['cFTP'])

        self.save_hr_zones(data)
        self.save_power_zones(pdata)

        Workout([],
                [],
                athlete_config['vV02'],
                athlete_config['fmin'],
                athlete_config['rfmax'],
                athlete_config['rflt'],
                athlete_config['rFTP'],
                athlete_config['cfmax'],
                athlete_config['cflt'],
                athlete_config['cFTP'],
                athlete_config['sfmax'],
                athlete_config['sflt'],
                '',
                date.today()
                ).zones()
