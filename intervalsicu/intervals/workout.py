from datetime import date, timedelta
import logging
import intervalsicu.intervals.api as IntervalsAPI


class IntervalsWorkout(IntervalsAPI.IntervalsAPI):
    """
    IntervalsWorkout for managing workouts with Intervals.icu.
    Inherits from IntervalsAPI to utilize its methods.
    """
    @staticmethod
    def convert_duration(duration):
        if duration.endswith("km"):
            return float(duration[:-2]) * 1000  # km to meters
        if duration.endswith("m"):
            return int(duration[:-1]) * 60      # min to seconds
        if duration.endswith("s"):
            return int(duration[:-1])           # seconds
        try:
            return int(duration)
        except Exception:
            return 0

    # Expand repeated intervals into separate blocks
    def expand_repeats(self, fmax, threshold_pace, steps):
        expanded_steps = []
        for step in steps:
            step_type = step.get('stepType', {}).get('stepTypeKey', '')
            if step_type == 'interval':
                expanded_steps.append(self.step_format(fmax, threshold_pace, step))
            elif step_type == 'repeat':
                substeps = [
                    self.step_format(fmax, threshold_pace, substep)
                    for substep in step.get('workoutSteps', [])
                ]
                duration = sum(sub.get('duration', 0) for sub in substeps)
                distance = sum(sub.get('distance', 0) for sub in substeps)
                reps = str(step.get('numberOfIterations', 1))
                repeat_step = {
                    'reps': reps,
                    'text': f"{reps}x",
                    'steps': substeps,
                }
                if duration > 0:
                    repeat_step['duration'] = duration
                if distance > 0:
                    repeat_step['distance'] = distance
                expanded_steps.append(repeat_step)
            else:
                step['description'] = ''
                expanded_steps.append(step)
        return expanded_steps

    def step_format(self, fmax, threshold_pace, step):
        # Use local vars to avoid repeated dict lookups
        step_type = step.get('stepType', {}).get('stepTypeKey', '')
        end_condition = step.get('endCondition', {}).get('conditionTypeKey', '')
        end_value = step.get('endConditionValue')
        target_type = step.get('targetType', {}).get('workoutTargetTypeKey', '')
        desc = step.get('description', '')

        # Set duration or distance
        if end_condition == 'time':
            step['duration'] = int(end_value)
        elif end_condition == 'distance':
            step['distance'] = int(end_value)

        # Heart rate zone
        if target_type == 'heart.rate.zone':
            start = str(round(step.get("targetValueOne", 0) / fmax * 100)) if fmax else '0'
            end = str(round(step.get("targetValueTwo", 0) / fmax * 100)) if fmax else '0'
            step['hr'] = {'units': '%hr', 'start': start, 'end': end}
            desc += f" {start}-{end}% HR intensity={step_type}"

        # Pace zone
        elif target_type == 'pace.zone':
            start = str(round(step.get("targetValueOne", 0) / threshold_pace * 100)) if threshold_pace else '0'
            end = str(round(step.get("targetValueTwo", 0) / threshold_pace * 100)) if threshold_pace else '0'
            step['pace'] = {'units': '%pace', 'start': start, 'end': end}
            desc += f" {start}-{end}% Pace  intensity={step_type}"

        step['description'] = desc
        step['text'] = desc

        # Remove unwanted keys efficiently
        remove_keys = {
            "type", "stepId", "stepOrder", "childStepId", 'stepType', "endCondition", "preferredEndConditionUnit",
            "endConditionValue", "endConditionCompare", "endConditionZone", "category", "exerciseName",
            "targetType", 'targetValueOne', 'targetValueTwo', 'zoneNumber',
            'secondaryTargetType', 'secondaryTargetValueOne', 'secondaryTargetValueTwo', 'secondaryZoneNumber'
        }
        return {k: v for k, v in step.items() if k not in remove_keys}

    # Format training data for API submission
    def format_training_data(self, workouts, plan_id=None, day_a=date.today(), day_b=date.today() + timedelta(days=1)):
        self.update_athlete_data(workouts)

        sp = {}
        for sport in ['Run', 'Swim', 'Ride']:
            # Fetch sport settings for each sport
            sport_settings = self.get_sport_settings(sport=sport)
            threshold_pace = sport_settings.get('threshold_pace') if sport_settings else None
            max_hr = sport_settings.get('max_hr') if sport_settings else None
            sp[sport] = {
                'threshold_pace': threshold_pace,
                'max_hr': max_hr
            }

        formatted_data = []

        for workout in workouts["trainings"]:
            sport_settings = sp.get(IntervalsWorkout.format_sport(workout))
            threshold_pace = sport_settings.get('threshold_pace') if sport_settings else None
            max_hr = sport_settings.get('max_hr') if sport_settings else None

            day_d, *_ = workout.get_workout_date()
            if day_d >= day_a and day_d <= day_b:
                description_lines = []
                expanded_steps = self.expand_repeats(
                    max_hr,
                    threshold_pace,
                    workout._steps(workout.config.get('steps', [])))

                for step in expanded_steps:
                    self.duration_string(description_lines, step)

                    for d in description_lines:
                        if "x" in d and description_lines.index(d) != 0:
                            description_lines[description_lines.index(d)] = "\n" + d

                formatted_data.append({
                    "athlete_id": self.athlete_id,
                    "folder_id": plan_id,
                    "name": workout.get_workout_name(),
                    "category": "WORKOUT",
                    "type": IntervalsWorkout.format_sport(workout),
                    "sub_type": workout.config.get("sub_type", None),
                    "color": None,
                    "description": "\n".join(description_lines).strip(),
                    "start_date_local": day_d.isoformat() + "T00:00:00",
                    "moving_time": workout.sec,
                    "steps": expanded_steps,
                    "attachments": [],
                })
        return formatted_data

    def update_athlete_data(self, workouts):
        max_hr = workouts['trainings'][0].fmax
        lthr = workouts['trainings'][0].flt
        resting_hr = workouts['trainings'][0].fmin
        self.update_resting_hr(resting_hr=resting_hr)

        for s in ['Run', 'Swim', 'Ride']:
            sport_settings = self.get_sport_settings(sport=s)
            if sport_settings and 'id' in sport_settings:
                if s == 'Run':
                    tp = float(workouts['trainings'][0].target['R2']['min'])
                    VAM = workouts['trainings'][0].vVO2.to_pace()
                    self.update_threshold_pace(threshold_pace=tp * VAM, id=sport_settings['id'])
                    self.update_max_hr(max_hr=max_hr, id=sport_settings['id'])
                    self.update_lthr(lthr=lthr, id=sport_settings['id'])
                    self.update_hrrc_min_percent(
                        hrrc_min_percent=90, id=sport_settings['id'])

                elif s == 'Ride':
                    self.update_max_hr(max_hr=max_hr, id=sport_settings['id'])
                    self.update_lthr(lthr=lthr, id=sport_settings['id'])
                    self.update_hrrc_min_percent(
                        hrrc_min_percent=90, id=sport_settings['id'])
                elif s == 'Swim':
                    self.update_max_hr(max_hr=max_hr, id=sport_settings['id'])
                    self.update_lthr(lthr=lthr, id=sport_settings['id'])
                    self.update_hrrc_min_percent(
                        hrrc_min_percent=90, id=sport_settings['id'])

    @staticmethod
    def duration_string(description_lines, step):
        # Fast path for duration
        if 'duration' in step and 'reps' not in step:
            d = step['duration']
            h, rem = divmod(d, 3600)
            m, s = divmod(rem, 60)
            description_lines.append(
                f"- {IntervalsWorkout.format_duration_string(h, m, s)} in {step['description']}"
            )
        # Fast path for distance
        elif 'distance' in step and 'reps' not in step:
            k = round(step['distance'] / 1000, 2)
            description_lines.append(f"- {k}km in {step['description']}")
        # Fast path for repeats
        elif 'reps' in step:
            description_lines.append(f"{step['reps']}x")
            for substep in step.get('steps', []):
                if 'duration' in substep:
                    d = substep['duration']
                    h, rem = divmod(d, 3600)
                    m, s = divmod(rem, 60)
                    description_lines.append(
                        f"  - {IntervalsWorkout.format_duration_string(h, m, s)} in {substep['description']}"
                    )
                elif 'distance' in substep:
                    k = round(substep['distance'] / 1000, 2)
                    description_lines.append(f"  - {k}km in {substep['description']}")

    @staticmethod
    def format_duration_string(h, m, s):
        # Fast string formatting, avoids unnecessary checks
        return (
            (f"{int(h)}h" if h else "") +
            (f"{int(m)}m" if m else "") +
            (f"{int(s)}s" if s else "")
        )

    # Upload training data to Intervals.icu
    def upload_workouts(self, data):
        url = f"{IntervalsWorkout.BASE_URL}/{self.athlete_id}/workouts/bulk"
        response = self.post(url, json=data)
        if response.status_code == 200:
            logging.info("Workouts uploaded successfully.")
        else:
            logging.error(f"Failed to upload workouts. Status code: {response.status_code}")
            logging.error(response.text)

    # Upload training data to Intervals.icu
    def upload_events(self, data):
        url = f"{IntervalsWorkout.BASE_URL}/{self.athlete_id}/events/bulk"
        response = self.post(url, json=data)
        if response.status_code == 200:
            logging.info("Events uploaded successfully.")
        else:
            logging.error(f"Failed to upload events. Status code: {response.status_code}")
            logging.error(response.text)

    @staticmethod
    def format_sport(workout):
        sport = workout.config.get("sport", "").lower()
        if "cycl" in sport:
            return "Ride"
        if "run" in sport:
            return "Run"
        if "swim" in sport:
            return "Swim"
        return "Other"

    def list_workouts(self):
        url: str = f"{IntervalsWorkout.BASE_URL}/{self.athlete_id}/workouts"
        response = self.get(url)
        return response.json()

    def list_folders(self):
        url: str = f"{IntervalsWorkout.BASE_URL}/{self.athlete_id}/folders"
        response = self.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch folders. Status code: {response.status_code}")
            return []

    def list_workout_folders(self):
        folders = self.list_folders()
        workout_folders = {folder.get('name', ''): folder for folder in folders if folder.get('type') == 'FOLDER'}
        return workout_folders

    def list_plans(self):
        folders = self.list_folders()
        plans = {folder.get('name', ''): folder for folder in folders if folder.get('type') == 'PLAN'}
        return plans

    def delete_range_events(self):
        url: str = f"{IntervalsWorkout.BASE_URL}/{self.athlete_id}/events"
        start_date = date.today() + timedelta(days=1)
        params = {
            'oldest': start_date.isoformat(),
            'category': ["WORKOUT", "TARGET"],
        }
        response = self.delete(url, params=params)
        if response.status_code == 200:
            logging.info("Events in range deleted successfully.")
        else:
            logging.error(f"Failed to delete events in range. Status code: {response.status_code}")
            logging.error(response.text)

    def get_sport_settings(self, sport):
        """
        Fetch the sport settings for the athlete.
        """
        url = f"{IntervalsWorkout.BASE_URL}/{self.athlete_id}/sport-settings"
        response = self.get(url)
        if response.status_code == 200:
            sport_settings = response.json()
            for s in sport_settings:
                if s.get("types")[0] == sport:
                    return s
                if s.get("types")[0] == 'Other':
                    return s
        else:
            logging.error(f"Failed to fetch sport settings. Status code: {response.status_code}")
            logging.error(response.text)
            return {}

    def update_threshold_pace(self, threshold_pace: float, id) -> None:
        """
        Update the threshold pace in Intervals.icu.
        """
        url = f"{IntervalsWorkout.BASE_URL}/{self.athlete_id}/sport-settings/{id}"
        payload = {"threshold_pace": threshold_pace}
        params = {"recalcHrZones": 'true'}
        response = self.put(url, json=payload, params=params)
        if response.status_code == 200:
            logging.info("Threshold pace updated successfully. Id: %s", id)
        else:
            logging.error(f"Failed to update threshold pace. Status code: {response.status_code}")
            logging.error(response.text)

    def update_max_hr(self, max_hr: int, id) -> None:
        """
        Update the maximum heart rate in Intervals.icu.
        """
        url = f"{IntervalsWorkout.BASE_URL}/{self.athlete_id}/sport-settings/{id}"
        payload = {"max_hr": max_hr}
        params = {"recalcHrZones": 'true'}
        response = self.put(url, json=payload, params=params)
        if response.status_code == 200:
            logging.info("Maximum heart rate updated successfully. Id: %s", id)
        else:
            logging.error(f"Failed to update maximum heart rate. Status code: {response.status_code}")
            logging.error(response.text)

    def update_resting_hr(self, resting_hr: int) -> None:
        """
        Update the resting heart rate in Intervals.icu.
        """
        url = f"{IntervalsWorkout.BASE_URL}/{self.athlete_id}"
        payload = {"applyToAll": False, "icu_resting_hr": resting_hr, "localDate": date.today().isoformat()}
        response = self.put(url, json=payload)
        if response.status_code == 200:
            logging.info("Resting heart rate updated successfully.")
        else:
            logging.error(f"Failed to update resting heart rate. Status code: {response.status_code}")
            logging.error(response.text)

    def update_lthr(self, lthr: int, id) -> None:
        """
        Update the lactate threshold heart rate in Intervals.icu.
        """
        url = f"{IntervalsWorkout.BASE_URL}/{self.athlete_id}/sport-settings/{id}"
        payload = {"lthr": lthr}
        params = {"recalcHrZones": 'true'}
        response = self.put(url, json=payload, params=params)
        if response.status_code == 200:
            logging.info("Lactate threshold heart rate updated successfully. Id: %s", id)
        else:
            logging.error(f"Failed to update lactate threshold heart rate. Status code: {response.status_code}")
            logging.error(response.text)

    def update_hrrc_min_percent(self, hrrc_min_percent: float, id) -> None:
        """
        Update the heart rate reserve calculation minimum percentage in Intervals.icu.
        """
        url = f"{IntervalsWorkout.BASE_URL}/{self.athlete_id}/sport-settings/{id}"
        payload = {"hrrc_min_percent": hrrc_min_percent}
        params = {"recalcHrZones": 'true'}
        response = self.put(url, json=payload, params=params)
        if response.status_code == 200:
            logging.info("Heart rate reserve calculation minimum percentage updated successfully. Id: %s", id)
        else:
            logging.error(
                f"Failed to update heart rate reserve calculation minimum percentage. "
                f"Status code: {response.status_code}"
            )
            logging.error(response.text)

    def set_target(self, monday, mileage, duration):
        """
        Set a target for the week in Intervals.icu.
        """
        url = f"{IntervalsWorkout.BASE_URL}/{self.athlete_id}/targets"
        payload = {
            "start_date_local": monday.isoformat() + "T00:00:00",
            "mileage": mileage,
            "duration": duration
        }
        response = self.post(url, json=payload)
        if response.status_code == 200:
            logging.info("Target set successfully.")
        else:
            logging.error(f"Failed to set target. Status code: {response.status_code}")
            logging.error(response.text)
