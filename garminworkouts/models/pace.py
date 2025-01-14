from dataclasses import dataclass
from garminworkouts.models.time import Time


@dataclass(frozen=True)
class Pace:
    pace: str

    def to_seconds(self) -> int:
        t: int = Time(self.pace).to_seconds()
        return t if t > 20 else 20

    def to_speed(self) -> float:
        return 1000.0 / self.to_seconds()

    def to_pace(self, vVO2=None, diff=float(0)) -> float:
        if vVO2:
            vVO2s = Time(vVO2).to_seconds()
            if not 0 <= vVO2s < 1000:
                raise ValueError('vVO2 must be between 0 [s] and 1000 [s] but was %s' % vVO2s)
        else:
            vVO2s = self.to_seconds()

        if not self._has_time():
            raise ValueError('Pace must have time')

        absolute_pace = self.to_speed()
        return 1.0 / (1.0 / absolute_pace + diff / 1000)

    def _has_time(self) -> bool:
        return ':' in self.pace

    @staticmethod
    def _to_absolute(pace, vVO2) -> float:
        return pace * vVO2 / 100
