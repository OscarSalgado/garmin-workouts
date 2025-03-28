
from garminworkouts.models.duration import Duration
from garminworkouts.models.target import Target
from garminworkouts.models.fields import (_STEP_TYPE, _END_CONDITION, _TYPE, _CATEGORY, _STEP_ID, _STEP_ORDER,
                                          _CHILD_STEP_ID, _DESCRIPTION, _END_CONDITION_VALUE, _END_CONDITION_COMPARE,
                                          _END_CONDITION_ZONE, _EXERCISE_NAME, _EXECUTABLE_STEP,
                                          _PREFERRED_END_CONDITION_UNIT, _CONDITION_TYPE_KEY, _UNIT_KEY, _DURATION,
                                          get_end_condition, get_step_type, get_stroke_type, get_equipment_type,
                                          get_weight)


class WorkoutStep:
    def __init__(
        self,
        order,
        child_step_id,
        description,
        step_type,
        end_condition='lap.button',
        end_condition_value=None,
        target=None,
        secondary_target=None,
        category=None,
        exerciseName=None,
        weight=None,
        equipment=None,
        stroke=None,
    ) -> None:
        '''Valid end condition values:
        - distance: '2.0km', '1.125km', '1.6km'
        - time: 0:40, 4:20
        - lap.button
        '''
        self.order: str = order
        self.child_step_id: str = child_step_id
        self.description: str = description
        self.step_type: str = step_type
        self.end_condition: str = end_condition
        self.end_condition_value: str | None = end_condition_value
        self.target: Target = target or Target()
        self.secondary_target: Target = secondary_target or Target()
        self.category: tuple = category,
        self.exerciseName = exerciseName,
        self.weight = weight,
        self.equipment: str | None = equipment
        self.stroke: str | None = stroke

    @staticmethod
    def end_condition_unit(end_condition) -> dict | None:
        if end_condition:
            unit_mapping = {
                'km': 'kilometer',
                'cals': 'calories'
            }
            for key, value in unit_mapping.items():
                if end_condition.endswith(key):
                    return {_UNIT_KEY: value}
            return {_UNIT_KEY: None}
        else:
            return None

    @staticmethod
    def _end_condition(step_config) -> dict:
        duration = step_config.get(_DURATION)
        if duration:
            return get_end_condition(
                'time' if WorkoutStep._str_is_time(duration) else
                'calories' if WorkoutStep._str_is_calories(duration) else
                'heart.rate' if WorkoutStep._str_is_ppm(duration) else
                'reps' if WorkoutStep._str_is_reps(duration) else
                'distance' if WorkoutStep._str_is_distance(duration) else
                'lap.button')
        return get_end_condition('lap.button')

    @staticmethod
    def _end_condition_key(step_config) -> str:
        return step_config[_CONDITION_TYPE_KEY]

    @staticmethod
    def _end_condition_value(step_config) -> int:
        return WorkoutStep.parsed_end_condition_value(step_config.get(_DURATION))

    @staticmethod
    def _str_is_time(string) -> bool:
        return True if ':' in string else False

    @staticmethod
    def _str_to_seconds(time_string) -> int:
        return Duration(str(time_string)).to_seconds()

    @staticmethod
    def _str_is_distance(string) -> bool:
        return True if 'm' in string.lower() else False

    @staticmethod
    def _str_to_meters(string) -> int:
        return int(float(string.lower().split('km')[0])*1000) if 'km' in string.lower() else int(
            string.lower().split('m')[0])

    @staticmethod
    def _str_is_calories(string) -> bool:
        return True if 'cals' in string else False

    @staticmethod
    def _str_to_calories(string) -> int:
        return int(string.lower().split('cals')[0])

    @staticmethod
    def _str_is_ppm(string) -> bool:
        return True if 'ppm' in string else False

    @staticmethod
    def _str_to_ppm(string) -> int:
        return int(string.lower().split('ppm')[0])

    @staticmethod
    def _str_is_reps(string) -> bool:
        return True if 'reps' in string else False

    @staticmethod
    def _str_to_reps(string) -> int:
        return int(string.lower().split('reps')[0])

    @staticmethod
    def parsed_end_condition_value(duration) -> int:
        if duration:
            return (
                WorkoutStep._str_to_seconds(duration) if WorkoutStep._str_is_time(duration) else
                WorkoutStep._str_to_calories(duration) if WorkoutStep._str_is_calories(duration) else
                WorkoutStep._str_to_ppm(duration) if WorkoutStep._str_is_ppm(duration) else
                WorkoutStep._str_to_reps(duration) if WorkoutStep._str_is_reps(duration) else
                WorkoutStep._str_to_meters(duration) if WorkoutStep._str_is_distance(duration) else
                int(0)
            )
        else:
            return int(0)

    def create_workout_step(self) -> dict:
        return {
            _TYPE: _EXECUTABLE_STEP,
            _STEP_ID: None,
            _STEP_ORDER: self.order,
            _CHILD_STEP_ID: self.child_step_id,
            _DESCRIPTION: self.description,
            _STEP_TYPE: get_step_type(self.step_type),
            _END_CONDITION: get_end_condition(self.end_condition),
            _PREFERRED_END_CONDITION_UNIT: WorkoutStep.end_condition_unit(self.end_condition),
            _END_CONDITION_VALUE: WorkoutStep.parsed_end_condition_value(self.end_condition_value),
            _END_CONDITION_COMPARE: None,
            _END_CONDITION_ZONE: None,
            _CATEGORY: self.category[0],
            _EXERCISE_NAME: self.exerciseName[0],
            **self.target.create_target(),
            **self.secondary_target.create_target(),
            **get_stroke_type(self.stroke),
            **get_equipment_type(self.equipment),
            **get_weight(self.weight[0], 'kilogram')
        }
