from dataclasses import dataclass
from typing import Union
from garminworkouts.models.time import Time
from garminworkouts.models.types import TYPE_MAPPING


@dataclass(frozen=True)
class Duration:
    duration: str

    def get_type(self) -> str:
        for key in TYPE_MAPPING:
            if key in self.duration:
                return TYPE_MAPPING[key]
        return 'time' if Duration.is_time(self.duration) else 'lap.button'

    @staticmethod
    def get_string(value: int, type: str) -> str:
        type_mapping = {
            'heart.rate': f"{value}ppm",
            'distance': f"{value}m" if value >= 100 else f"{value}km",
            'calories': f"{value}cals",
            'reps': f"{value}reps",
            'power': f"{value}w",
            'time': Time.to_str(value)
        }
        return type_mapping.get(type, '')

    @staticmethod
    def get_value(duration: str) -> Union[int, None]:
        for key, _ in TYPE_MAPPING.items():
            if key in duration:
                return int(float(duration.split(key)[0]))
        if Duration.is_time(duration):
            return Time(duration).to_seconds()
        return None

    @staticmethod
    def is_time(string: str) -> bool:
        return ':' in string

    @staticmethod
    def is_distance(string: str) -> bool:
        return 'm' in string or 'km' in string

    @staticmethod
    def is_reps(string: str) -> bool:
        return 'reps' in string

    @staticmethod
    def is_heart_rate(string: str) -> bool:
        return 'ppm' in string

    @staticmethod
    def is_power(string: str) -> bool:
        return 'w' in string

    @staticmethod
    def is_energy(string: str) -> bool:
        return 'cals' in string

    def to_seconds(self) -> int:
        return Time(self.duration).to_seconds()
