from datetime import date, timedelta
from typing import Any
import account
from garminworkouts.config import configreader
from intervalsicu.intervals.target import IntervalsTarget
from garminworkouts.models.types import STEP_TYPES


class IntervalsWorkout(IntervalsTarget):
    """
    IntervalsWorkout for managing workouts with Intervals.icu.
    Inherits from IntervalsAPI to utilize its methods.
    """
    # Expand repeated intervals into separate blocks
    def expand_repeats(self, fmax, threshold_pace, steps):
        expanded_steps = []
        valid_keys = list(STEP_TYPES.keys())
        valid_keys.remove('repeat')

        for step in steps:
            step_type = step.get('stepType', {}).get('stepTypeKey', '')
            if step_type in valid_keys:
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
    def format_training_data(self, workouts, plan_folder={},
                             day_a=date.today(), day_b=date.today() + timedelta(days=1)):
        start_date_str = plan_folder.get('start_date_local', None)
        start_date = date.fromisoformat(start_date_str.split('T')[0]) if start_date_str else date.today()

        sp = {}
        for sport in self.SUPPORTED_WORKOUT_TYPES:
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
                    description_lines.append('\n')
                    for d in description_lines:
                        if "x" in d and description_lines.index(d) != 0:
                            description_lines[description_lines.index(d)] = "\n" + d
                diff_days = (day_d - start_date).days
                formatted_data.append({
                    "athlete_id": self.athlete_id,
                    "folder_id": plan_folder.get('id', None) if plan_folder else None,
                    "name": workout.get_workout_name(),
                    "category": "WORKOUT",
                    "type": IntervalsWorkout.format_sport(workout),
                    "sub_type": workout.config.get("sub_type", None),
                    "color": None,
                    "description": "\n".join(description_lines).strip(),
                    "start_date_local": day_d.isoformat() + "T00:00:00",
                    "day": diff_days,
                    "moving_time": workout.sec,
                    "steps": expanded_steps,
                    "attachments": [],
                })
        return formatted_data

    def update_athlete_data(self):
        target: dict[Any, Any] = configreader.read_config(r'target.yaml')
        resting_hr = account.fmin

        self.update_resting_hr(resting_hr=resting_hr)

        for s in self.SUPPORTED_WORKOUT_TYPES:
            sport_settings = self.get_sport_settings(sport=s)
            if sport_settings and 'id' in sport_settings:
                if s == 'Run':
                    max_hr = account.rfmax
                    lthr = account.rflt
                    tp = float(target['R2']['min'])
                    VAM = account.vV02.to_pace()
                    self.update_threshold_pace(threshold_pace=tp * VAM, id=sport_settings['id'])
                    self.update_max_hr(max_hr=max_hr, id=sport_settings['id'])
                    self.update_lthr(lthr=lthr, id=sport_settings['id'])
                    self.update_hrrc_min_percent(
                        hrrc_min_percent=90, id=sport_settings['id'])

                elif s == 'Ride':
                    max_hr = account.cfmax
                    lthr = account.cflt
                    self.update_max_hr(max_hr=max_hr, id=sport_settings['id'])
                    self.update_lthr(lthr=lthr, id=sport_settings['id'])
                    self.update_hrrc_min_percent(
                        hrrc_min_percent=90, id=sport_settings['id'])
                elif s == 'Swim':
                    max_hr = account.sfmax
                    lthr = account.sflt
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
            description_lines.append(f"\n{step['reps']}x")
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

    def list_workout_folders(self):
        folders = self.list_folders()
        workout_folders = {folder.get('name', ''): folder for folder in folders if folder.get('type') == 'FOLDER'}
        return workout_folders

    def list_plans(self):
        folders = self.list_folders()
        plans = {folder.get('name', ''): folder for folder in folders if folder.get('type') == 'PLAN'}
        return plans
