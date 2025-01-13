import unittest
from datetime import date, timedelta
from typing import Tuple
from garminworkouts.models.date import get_date


class TestGetDate(unittest.TestCase):
    def test_valid_date_conversion(self) -> None:
        race = date(2022, 1, 1)
        week_range = range(0, 30)
        day_range = range(1, 10)

        def days_from_RD(name: str, day: date):
            s = name.replace('R', '').replace('D', '').split('_')
            week = int(s[0])
            days = int(s[1]) if int(s[1]) < 8 else 0
            return day + timedelta(days=(week - 1) * 7 + days), -week, days

        def days_from_none(name: str, day: date):
            s = name.split('_')
            week = int(s[0])
            days = int(s[1]) if int(s[1]) < 8 else 0
            return day + timedelta(days=-(week + 1) * 7 + days), week, days

        names = [f'{q}{i}_{j}' for q in ['R', 'D'] for i in week_range for j in day_range]
        valid_dates = [(name, days_from_RD(name, race)) for name in names]

        for name, expected_date in valid_dates:
            with self.subTest():
                self.assertEqual(get_date(name, race, None), expected_date)

        names = [f'{i}_{j}' for i in week_range for j in day_range]
        valid_dates = [(name, days_from_none(name, race)) for name in names]

        for name, expected_date in valid_dates:
            with self.subTest():
                self.assertEqual(get_date(name, race, None), expected_date)

    def test_get_date_without(self) -> None:
        name = 'SampleNote'
        race = date(2022, 1, 1)
        expected_output: Tuple[date, int, int] = (date.today(), 0, 0)
        self.assertEqual(get_date(name, race, None), expected_output)

    def test_get_date_with_date_ini(self) -> None:
        name = 'Sample'
        race = date(2022, 1, 1)
        date_ini: dict[str, int] = {'year': 2023, 'month': 2, 'day': 15}
        expected_output: Tuple[date, int, int] = (date(2023, 2, 15), 0, 0)
        self.assertEqual(get_date(name, race, date_ini), expected_output)
