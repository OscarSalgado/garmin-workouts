import pytest

from garminworkouts.config.generators.strength.suspension import (
    chest_fly_rep_generator,
    chest_fly_hold_generator,
    chest_press_rep_generator,
    chest_press_hold_generator,
    crunch_rep_generator,
    crunch_hold_generator,
    curl_rep_generator,
    curl_hold_generator,
    dip_rep_generator,
    dip_hold_generator,
    face_pull_rep_generator,
    face_pull_hold_generator,
    glute_bridge_rep_generator,
    glute_bridge_hold_generator,
    hamstring_curl_rep_generator,
    hamstring_curl_hold_generator,
    hip_drop_rep_generator,
    hip_drop_hold_generator,
    knee_drive_jump_rep_generator,
    knee_drive_jump_hold_generator,
    knee_to_chest_rep_generator,
    knee_to_chest_hold_generator,
    lat_pullover_rep_generator,
    lat_pullover_hold_generator,
    lunge_rep_generator,
    lunge_hold_generator,
    mountain_climber_rep_generator,
    mountain_climber_hold_generator,
    pendulum_rep_generator,
    pendulum_hold_generator,
    pike_rep_generator,
    pike_hold_generator,
    plank_rep_generator,
    plank_hold_generator,
    power_pull_rep_generator,
    power_pull_hold_generator,
    pull_up_rep_generator,
    pull_up_hold_generator,
    push_up_rep_generator,
    push_up_hold_generator,
    reverse_mountain_climber_rep_generator,
    reverse_mountain_climber_hold_generator,
    reverse_plank_rep_generator,
    reverse_plank_hold_generator,
    rollout_rep_generator,
    rollout_hold_generator,
    row_rep_generator,
    row_hold_generator,
    side_lunge_rep_generator,
    side_lunge_hold_generator,
    side_plank_rep_generator,
    side_plank_hold_generator,
    single_leg_deadlift_rep_generator,
    single_leg_deadlift_hold_generator,
    single_leg_squat_rep_generator,
    single_leg_squat_hold_generator,
    sit_up_rep_generator,
    sit_up_hold_generator,
    squat_rep_generator,
    squat_hold_generator,
    squat_jump_rep_generator,
    squat_jump_hold_generator,
    tricep_press_rep_generator,
    tricep_press_hold_generator,
    y_fly_rep_generator,
    y_fly_hold_generator,
    )


@pytest.mark.parametrize("generator, exercise_name, execution", [
    (chest_fly_rep_generator,
     'CHEST_FLY',
     'reps'),
    (chest_fly_hold_generator,
     'CHEST_FLY',
     'hold'),
    (chest_press_rep_generator,
     'CHEST_PRESS',
     'reps'),
    (chest_press_hold_generator,
     'CHEST_PRESS',
     'hold'),
    (crunch_rep_generator,
     'CRUNCH',
     'reps'),
    (crunch_hold_generator,
     'CRUNCH',
     'hold'),
    (curl_rep_generator,
     'CURL',
     'reps'),
    (curl_hold_generator,
     'CURL',
     'hold'),
    (dip_rep_generator,
     'DIP',
     'reps'),
    (dip_hold_generator,
     'DIP',
     'hold'),
    (face_pull_rep_generator,
     'FACE_PULL',
     'reps'),
    (face_pull_hold_generator,
     'FACE_PULL',
     'hold'),
    (glute_bridge_rep_generator,
     'GLUTE_BRIDGE',
     'reps'),
    (glute_bridge_hold_generator,
     'GLUTE_BRIDGE',
     'hold'),
    (hamstring_curl_rep_generator,
     'HAMSTRING_CURL',
     'reps'),
    (hamstring_curl_hold_generator,
     'HAMSTRING_CURL',
     'hold'),
    (hip_drop_rep_generator,
     'HIP_DROP',
     'reps'),
    (hip_drop_hold_generator,
     'HIP_DROP',
     'hold'),
    (knee_drive_jump_rep_generator,
     'KNEE_DRIVE_JUMP',
     'reps'),
    (knee_drive_jump_hold_generator,
     'KNEE_DRIVE_JUMP',
     'hold'),
    (knee_to_chest_rep_generator,
     'KNEE_TO_CHEST',
     'reps'),
    (knee_to_chest_hold_generator,
     'KNEE_TO_CHEST',
     'hold'),
    (lat_pullover_rep_generator,
     'LAT_PULLOVER',
     'reps'),
    (lat_pullover_hold_generator,
     'LAT_PULLOVER',
     'hold'),
    (lunge_rep_generator,
     'LUNGE',
     'reps'),
    (lunge_hold_generator,
     'LUNGE',
     'hold'),
    (mountain_climber_rep_generator,
     'MOUNTAIN_CLIMBER',
     'reps'),
    (mountain_climber_hold_generator,
     'MOUNTAIN_CLIMBER',
     'hold'),
    (pendulum_rep_generator,
     'PENDULUM',
     'reps'),
    (pendulum_hold_generator,
     'PENDULUM',
     'hold'),
    (pike_rep_generator,
     'PIKE',
     'reps'),
    (pike_hold_generator,
     'PIKE',
     'hold'),
    (plank_rep_generator,
     'PLANK',
     'reps'),
    (plank_hold_generator,
     'PLANK',
     'hold'),
    (power_pull_rep_generator,
     'POWER_PULL',
     'reps'),
    (power_pull_hold_generator,
     'POWER_PULL',
     'hold'),
    (pull_up_rep_generator,
     'PULL_UP',
     'reps'),
    (pull_up_hold_generator,
     'PULL_UP',
     'hold'),
    (push_up_rep_generator,
     'PUSH_UP',
     'reps'),
    (push_up_hold_generator,
     'PUSH_UP',
     'hold'),
    (reverse_mountain_climber_rep_generator,
     'REVERSE_MOUNTAIN_CLIMBER',
     'reps'),
    (reverse_mountain_climber_hold_generator,
     'REVERSE_MOUNTAIN_CLIMBER',
     'hold'),
    (reverse_plank_rep_generator,
     'REVERSE_PLANK',
     'reps'),
    (reverse_plank_hold_generator,
     'REVERSE_PLANK',
     'hold'),
    (rollout_rep_generator,
     'ROLLOUT',
     'reps'),
    (rollout_hold_generator,
     'ROLLOUT',
     'hold'),
    (row_rep_generator,
     'ROW',
     'reps'),
    (row_hold_generator,
     'ROW',
     'hold'),
    (side_lunge_rep_generator,
     'SIDE_LUNGE',
     'reps'),
    (side_lunge_hold_generator,
     'SIDE_LUNGE',
     'hold'),
    (side_plank_rep_generator,
     'SIDE_PLANK',
     'reps'),
    (side_plank_hold_generator,
     'SIDE_PLANK',
     'hold'),
    (single_leg_deadlift_rep_generator,
     'SINGLE_LEG_DEADLIFT',
     'reps'),
    (single_leg_deadlift_hold_generator,
     'SINGLE_LEG_DEADLIFT',
     'hold'),
    (single_leg_squat_rep_generator,
     'SINGLE_LEG_SQUAT',
     'reps'),
    (single_leg_squat_hold_generator,
     'SINGLE_LEG_SQUAT',
     'hold'),
    (sit_up_rep_generator,
     'SIT_UP',
     'reps'),
    (sit_up_hold_generator,
     'SIT_UP',
     'hold'),
    (squat_rep_generator,
     'SQUAT',
     'reps'),
    (squat_hold_generator,
     'SQUAT',
     'hold'),
    (squat_jump_rep_generator,
     'SQUAT_JUMP',
     'reps'),
    (squat_jump_hold_generator,
     'SQUAT_JUMP',
     'hold'),
    (tricep_press_rep_generator,
     'TRICEP_PRESS',
     'reps'),
    (tricep_press_hold_generator,
     'TRICEP_PRESS',
     'hold'),
    (y_fly_rep_generator,
     'Y_FLY',
     'reps'),
    (y_fly_hold_generator,
     'Y_FLY',
     'hold'),
    ])
def test_exercise_generators(generator, exercise_name, execution):
    duration = "10reps" if execution == 'reps' else 'lap.button'
    description = exercise_name.replace('_', ' ').title() if execution == 'reps' else "10-count hold"
    result = generator(10)
    assert result['category'] == 'SUSPENSION'
    assert result['exerciseName'] == exercise_name
    assert result['duration'] == duration
    assert result['target'] == 'NO_TARGET'
    assert result['description'] == description
