from datetime import timedelta
import yaml
from typing import Any

import account


class Extraction(object):
    @staticmethod
    def description_formatting(description: str | None) -> str:
        if description is None:
            return ''

        if not any(substring in description for substring in ['Dr.', '. Complete', '\u2022']):
            description = description.replace('. ', '.\n')

        replacements = {
            'rest20s': 'rest\n 20s',
            '.Try': '.\nTry',
            ':20s': ':\n-20s',
            '.8 sets': '.\n-8 sets',
            ')8 sets': ')\n-8 sets',
            '.Workout': '.\nWorkout',
            'push-ups.Benchmark': 'push-ups.\nBenchmark',
            'Importado con EstraperTools:\nestraperlista.com/estrapertools\n\n': ''
        }

        for old, new in replacements.items():
            description = description.replace(old, new)

        return description

    @staticmethod
    def workout_export_yaml(workout, filename) -> None:
        filename = filename.replace('.json', '.yaml')
        workout_dict: dict = {
            'name': workout.get('name', ''),
            'sport': Extraction.format_sport(workout.get('type', '')),
            **({'subsport': workout.get('sub_type', '') if 'sub_type' in workout else ''}
               if workout.get('sub_type', '') else {}),
            'description': Extraction.description_formatting(workout.get('workout_doc', {}).get('description', '')),
            'load': workout.get('icu_training_load', ''),
            'steps': [],
        }

        if 'workout_doc' in workout and workout['workout_doc']:
            workout_segment: Any = workout['workout_doc']
            workout_steps: Any = workout_segment.get('steps', [])

            for step_json in workout_steps:
                step_type = next(iter(step_json.keys()))

                if step_type != 'reps':
                    workout_dict['steps'].append(Extraction.format_step(step_json, workout.get('type', '')))
                else:
                    rep_step = [Extraction.format_step(rep_step_json, workout.get('type', ''))
                                for rep_step_json in step_json.get('steps', [])]
                    for _ in range(step_json['reps']):
                        workout_dict['steps'].append(rep_step)

            with open(filename, 'w') as f:
                yaml.dump(workout_dict, f, default_flow_style=None)

    @staticmethod
    def format_sport(sport: str) -> str:
        if sport == 'Run':
            return 'running'
        elif sport == 'Ride':
            return 'cycling'
        elif sport == 'Swim':
            return 'swimming'
        elif sport == 'Walk':
            return 'walking'
        elif sport == 'Strength Training':
            return 'strength_training'
        else:
            return ''

    @staticmethod
    def format_step(step_json, sport):
        if 'power' in step_json:
            return Extraction._format_power_step(step_json)
        elif 'hr' in step_json:
            return Extraction._format_hr_step(step_json, sport)
        elif 'reps' in step_json:
            return Extraction._format_reps_step(step_json, sport)
        elif 'maxeffort' in step_json:
            return Extraction._format_maxeffort_step(step_json)
        else:
            return Extraction._format_default_step(step_json)

    @staticmethod
    def _format_power_step(step_json):
        step = {
            'type': 'interval',
            'duration': str(timedelta(seconds=int(step_json.get('duration')))),
            'target': {'type': 'power.zone'}
        }
        power = step_json['power']
        if 'value' in power:
            if power['value'] == 0:
                step['target']['min'] = 0
                step['target']['max'] = 0.05
            else:
                step['target']['min'] = (power['value'] - 5) / 100
                step['target']['max'] = (power['value'] + 5) / 100
            step['description'] = str(power['value']) + '%FTP'
        elif 'start' in power and 'end' in power:
            val_min = power['start'] / 100
            val_max = power['end'] / 100

            if val_max < val_min:
                val_min, val_max = val_max, val_min

            step['target']['min'] = val_min
            step['target']['max'] = val_max
            step['description'] = str(power['start']) + '%FTP'
        else:
            step['target']['min'] = 0
            step['target']['max'] = 1
            step['description'] = 'Unknown Power Zone'
        return step

    @staticmethod
    def _format_hr_step(step_json, sport):
        step = {
            'type': 'interval',
            'duration': str(timedelta(seconds=int(step_json.get('duration')))),
            'target': {'type': 'heart.rate.zone'}
        }
        fmin = account.fmin
        if sport == 'Run':
            fmax = account.rfmax
        elif sport == 'Ride':
            fmax = account.cfmax
        else:
            fmax = account.rfmax

        hr = step_json['hr']
        if 'value' in hr:
            step['target']['min'] = (hr['value'] - 5) / 100
            step['target']['max'] = (hr['value'] + 5) / 100
            step['target']['min'] = round((step['target']['min'] * fmax - fmin) / (fmax - fmin), 2)
            step['target']['max'] = round((step['target']['max'] * fmax - fmin) / (fmax - fmin), 2)
            step['description'] = str(hr['value']) + '%HR'
        elif 'start' in hr and 'end' in hr:
            val_min = hr['start'] / 100
            val_max = hr['end'] / 100

            if val_max < val_min:
                val_min, val_max = val_max, val_min

            step['target']['min'] = val_min
            step['target']['max'] = val_max
            step['description'] = str(hr['start']) + ' - ' + str(hr['end']) + '%HR'
        else:
            step['target']['min'] = 0
            step['target']['max'] = 1
            step['description'] = 'Unknown Power Zone'
        return step

    @staticmethod
    def _format_reps_step(step_json, sport):
        steps = []
        for _ in range(step_json['reps']):
            for rep_step_json in step_json['steps']:
                sub_step = Extraction.format_step(rep_step_json, sport)
                steps.append(sub_step)
        return steps

    @staticmethod
    def _format_maxeffort_step(step_json):
        return {
            'type': 'interval',
            'duration': str(timedelta(seconds=int(step_json.get('duration')))),
            'target': {
                'type': 'power.zone',
                'min': 1.5,
                'max': 2.5
            },
            'description': 'Maximum effort'
        }

    @staticmethod
    def _format_default_step(step_json):
        return {
            'type': 'interval',
            'duration': str(timedelta(seconds=int(step_json.get('duration')))),
            'target': None
        }
