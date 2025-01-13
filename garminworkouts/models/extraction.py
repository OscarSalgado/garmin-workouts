from datetime import timedelta
import yaml
from typing import Any


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
            'push-ups.Benchmark': 'push-ups.\nBenchmark'
        }

        for old, new in replacements.items():
            description = description.replace(old, new)

        return description

    @staticmethod
    def end_condition_extraction(step_json, step) -> dict:
        end_condition: str = step_json['endCondition']['conditionTypeKey']
        end_condition_value: str = step_json.get('endConditionValue', '0') if step_json.get('endConditionValue', '0') \
            is not None else '0'

        duration_mapping = {
            'time': str(timedelta(seconds=int(end_condition_value))),
            'fixed.rest': str(timedelta(seconds=int(end_condition_value))),
            'distance': f"{round(float(end_condition_value) / 1000, 3)}km",
            'reps': f"{int(end_condition_value)}reps",
            'heart.rate': f"{int(end_condition_value)}ppm{step_json.get('endConditionCompare', '')}",
            'calories': f"{int(end_condition_value)}cal",
            'lap.button': 'lap.button'
        }

        if end_condition in duration_mapping:
            step['duration'] = duration_mapping[end_condition]
        else:
            raise ValueError(f"Unsupported end condition: {end_condition}")

        return step

    @staticmethod
    def target_extraction(step_json, step) -> dict:
        step['target'] = {'type': 'no.target'}
        if 'targetType' in step_json and step_json['targetType']:
            target_type_key = step_json['targetType']['workoutTargetTypeKey']
            target_values = {
                'min': step_json.get('targetValueOne'),
                'max': step_json.get('targetValueTwo'),
                'zone': step_json.get('zoneNumber')
            }

            if target_type_key == 'pace.zone':
                step['target'] = {
                    'type': target_type_key,
                    **({'min': str(timedelta(seconds=1000 / float(target_values['min'])))
                        } if target_values['zone'] is None else {}),
                    **({'max': str(timedelta(seconds=1000 / float(target_values['max'])))
                        } if target_values['zone'] is None else {})
                }
            elif target_type_key == 'cadence':
                step['target'] = {
                    'type': target_type_key,
                    'min': str(int(target_values['min'])),
                    'max': str(int(target_values['max']))
                }
            elif target_type_key in ['heart.rate.zone', 'power.zone']:
                step['target'] = {
                    'type': target_type_key,
                    **({'min': str(int(target_values['min']))} if target_values['zone'] is None else {}),
                    **({'max': str(int(target_values['max']))} if target_values['zone'] is None else {}),
                    **({'zone': str(target_values['zone'])} if target_values['zone'] is not None else {})
                }
            elif target_type_key == 'no.target':
                step['target']['type'] = 'no.target'
            else:
                raise ValueError(f"Unsupported target: {target_type_key}")

        return step

    @staticmethod
    def secondary_target_extraction(step_json, step) -> dict:
        if 'secondaryTargetType' in step_json and step_json['secondaryTargetType']:
            secondary_target_key = step_json['secondaryTargetType']['workoutTargetTypeKey']
            secondary_target_values = {
                'min': step_json.get('secondaryTargetValueOne'),
                'max': step_json.get('secondaryTargetValueTwo'),
                'zone': step_json.get('secondaryZoneNumber')
            }

            if secondary_target_key == 'pace.zone':
                step['secondaryTarget'] = {
                    'type': secondary_target_key,
                    **({'min': str(timedelta(seconds=1000 / float(secondary_target_values['min'])))
                        } if secondary_target_values['zone'] is None else {}),
                    **({'max': str(timedelta(seconds=1000 / float(secondary_target_values['max'])))
                        } if secondary_target_values['zone'] is None else {})
                }
            elif secondary_target_key == 'cadence':
                step['secondaryTarget'] = {
                    'type': secondary_target_key,
                    'min': str(int(secondary_target_values['min'])),
                    'max': str(int(secondary_target_values['max']))
                }
            elif secondary_target_key in ['heart.rate.zone', 'power.zone']:
                step['secondaryTarget'] = {
                    'type': secondary_target_key,
                    **({'min': str(int(secondary_target_values['min']))
                        } if secondary_target_values['zone'] is None else {}),
                    **({'max': str(int(secondary_target_values['max']))
                        } if secondary_target_values['zone'] is None else {}),
                    **({'zone': str(secondary_target_values['zone'])
                        } if secondary_target_values['zone'] is not None else {})
                }
            elif secondary_target_key == 'no.target':
                step.pop('secondaryTarget', None)
            else:
                raise ValueError(f"Unsupported secondary target: {secondary_target_key}")
        return step

    @staticmethod
    def weight_extraction(step_json, step) -> dict:
        weight_value = step_json.get('weightValue')
        weight_unit = step_json.get('weightUnit', {}).get('unitKey')

        if weight_value:
            if weight_unit == 'kilogram':
                step['weight'] = f"{weight_value}kg"
            elif weight_unit == 'pound':
                step['weight'] = f"{weight_value}pound"
            else:
                raise ValueError(f"Unsupported weight unit: {weight_unit}")
        return step

    @staticmethod
    def step_extraction(step_json) -> dict | None:
        if step_json['stepType']['stepTypeKey'] != 'repeat':
            step = {
                'type': step_json['stepType']['stepTypeKey'],
                **{k: v for k, v in {
                    'description': step_json.get('description', ''),
                    'equipment': step_json.get('equipmentType', {}).get('equipmentTypeKey'),
                    'category': step_json.get('category'),
                    'exerciseName': step_json.get('exerciseName'),
                    # 'workoutProvider': step_json.get('workoutProvider'),
                    # 'providerExerciseSourceId': step_json.get('providerExerciseSourceId'),
                    'repeatDuration': step_json.get('repeatDuration')
                }.items() if v}
            }
            step = Extraction.end_condition_extraction(step_json, step)
            step = Extraction.target_extraction(step_json, step)
            step = Extraction.secondary_target_extraction(step_json, step)
            step = Extraction.weight_extraction(step_json, step)
            return step

    @staticmethod
    def workout_export_yaml(workout, filename) -> None:
        workout_dict: dict = {
            'name': workout.get('workoutName', ''),
            'sport': workout['sportType'].get('sportTypeKey', ''),
            **({'subsport': workout.get('subSportType', '') if 'subSportType' in workout else ''}
               if workout.get('subSportType', '') else {}),
            'description': Extraction.description_formatting(workout.get('description', '')),
            'steps': [],
        }

        if 'workoutSegments' in workout and workout['workoutSegments']:
            workout_segment: Any = workout['workoutSegments'][0]
            workout_steps: Any = workout_segment.get('workoutSteps', [])

            for step_json in workout_steps:
                step_type: Any = step_json['stepType'].get('stepTypeKey', '')

                if step_type != 'repeat':
                    workout_dict['steps'].append(Extraction.step_extraction(step_json))
                else:
                    if 'numberOfIterations' in step_json and step_json['numberOfIterations'] is not None:
                        rep_step = [Extraction.step_extraction(rep_step_json)
                                    for rep_step_json in step_json.get('workoutSteps', [])]
                        for _ in range(step_json['numberOfIterations']):
                            workout_dict['steps'].append(rep_step)
                    else:
                        for rep_step_json in step_json.get('workoutSteps', []):
                            rep_step_json['repeatDuration'] = str(timedelta(seconds=int(
                                step_json.get('endConditionValue', 0))))
                            workout_dict['steps'].append(Extraction.step_extraction(rep_step_json))
        with open(filename, 'w') as file:
            yaml.dump(workout_dict, file, default_flow_style=None)

    @staticmethod
    def event_export_yaml(event, filename) -> None:
        with open(filename, 'w') as file:
            yaml.dump(event, file, default_flow_style=None)

    @staticmethod
    def note_export_yaml(note, filename) -> None:
        with open(filename, 'w') as file:
            yaml.dump(note, file, default_flow_style=False)
