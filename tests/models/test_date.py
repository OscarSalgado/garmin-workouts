from datetime import date, timedelta
import pytest
from garminworkouts.models.date import get_date

race = date(2022, 1, 1)
date_ini: dict[str, int] = {'year': 2023, 'month': 2, 'day': 15}


def days_from_RD(name: str, day: date):
    s = name.replace('R', '').replace('D', '').split('_')
    week = int(s[0])
    days = int(s[1]) if int(s[1]) < 8 else 0
    return day + timedelta(days=(week - 1) * 7 + days), -week, days


def days_from_W(name: str, day: date):
    s = name.replace('W', '').replace('D', '').split('-')
    week = int(s[0])
    days = int(s[1]) if int(s[1]) < 8 else 0
    return day + timedelta(days=(week - 1) * 7 + days), -week, days


def days_from_none(name: str, day: date):
    s = name.split('_')
    week = int(s[0])
    days = int(s[1]) if int(s[1]) < 8 else 0
    return day + timedelta(days=-(week + 1) * 7 + days), week, days


def days_from_D(name: str, day: date):
    s = name.replace('D', '').split('_')
    week = int(0)
    days = int(s[0])
    return day + timedelta(days=-(week + 1) * 7 + days), week, days


def create_test_list():
    week_range = range(0, 30)
    day_range = range(1, 10)

    names = [f'{q}{i}_{j}' for q in ['R', 'D'] for i in week_range for j in day_range]
    valid_dates = [(name, None, days_from_RD(name, race)) for name in names]

    names = [f'{i}_{j}' for i in week_range for j in day_range]
    valid_dates += [(name, None, days_from_none(name, race)) for name in names]

    names = [f'W{i:02d}-D{j}' for i in week_range for j in day_range]
    valid_dates += [(name, None, days_from_W(name, race)) for name in names]

    names = [f'D{i}' for i in week_range]
    valid_dates += [(name, None, days_from_D(name, race)) for name in names]

    valid_dates += [('SampleNote', None, (date.today(), 0, 0))]
    valid_dates += [('SampleNote', date_ini, (date(2023, 2, 15), 0, 0))]

    return valid_dates


@pytest.mark.parametrize("name, ini, tuple", create_test_list())
def test_get_date(name, ini, tuple):
    date, week, day = tuple
    assert get_date(name, race, ini) == (date, week, day)
