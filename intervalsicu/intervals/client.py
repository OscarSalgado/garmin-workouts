
from datetime import date, timedelta
from sklearn.linear_model import LinearRegression
import numpy as np
import logging
import os
import re
from intervalsicu.intervals.extraction import Extraction
from garminworkouts.models.workout import Workout
from intervalsicu.intervals.workout import IntervalsWorkout
from intervalsicu.intervals.threshold import IntervalsThreshold


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
        d1 = date(year=3000, month=1, day=1)
        d2 = date(year=1000, month=1, day=1)
        for workout in workouts:
            day_d, *_ = workout.get_workout_date()
            if day_d < d1:
                d1 = day_d
            if day_d > d2:
                d2 = day_d

        trainings: dict = {'trainings': []}
        trainings['trainings'] = workouts

        start_date = date.today() + timedelta(days=1) + timedelta(weeks=0)
        if d1 > start_date:
            start_date = d1

        # Calculate the Monday before or equal to start_date
        monday_before = start_date - timedelta(days=start_date.weekday())

        # Find the next Sunday after start_date
        days_until_sunday = (6 - start_date.weekday()) % 7
        end_date = start_date + timedelta(days=days_until_sunday) + timedelta(weeks=3)
        if end_date > d2:
            end_date = d2
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

    def export_workouts(self) -> None:
        list_folders = self.list_folders()

        for folder in list_folders:
            if folder.get('type', "") == "FOLDER":
                workouts = folder.get('children', [])
                folder_name = './workouts/' + folder.get('name', "")
                os.makedirs(folder_name, exist_ok=True)

                for workout in workouts:
                    cname = workout.get('name', "")
                    # Remove illegal characters from cname
                    cname = re.sub(r'[.<>:"/\\|?*]', '_', cname)
                    workout_name = folder_name + '/' + cname + '.yaml'
                    self.export_workout(workout, workout_name)
                    logging.info("Exported workout '%s'", workout_name)

    def export_workout(self, workout, workout_name: str) -> None:
        # Implement the logic to export a single workout
        Extraction.workout_export_yaml(workout, workout_name)

    def compute_aerobic_threshold(self):
        # Read the data
        activities = self.get_activities(start_date=date.today()-timedelta(days=365), end_date=date.today())

        for act in activities:
            if 'Ride' in act.get('type', '') or 'Run' in act.get('type', ''):
                logging.info("Processing activity ID: %s", act.get('id', 'Unknown ID'))
                # Implement logic to fetch and process HRV data for each activity
                # For demonstration, we will assume HRV data is fetched and stored in a CSV file
                hrv = self.get_activity_stream(act.get('id', None), 'hrv')
                RRs = IntervalsThreshold.read_RR_intervals(hrv)

                if len(RRs) > 1000:
                    df = IntervalsThreshold.remove_artifacts(RRs)
                    features_df = IntervalsThreshold.computeFeatures(df)
                    length = len(features_df['alpha1'])

                    if length > 0 and max(features_df['heartrate']) > 100:
                        reg = LinearRegression().fit(
                            features_df['alpha1'].values.reshape(length, 1),
                            features_df['heartrate'].values.reshape(length, 1))
                        prediction_LT1 = reg.predict(np.array(0.75).reshape(1, 1))
                        prediction_LT2 = reg.predict(np.array(0.5).reshape(1, 1))

                        if prediction_LT1[0][0] < max(features_df['heartrate']):
                            print("Date:", act.get('start_date_local', 'Unknown Date'))
                            print('LT1 (alpha1=0.75): ', round(prediction_LT1[0][0], 2), ' bpm')
                            if prediction_LT2[0][0] < max(features_df['heartrate']):
                                print('LT2 (alpha1=0.5): ', round(prediction_LT2[0][0], 2), ' bpm')
                            print('-----------------------------------')
            else:
                logging.warning("No valid HRV data found for type : %s", act.get('type', ''))
