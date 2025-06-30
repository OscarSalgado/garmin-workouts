
from datetime import date, timedelta
import logging
from garminworkouts.models.workout import Workout
from intervalsicu.intervals.workout import IntervalsWorkout


class IntervalsClient(IntervalsWorkout):

    def update_workouts(self, workouts: list[Workout], plan: str) -> None:
        existing_plans = self.list_plans()

        plan_folder = self.get_plan_folder(workouts, plan, existing_plans)
        self.update_events_(workouts, plan_folder)

    def get_plan_folder(self, workouts, plan, existing_plans):
        d = date(year=3000, month=1, day=1)
        for workout in workouts:
            day_d, *_ = workout.get_workout_date()
            if day_d < d:
                d = day_d

        monday_before = d - timedelta(days=d.weekday())

        if plan in existing_plans.keys():
            plan_folder = existing_plans[plan]
            if len(plan_folder.get('children', [])) == 0:
                self.delete_plan(plan_folder.get('id', None))
                wellness = self.get_wellness(date=monday_before)
                plan_folder = self.create_plan(plan_name=plan,
                                               d=monday_before,
                                               ctl=wellness.get('ctl', -1),
                                               atl=wellness.get('atl', -1))
                logging.info("Plan '%s'", plan)
        else:
            wellness = self.get_wellness(date=d)
            plan_folder = self.create_plan(plan_name=plan,
                                           d=d,
                                           ctl=wellness.get('ctl', -1),
                                           atl=wellness.get('atl', -1))
            logging.info("Plan '%s'", plan)

        return plan_folder

    def update_events_(self, workouts: list[Workout], plan_folder) -> None:
        trainings: dict = {'trainings': []}
        trainings['trainings'] = workouts

        start_date = date.today() + timedelta(days=1) + timedelta(weeks=0)

        # Calculate the Monday before or equal to start_date
        monday_before = start_date - timedelta(days=start_date.weekday())

        # Find the next Sunday after start_date
        days_until_sunday = (6 - start_date.weekday()) % 7
        end_date = start_date + timedelta(days=days_until_sunday) + timedelta(weeks=3)
        self.delete_range_events(monday_before, end_date)
        self.set_targets(workouts, day_a=monday_before, day_b=end_date)
        formatted_payload = self.format_training_data(
            trainings, plan_folder=plan_folder, day_a=monday_before, day_b=end_date)
        if len(formatted_payload) > 0:
            self.upload_events(formatted_payload)
        else:
            logging.warning("No events to upload for plan '%s'", plan_folder.get('name', 'Unknown Plan'))

    def update_training_plan(self, workouts: list[Workout], plan: str) -> None:
        existing_plans = self.list_plans()

        plan_folder = self.get_plan_folder(workouts, plan, existing_plans)
        self.sync_plan_folder(workouts, plan_folder)

    def sync_plan_folder(self, workouts, plan_folder):
        start_date_str = plan_folder.get('start_date_local', None)
        start_date = date.fromisoformat(start_date_str.split('T')[0]) if start_date_str else date.today()
        end_date = start_date  # + timedelta(weeks=18)

        workout_list = plan_folder.get('children', [])
        existing_workouts_by_name: dict = {w.get('name', ''): w for w in workout_list} if workout_list else {}
        curated_list = []

        for workout in workouts:
            workout_name = workout.get_workout_name()
            d = workout.get_workout_date()[0]
            if d > end_date:
                end_date = d
            if workout_name in existing_workouts_by_name:
                existing_workouts_by_name.pop(workout_name, None)
            else:
                curated_list.append(workout)

        if len(curated_list) > 0:
            trainings: dict = {'trainings': []}
            trainings['trainings'] = curated_list

            formatted_payload = self.format_training_data(
                trainings, plan_folder=plan_folder, day_a=start_date, day_b=end_date)
            self.upload_workouts(formatted_payload)

        for name in existing_workouts_by_name:
            workout = existing_workouts_by_name[name]
            id = workout.get('id', None)
            self.delete_workout(id)
