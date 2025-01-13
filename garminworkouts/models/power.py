from dataclasses import dataclass
from typing import List, Dict


@dataclass(frozen=True)
class Power:
    power: str

    def to_watts(self, ftp) -> float:
        ftp = int(ftp)
        if not 0 <= ftp < 1000:
            raise ValueError(f'FTP must be between 0 [W] and 999 [W] but was {ftp}')

        if self._has_watt():
            absolute_power = float(self.power[:-1])
        elif self._has_percent():
            absolute_power = self._to_percent(self.power[:-1], ftp)
        else:
            absolute_power = self._to_absolute(self.power, ftp)

        if not 0 <= absolute_power < 5000:
            raise ValueError(f'Power must be between 0 [W] and 4999 [W] but was {absolute_power}')

        return round(absolute_power)

    def _has_watt(self) -> bool:
        return self.power.lower().endswith('w')

    def _has_percent(self) -> bool:
        return self.power.lower().endswith('%')

    @staticmethod
    def _to_percent(power: str, ftp: int) -> float:
        return round(float(power) * ftp / 100)

    @staticmethod
    def _to_absolute(power: str, ftp: int) -> float:
        return round(float(power) * ftp)

    @staticmethod
    def power_zones(rftp, cftp) -> tuple[List[float], List[int], List[int], List[Dict]]:
        zones = [0.65, 0.8, 0.9, 1.0, 1.15, 1.3, 1.5, 1.7]
        rpower_zones = [int(float(rftp.power[:-1]) * zone) for zone in zones]
        cpower_zones = [int(float(cftp.power[:-1]) * zone) for zone in zones]

        def create_zone_data(sport, ftp, power_zones):
            return {
                'sport': sport,
                'functionalThresholdPower': ftp.power[:-1],
                'zone1Floor': str(power_zones[0]),
                'zone2Floor': str(power_zones[1]),
                'zone3Floor': str(power_zones[2]),
                'zone4Floor': str(power_zones[3]),
                'zone5Floor': str(power_zones[4]),
                'zone6Floor': str(power_zones[5] if sport == 'CYCLING' else 0.0),
                'zone7Floor': str(power_zones[6] if sport == 'CYCLING' else 0.0),
                'userLocalTime': None
            }

        data = [
            create_zone_data('CYCLING', cftp, cpower_zones),
            create_zone_data('RUNNING', rftp, rpower_zones)
        ]

        return zones, rpower_zones, cpower_zones, data
