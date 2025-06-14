from datetime import date, timedelta
from intervalsicu.intervals.api import IntervalsAPI


class IntervalsTarget(IntervalsAPI):
    """A class to represent the target metrics for workouts in Intervals.icu."""

    def set_targets(self, workouts, day_a: date, day_b: date) -> None:
        # Encuentra los días que son lunes entre day_a y day_b
        data = []
        for sport in self.SUPPORTED_WORKOUT_TYPES:
            mondays, mileage, duration = self.get_sport_target_metrics(workouts, day_a, day_b, sport)

            self.set_targets_(data, sport, mondays, mileage, duration)
        self.upload_events(data)

    def get_sport_target_metrics(self, workouts, day_a, day_b, sport):
        mondays = []
        current_day = day_a
        while current_day <= day_b:
            if current_day.weekday() == 0:  # 0 es lunes
                mondays.append(current_day)
            current_day += timedelta(days=1)
        sundays = [monday + timedelta(days=6) for monday in mondays]  # Añade los domingos correspondientes
        # Inicializa un vector de ceros del tamaño de mondays
        mileage = [0] * len(mondays)
        duration = [0] * len(mondays)

        for w in workouts:
            if self.format_sport(w) == sport:
                d, _, _ = w.get_workout_date()
                for monday in mondays:
                    index = mondays.index(monday)
                    sunday = sundays[index]
                    if monday <= d <= sunday:
                        # Suma el kilometraje y la duración al índice correspondiente
                        if w.mileage is not None:
                            mileage[index] += w.mileage if sport == 'Run' else 0
                        if w.duration is not None:
                            duration[index] += w.duration.seconds
                        break
        return mondays, mileage, duration

    def set_targets_(self, data, sport, mondays, mileage, duration):
        for monday in mondays:
            if monday >= date.today():
                index = mondays.index(monday)
                data.append({
                    "category": "TARGET",
                    "type": sport,
                    "name": "Weekly",
                    "start_date_local": f"{monday.isoformat()}T00:00:00",
                    "load_target": 0,
                    "time_target": duration[index],
                    "distance_target": mileage[index] * 1000,
                })
