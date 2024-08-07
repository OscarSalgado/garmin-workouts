import unittest
from garminworkouts.models.workoutstep import WorkoutStep
from garminworkouts.models.target import Target
from garminworkouts.models.fields import (_UNIT_KEY,
                                          get_end_condition)


class TestWorkoutStep(unittest.TestCase):
    def test_end_condition_unit(self) -> None:
        assert WorkoutStep.end_condition_unit('1km') == {_UNIT_KEY: 'kilometer'}
        assert WorkoutStep.end_condition_unit('1cals') == {_UNIT_KEY: 'calories'}
        assert WorkoutStep.end_condition_unit('1') == {_UNIT_KEY: None}
        assert WorkoutStep.end_condition_unit(None) is None

        assert WorkoutStep.parsed_end_condition_value('0:40') == 40
        assert WorkoutStep.parsed_end_condition_value('4:20') == 260
        assert WorkoutStep.parsed_end_condition_value('2.0km') == 2000
        assert WorkoutStep.parsed_end_condition_value('1.125km') == 1125
        assert WorkoutStep.parsed_end_condition_value('1.6km') == 1600
        assert WorkoutStep.parsed_end_condition_value('1cals') == 1
        assert WorkoutStep.parsed_end_condition_value('0ppm') == 0
        assert WorkoutStep.parsed_end_condition_value('0tp') == 0
        assert WorkoutStep.parsed_end_condition_value('10reps') == 10
        assert WorkoutStep.parsed_end_condition_value(None) == 0

        assert WorkoutStep._str_to_meters('2.0km') == 2000
        assert WorkoutStep._str_to_meters('1.125km') == 1125
        assert WorkoutStep._str_to_meters('1.6km') == 1600
        assert WorkoutStep._str_to_meters('500m') == 500
        assert WorkoutStep._str_to_meters('100m') == 100
        assert WorkoutStep._str_to_meters('10m') == 10
        assert WorkoutStep._str_to_meters('1m') == 1
        assert WorkoutStep._str_to_meters('0m') == 0
        assert WorkoutStep._str_to_meters('2km') == 2000
        assert WorkoutStep._str_to_meters('1.5km') == 1500
        assert WorkoutStep._str_to_meters('0.5km') == 500

    def test_end_condition(self) -> None:
        step_config: dict = {
            'condition_type_key': 'lap.button'
        }
        assert WorkoutStep._end_condition(step_config) == get_end_condition('lap.button')

        step_config = {
            'duration': '2.0km',
            'condition_type_key': 'distance'
        }
        assert WorkoutStep._end_condition(step_config) == get_end_condition('distance')

        step_config = {
            'duration': '1cals',
            'condition_type_key': 'calories'
        }
        assert WorkoutStep._end_condition(step_config) == get_end_condition('calories')

        step_config = {
            'duration': '0ppm',
            'condition_type_key': 'heart.rate'
        }
        assert WorkoutStep._end_condition(step_config) == get_end_condition('heart.rate')

        step_config = {
            'duration': '10reps',
            'condition_type_key': 'reps'
        }
        assert WorkoutStep._end_condition(step_config) == get_end_condition('reps')

    def test_create_workout_step(self) -> None:
        step = WorkoutStep(
            order='1',
            child_step_id='child_step_1',
            description='Sample workout step',
            step_type='warmup',
            end_condition='distance',
            end_condition_value='2.0km',
            target=Target(target='no.target'),
            secondary_target=Target(target='no.target'),
            category='running',
            exerciseName='running',
            weight='10',
            equipment='treadmill',
            stroke=None
        )
        expected_result: dict = {
            'type': 'ExecutableStepDTO',
            'stepId': None,
            'stepOrder': '1',
            'childStepId': 'child_step_1',
            'description': 'Sample workout step',
            'stepType': {
                'stepTypeId': 1,
                'stepTypeKey': 'warmup'
            },
            'endCondition': {
                'conditionTypeId': 3,
                'conditionTypeKey': 'distance'
            },
            'preferredEndConditionUnit': {'unitKey': None},
            'endConditionValue': 2000,
            'endConditionCompare': None,
            'endConditionZone': None,
            'category': 'running',
            'exerciseName': 'running',
            'weightValue': '10',
            'weightUnit': {'unitId': 8, 'unitKey': 'kilogram', 'factor': 1000}
        }
        assert step.create_workout_step() == expected_result
