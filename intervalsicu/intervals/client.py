
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

    def update_events_(self, workouts: list[Workout], plan_folder) -> None:
        trainings: dict = {'trainings': []}
        trainings['trainings'] = workouts

        start_date = date.today() + timedelta(days=1) + timedelta(weeks=0)

        # Calculate the Monday before or equal to start_date
            monday_before = start_date - timedelta(days=start_date.weekday())
        start_date = monday_before if monday_before >= start_date else start_date

        # Find the next Sunday after start_date
        days_until_sunday = (6 - start_date.weekday()) % 7
        end_date = start_date + timedelta(days=days_until_sunday) + timedelta(weeks=3)
        self.delete_range_events(start_date)
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
