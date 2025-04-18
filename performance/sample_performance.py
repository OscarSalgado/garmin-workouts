
from datetime import date
from garminworkouts.models.duration import Duration
from garminworkouts.models.pace import Pace

Races = {
    '1km': [date(day=24, month=9, year=2023), Duration('6:00').to_seconds(), Pace('3:44').to_speed()],
    'mile': [date(day=24, month=9, year=2023), Duration('8:40').to_seconds(), Pace('3:52').to_speed()],
}
