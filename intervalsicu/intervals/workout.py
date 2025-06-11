from datetime import date, timedelta
import logging
from math import floor
import intervalsicu.intervals.api as IntervalsAPI


class IntervalsWorkout(IntervalsAPI.IntervalsAPI):
    """
    IntervalsWorkout for managing workouts with Intervals.icu.
    Inherits from IntervalsAPI to utilize its methods.
    """
    @staticmethod
    def convert_duration(duration):
        if "km" in duration:
            return float(duration.replace("km", "")) * 1000  # Convert km to meters
        elif "m" in duration and not duration.endswith("km"):
            return int(duration.replace("m", "")) * 60  # Convert minutes to seconds
        elif "s" in duration:
            return int(duration.replace("s", ""))  # Keep seconds as is
        else:
            return int(duration)  # Default for unknown formats

    # Expand repeated intervals into separate blocks
    def expand_repeats(self, fmax, vVO2, steps):
        expanded_steps = []
        for step in steps:
            if step.get('stepType').get('stepTypeKey') == 'interval':
                step = self.step_format(fmax, vVO2, step)
            elif step.get('stepType').get('stepTypeKey') == 'repeat':
                expanded_substeps = []

                duration = 0
                distance = 0
                for substep in step.get('workoutSteps', []):
                    substep = self.step_format(fmax, vVO2, substep)
                    duration += substep.get('duration', 0)
                    distance += substep.get('distance', 0)
                    substep['description'] = f"{substep.get('description', '')}"
                    expanded_substeps.append(substep)

                step = {
                    'reps': str(step.get('numberOfIterations', 1)),
                    'text': str(step.get('numberOfIterations', 1)) + "x",
                    'steps': expanded_substeps,
                }
                if duration > 0:
                    step['duration'] = duration
                if distance > 0:
                    step['distance'] = distance
            else:
                step['description'] = ''

            expanded_steps.append(step)
        return expanded_steps

    def step_format(self, fmax, vVO2, step):
        step['text'] = step.get('description', '')

        intensity = step.get('stepType').get('stepTypeKey', '')
        if step.get('endCondition').get('conditionTypeKey') == 'time':
            step['duration'] = int(step['endConditionValue'])
        elif step.get('endCondition').get('conditionTypeKey') == 'distance':
            step['distance'] = int(step['endConditionValue'])

        if step.get('targetType').get('workoutTargetTypeKey') == 'heart.rate.zone':
            start = str(round(step["targetValueOne"] / fmax * 100)) if fmax else '0'
            end = str(round(step["targetValueTwo"] / fmax * 100)) if fmax else '0'
            step['hr'] = {
                'units': '%hr',
                'start': start,
                'end': end
            }
            step['description'] += f" {start}-{end}% HR intensity={intensity}"

        elif step.get('targetType').get('workoutTargetTypeKey') == 'pace.zone':
            start = str(round(step["targetValueOne"] / vVO2 * 100)) if fmax else '0'
            end = str(round(step["targetValueTwo"] / vVO2 * 100)) if fmax else '0'
            step['pace'] = {
                'units': '%pace',
                'start': start,
                'end': end
            }
            step['description'] += f" {start}-{end}% Pace  intensity={intensity}"

        step['text'] = step.get('description', '')

        step = {k: v for k, v in step.items() if k not in (
                "type", "stepId", "stepOrder", "childStepId", 'stepType', "endCondition", "preferredEndConditionUnit",
                "endConditionValue", "endConditionCompare", "endConditionZone", "category", "exerciseName",
                "targetType", 'targetValueOne', 'targetValueTwo', 'zoneNumber',
                'secondaryTargetType', 'secondaryTargetValueOne', 'secondaryTargetValueTwo', 'secondaryZoneNumber')}

        return step

    # Format training data for API submission
    def format_training_data(self, workouts, plan_id=None, day_a=date.today(), day_b=date.today() + timedelta(days=1)):
        sport_settings = self.get_sport_settings(sport='Run')
        if sport_settings and 'id' in sport_settings:
            self.update_threshold_pace(threshold_pace=0.85 * workouts['trainings'][0].vVO2.to_pace(),
                                       id=sport_settings['id'])
        formatted_data = []
        threshold_pace = sport_settings.get('threshold_pace') if sport_settings else None
        max_hr = sport_settings.get('max_hr') if sport_settings else None
        for workout in workouts["trainings"]:
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

    @staticmethod
    def duration_string(description_lines, step):
        if 'duration' in step and 'reps' not in step:
            h = str(floor(step['duration'] / 3600))
            step['duration'] = step['duration'] - (int(h) * 3600)
            m = str(floor(step['duration'] / 60))
            step['duration'] = step['duration'] - (int(m) * 60)
            s = str(step['duration'])
            description_lines.append(f"- {IntervalsWorkout.format_duration_string(h, m, s)} in {step['description']}")
        elif 'distance' in step and 'reps' not in step:
            k = str(round(step['distance'] / 1000, 2))
            description_lines.append(f"- {k}km in {step['description']}")
        elif 'reps' in step:
            description_lines.append(f"{step['reps']}x")
            for substep in step.get('steps', []):
                if 'duration' in substep:
                    h = str(floor(substep['duration'] / 3600))
                    substep['duration'] = substep['duration'] - (int(h) * 3600)
                    m = str(floor(substep['duration'] / 60))
                    substep['duration'] = substep['duration'] - (int(m) * 60)
                    s = str(substep['duration'])

                    description_lines.append(
                        f"  - {IntervalsWorkout.format_duration_string(h, m, s)} in {substep['description']}")
                elif 'distance' in substep:
                    k = str(round(substep['distance'] / 1000, 2))
                    description_lines.append(f"  - {k}km in {substep['description']}")

    @staticmethod
    def format_duration_string(h, m, s):
        time_parts = []
        if int(h) > 0:
            time_parts.append(f"{h}h")
        if int(m) > 0:
            time_parts.append(f"{m}m")
        if int(s) > 0:
            time_parts.append(f"{s}s")
        time_str = "".join(time_parts)
        return time_str

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
            logging.info("Threshold pace updated successfully.")
        else:
            logging.error(f"Failed to update threshold pace. Status code: {response.status_code}")
            logging.error(response.text)

    def update_max_hr(self, max_hr: int) -> None:
        """
        Update the maximum heart rate in Intervals.icu.
        """
        url = f"{IntervalsWorkout.BASE_URL}/{self.athlete_id}/sport-settings"
        payload = {"max_hr": max_hr}
        response = self.put(url, json=payload)
        if response.status_code == 200:
            logging.info("Maximum heart rate updated successfully.")
        else:
            logging.error(f"Failed to update maximum heart rate. Status code: {response.status_code}")
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
