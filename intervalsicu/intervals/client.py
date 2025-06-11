
from datetime import date, timedelta
import logging
from garminworkouts.models.workout import Workout
from intervalsicu.intervals.workout import IntervalsWorkout


class IntervalsClient(IntervalsWorkout):

    def update_workouts_(self, workouts: list[Workout], plan_folder) -> None:
        trainings: dict = {'trainings': []}
        trainings['trainings'] = workouts

        start_date_str = plan_folder.get('start_date_local', None)
        start_date = date.fromisoformat(start_date_str.split('T')[0]) if start_date_str else date.today()
        end_date = date.today() + timedelta(weeks=18)
        formatted_payload = self.format_training_data(
            trainings, plan_id=plan_folder.get('id', None), day_a=start_date, day_b=end_date)
        self.upload_workouts(formatted_payload)

    def set_targets(self, workouts, day_a: date, day_b: date) -> None:
        # Encuentra los días que son lunes entre day_a y day_b
        data = []
        for sport in ['Run', 'Swim', 'Ride']:
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

    def update_events_(self, workouts: list[Workout], plan_folder) -> None:
        trainings: dict = {'trainings': []}
        trainings['trainings'] = workouts

        start_date = date.today() + timedelta(days=1)

        # Calculate the Monday before or equal to start_date
        if start_date.weekday() == 0:
            monday_before = start_date
        else:
            monday_before = start_date - timedelta(days=start_date.weekday())

        # Find the next Sunday after start_date
        days_until_sunday = (6 - start_date.weekday()) % 7
        end_date = start_date + timedelta(days=days_until_sunday) + timedelta(weeks=3)
        self.delete_range_events()
        self.set_targets(workouts, day_a=monday_before, day_b=end_date)
        formatted_payload = self.format_training_data(
            trainings, plan_id=plan_folder.get('id', None), day_a=start_date, day_b=end_date)
        self.upload_events(formatted_payload)

    def update_workouts(self, workouts: list[Workout], plan: str) -> None:
        existing_plans = self.list_plans()

        plan_folder = self.create_plan_folder(workouts, plan, existing_plans)
        self.update_events_(workouts, plan_folder)
        workouts_by_name: dict[str, Workout] = {w.get_workout_name(): w for w in workouts}
        self.sync_plan_folder(workouts, workouts_by_name, plan_folder)

    def sync_plan_folder(self, workouts, workouts_by_name, plan_folder):
        self.update_workouts_(workouts=workouts, plan_folder=plan_folder)
        existing_workouts_by_name: dict = {w.get('name'): w for w in self.list_workouts()}
        for workout_name in existing_workouts_by_name.keys():
            id = existing_workouts_by_name[workout_name].get('id', None)
            w = workouts_by_name.get(workout_name)
            if w:
                d, _,  _ = w.get_workout_date()
                days_diff = (d - date.fromisoformat(plan_folder['start_date_local'].split('T')[0])).days
                self.update_workout(id, days_diff)

    def create_plan_folder(self, workouts, plan, existing_plans):
        d = date(year=3000, month=1, day=1)
        for workout in workouts:
            day_d, *_ = workout.get_workout_date()
            if day_d < d:
                d = day_d

        if plan in existing_plans.keys():
            plan_folder = existing_plans[plan]
            self.delete_plan(plan_folder.get('id', None))

        plan_folder = self.create_plan(plan_name=plan, d=d)
        logging.info("Plan '%s'", plan)

        return plan_folder

    def create_plan(self, plan_name: str, d: date):
        """
        Create a new plan folder in Intervals.icu.
        """
        url = f"{self.BASE_URL}/{self.athlete_id}/folders"
        payload = {
            "auto_rollout_day": 7,
            "name": plan_name,
            "rollout_weeks": 2,
            "start_date_local": f"{d.isoformat()}T00:00:00",
            "starting_atl": -1,
            "starting_ctl": -1,
            "type": "PLAN"
        }
        return self.post(url, json=payload).json()

    def delete_plan(self, plan_id: str):
        """
        Delete a plan folder in Intervals.icu.
        """
        url = f"{self.BASE_URL}/{self.athlete_id}/folders/{plan_id}"
        self.delete(url)

    def update_workout(self, workout_id: str, days_diff: int):
        """
        Update a workout in Intervals.icu.
        """
        url = f"{self.BASE_URL}/{self.athlete_id}/workouts/{workout_id}"
        payload = {
            "day": days_diff
        }
        self.put(url, json=payload)
