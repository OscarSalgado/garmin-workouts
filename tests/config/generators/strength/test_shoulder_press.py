import pytest

from garminworkouts.config.generators.strength.shoulder_press import (
    alternating_dumbbell_shoulder_press_rep_generator,
    alternating_dumbbell_shoulder_press_hold_generator,
    arnold_press_rep_generator,
    arnold_press_hold_generator,
    barbell_front_squat_to_push_press_rep_generator,
    barbell_front_squat_to_push_press_hold_generator,
    barbell_push_press_rep_generator,
    barbell_push_press_hold_generator,
    barbell_shoulder_press_rep_generator,
    barbell_shoulder_press_hold_generator,
    dead_curl_press_rep_generator,
    dead_curl_press_hold_generator,
    dumbbell_alternating_shoulder_press_and_twist_rep_generator,
    dumbbell_alternating_shoulder_press_and_twist_hold_generator,
    dumbbell_front_raise_rep_generator,
    dumbbell_front_raise_hold_generator,
    dumbbell_hammer_curl_to_lunge_to_press_rep_generator,
    dumbbell_hammer_curl_to_lunge_to_press_hold_generator,
    dumbbell_push_press_rep_generator,
    dumbbell_push_press_hold_generator,
    dumbbell_shoulder_press_rep_generator,
    dumbbell_shoulder_press_hold_generator,
    floor_inverted_shoulder_press_rep_generator,
    floor_inverted_shoulder_press_hold_generator,
    inverted_shoulder_press_rep_generator,
    inverted_shoulder_press_hold_generator,
    military_press_rep_generator,
    military_press_hold_generator,
    one_arm_push_press_rep_generator,
    one_arm_push_press_hold_generator,
    overhead_barbell_press_rep_generator,
    overhead_barbell_press_hold_generator,
    overhead_dumbbell_press_rep_generator,
    overhead_dumbbell_press_hold_generator,
    seated_barbell_shoulder_press_rep_generator,
    seated_barbell_shoulder_press_hold_generator,
    seated_dumbbell_shoulder_press_rep_generator,
    seated_dumbbell_shoulder_press_hold_generator,
    single_arm_dumbbell_shoulder_press_rep_generator,
    single_arm_dumbbell_shoulder_press_hold_generator,
    single_arm_step_up_and_press_rep_generator,
    single_arm_step_up_and_press_hold_generator,
    smith_machine_overhead_press_rep_generator,
    smith_machine_overhead_press_hold_generator,
    split_stance_hammer_curl_to_press_rep_generator,
    split_stance_hammer_curl_to_press_hold_generator,
    strict_press_rep_generator,
    strict_press_hold_generator,
    swiss_ball_dumbbell_shoulder_press_rep_generator,
    swiss_ball_dumbbell_shoulder_press_hold_generator,
    weight_plate_front_raise_rep_generator,
    weight_plate_front_raise_hold_generator,
    weighted_floor_inverted_shoulder_press_rep_generator,
    weighted_floor_inverted_shoulder_press_hold_generator,
    weighted_inverted_shoulder_press_rep_generator,
    weighted_inverted_shoulder_press_hold_generator,
    )


@pytest.mark.parametrize("generator, exercise_name, execution", [
    (alternating_dumbbell_shoulder_press_rep_generator,
     'ALTERNATING_DUMBBELL_SHOULDER_PRESS',
     'reps'),
    (alternating_dumbbell_shoulder_press_hold_generator,
     'ALTERNATING_DUMBBELL_SHOULDER_PRESS',
     'hold'),
    (arnold_press_rep_generator,
     'ARNOLD_PRESS',
     'reps'),
    (arnold_press_hold_generator,
     'ARNOLD_PRESS',
     'hold'),
    (barbell_front_squat_to_push_press_rep_generator,
     'BARBELL_FRONT_SQUAT_TO_PUSH_PRESS',
     'reps'),
    (barbell_front_squat_to_push_press_hold_generator,
     'BARBELL_FRONT_SQUAT_TO_PUSH_PRESS',
     'hold'),
    (barbell_push_press_rep_generator,
     'BARBELL_PUSH_PRESS',
     'reps'),
    (barbell_push_press_hold_generator,
     'BARBELL_PUSH_PRESS',
     'hold'),
    (barbell_shoulder_press_rep_generator,
     'BARBELL_SHOULDER_PRESS',
     'reps'),
    (barbell_shoulder_press_hold_generator,
     'BARBELL_SHOULDER_PRESS',
     'hold'),
    (dead_curl_press_rep_generator,
     'DEAD_CURL_PRESS',
     'reps'),
    (dead_curl_press_hold_generator,
     'DEAD_CURL_PRESS',
     'hold'),
    (dumbbell_alternating_shoulder_press_and_twist_rep_generator,
     'DUMBBELL_ALTERNATING_SHOULDER_PRESS_AND_TWIST',
     'reps'),
    (dumbbell_alternating_shoulder_press_and_twist_hold_generator,
     'DUMBBELL_ALTERNATING_SHOULDER_PRESS_AND_TWIST',
     'hold'),
    (dumbbell_front_raise_rep_generator,
     'DUMBBELL_FRONT_RAISE',
     'reps'),
    (dumbbell_front_raise_hold_generator,
     'DUMBBELL_FRONT_RAISE',
     'hold'),
    (dumbbell_hammer_curl_to_lunge_to_press_rep_generator,
     'DUMBBELL_HAMMER_CURL_TO_LUNGE_TO_PRESS',
     'reps'),
    (dumbbell_hammer_curl_to_lunge_to_press_hold_generator,
     'DUMBBELL_HAMMER_CURL_TO_LUNGE_TO_PRESS',
     'hold'),
    (dumbbell_push_press_rep_generator,
     'DUMBBELL_PUSH_PRESS',
     'reps'),
    (dumbbell_push_press_hold_generator,
     'DUMBBELL_PUSH_PRESS',
     'hold'),
    (dumbbell_shoulder_press_rep_generator,
     'DUMBBELL_SHOULDER_PRESS',
     'reps'),
    (dumbbell_shoulder_press_hold_generator,
     'DUMBBELL_SHOULDER_PRESS',
     'hold'),
    (floor_inverted_shoulder_press_rep_generator,
     'FLOOR_INVERTED_SHOULDER_PRESS',
     'reps'),
    (floor_inverted_shoulder_press_hold_generator,
     'FLOOR_INVERTED_SHOULDER_PRESS',
     'hold'),
    (inverted_shoulder_press_rep_generator,
     'INVERTED_SHOULDER_PRESS',
     'reps'),
    (inverted_shoulder_press_hold_generator,
     'INVERTED_SHOULDER_PRESS',
     'hold'),
    (military_press_rep_generator,
     'MILITARY_PRESS',
     'reps'),
    (military_press_hold_generator,
     'MILITARY_PRESS',
     'hold'),
    (one_arm_push_press_rep_generator,
     'ONE_ARM_PUSH_PRESS',
     'reps'),
    (one_arm_push_press_hold_generator,
     'ONE_ARM_PUSH_PRESS',
     'hold'),
    (overhead_barbell_press_rep_generator,
     'OVERHEAD_BARBELL_PRESS',
     'reps'),
    (overhead_barbell_press_hold_generator,
     'OVERHEAD_BARBELL_PRESS',
     'hold'),
    (overhead_dumbbell_press_rep_generator,
     'OVERHEAD_DUMBBELL_PRESS',
     'reps'),
    (overhead_dumbbell_press_hold_generator,
     'OVERHEAD_DUMBBELL_PRESS',
     'hold'),
    (seated_barbell_shoulder_press_rep_generator,
     'SEATED_BARBELL_SHOULDER_PRESS',
     'reps'),
    (seated_barbell_shoulder_press_hold_generator,
     'SEATED_BARBELL_SHOULDER_PRESS',
     'hold'),
    (seated_dumbbell_shoulder_press_rep_generator,
     'SEATED_DUMBBELL_SHOULDER_PRESS',
     'reps'),
    (seated_dumbbell_shoulder_press_hold_generator,
     'SEATED_DUMBBELL_SHOULDER_PRESS',
     'hold'),
    (single_arm_dumbbell_shoulder_press_rep_generator,
     'SINGLE_ARM_DUMBBELL_SHOULDER_PRESS',
     'reps'),
    (single_arm_dumbbell_shoulder_press_hold_generator,
     'SINGLE_ARM_DUMBBELL_SHOULDER_PRESS',
     'hold'),
    (single_arm_step_up_and_press_rep_generator,
     'SINGLE_ARM_STEP_UP_AND_PRESS',
     'reps'),
    (single_arm_step_up_and_press_hold_generator,
     'SINGLE_ARM_STEP_UP_AND_PRESS',
     'hold'),
    (smith_machine_overhead_press_rep_generator,
     'SMITH_MACHINE_OVERHEAD_PRESS',
     'reps'),
    (smith_machine_overhead_press_hold_generator,
     'SMITH_MACHINE_OVERHEAD_PRESS',
     'hold'),
    (split_stance_hammer_curl_to_press_rep_generator,
     'SPLIT_STANCE_HAMMER_CURL_TO_PRESS',
     'reps'),
    (split_stance_hammer_curl_to_press_hold_generator,
     'SPLIT_STANCE_HAMMER_CURL_TO_PRESS',
     'hold'),
    (strict_press_rep_generator,
     'STRICT_PRESS',
     'reps'),
    (strict_press_hold_generator,
     'STRICT_PRESS',
     'hold'),
    (swiss_ball_dumbbell_shoulder_press_rep_generator,
     'SWISS_BALL_DUMBBELL_SHOULDER_PRESS',
     'reps'),
    (swiss_ball_dumbbell_shoulder_press_hold_generator,
     'SWISS_BALL_DUMBBELL_SHOULDER_PRESS',
     'hold'),
    (weight_plate_front_raise_rep_generator,
     'WEIGHT_PLATE_FRONT_RAISE',
     'reps'),
    (weight_plate_front_raise_hold_generator,
     'WEIGHT_PLATE_FRONT_RAISE',
     'hold'),
    (weighted_floor_inverted_shoulder_press_rep_generator,
     'WEIGHTED_FLOOR_INVERTED_SHOULDER_PRESS',
     'reps'),
    (weighted_floor_inverted_shoulder_press_hold_generator,
     'WEIGHTED_FLOOR_INVERTED_SHOULDER_PRESS',
     'hold'),
    (weighted_inverted_shoulder_press_rep_generator,
     'WEIGHTED_INVERTED_SHOULDER_PRESS',
     'reps'),
    (weighted_inverted_shoulder_press_hold_generator,
     'WEIGHTED_INVERTED_SHOULDER_PRESS',
     'hold'),
    ])
def test_exercise_generators(generator, exercise_name, execution):
    duration = "10reps" if execution == 'reps' else 'lap.button'
    description = exercise_name.replace('_', ' ').title() if execution == 'reps' else "10-count hold"
    result = generator(10)
    assert result['category'] == 'SHOULDER_PRESS'
    assert result['exerciseName'] == exercise_name
    assert result['duration'] == duration
    assert result['target'] == 'NO_TARGET'
    assert result['description'] == description
