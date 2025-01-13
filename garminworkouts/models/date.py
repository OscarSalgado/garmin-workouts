from datetime import date, timedelta


def get_date(name, race, date_ini) -> tuple[date, int, int]:
    try:
        parts = name.lstrip('RD').split('_')
        week = int(parts[0])
        week = -week if ('R' in name or 'D' in name) else week
        day = int(parts[1]) if len(parts) > 1 else int(name.split('D')[1].split('-')[0])
        day = day if day < 8 else 0
        return race - timedelta(weeks=week + 1) + timedelta(days=day), week, day
    except ValueError:
        if isinstance(date_ini, dict):
            return date(
                year=date_ini.get('year', 2024),
                month=date_ini.get('month', 1),
                day=date_ini.get('day', 1)), 0, 0
        else:
            return date.today(), 0, 0
