from dataclasses import dataclass
from datetime import timedelta


@dataclass(frozen=True)
class Time:
    duration: str

    def to_seconds(self) -> int:
        parts = list(map(int, self.duration.split(':')))
        if len(parts) == 1:
            hours, minutes, seconds = 0, 0, parts[0]
        elif len(parts) == 2:
            hours, minutes, seconds = 0, parts[0], parts[1]
        elif len(parts) == 3:
            hours, minutes, seconds = parts
        else:
            raise ValueError('Invalid duration format')

        if not (0 <= hours <= 23 and 0 <= minutes <= 59 and 0 <= seconds <= 59):
            raise ValueError('Invalid duration')

        return hours * 3600 + minutes * 60 + seconds

    @staticmethod
    def to_str(seconds: int) -> str:
        return str(timedelta(seconds=seconds))
