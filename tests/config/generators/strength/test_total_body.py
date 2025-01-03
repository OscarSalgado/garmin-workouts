import pytest

from garminworkouts.config.generators.strength.total_body import (
    barbell_burpee_rep_generator,
    barbell_burpee_hold_generator,
    burpee_rep_generator,
    burpee_hold_generator,
    burpee_box_jump_rep_generator,
    burpee_box_jump_hold_generator,
    burpee_box_jump_over_rep_generator,
    burpee_box_jump_over_hold_generator,
    burpee_box_jump_step_up_over_rep_generator,
    burpee_box_jump_step_up_over_hold_generator,
    high_pull_burpee_rep_generator,
    high_pull_burpee_hold_generator,
    lateral_barbell_burpee_rep_generator,
    lateral_barbell_burpee_hold_generator,
    man_makers_rep_generator,
    man_makers_hold_generator,
    one_arm_burpee_rep_generator,
    one_arm_burpee_hold_generator,
    squat_plank_push_up_rep_generator,
    squat_plank_push_up_hold_generator,
    squat_thrusts_rep_generator,
    squat_thrusts_hold_generator,
    standing_t_rotation_balance_rep_generator,
    standing_t_rotation_balance_hold_generator,
    total_body_burpee_over_bar_rep_generator,
    total_body_burpee_over_bar_hold_generator,
    weighted_burpee_rep_generator,
    weighted_burpee_hold_generator,
    weighted_burpee_box_jump_rep_generator,
    weighted_burpee_box_jump_hold_generator,
    weighted_squat_plank_push_up_rep_generator,
    weighted_squat_plank_push_up_hold_generator,
    weighted_squat_thrusts_rep_generator,
    weighted_squat_thrusts_hold_generator,
    weighted_standing_t_rotation_balance_rep_generator,
    weighted_standing_t_rotation_balance_hold_generator,
    )


@pytest.mark.parametrize("generator, exercise_name, execution", [
    (barbell_burpee_rep_generator, 'BARBELL_BURPEE', 'reps'),
    (barbell_burpee_hold_generator, 'BARBELL_BURPEE', 'hold'),
    (burpee_rep_generator, 'BURPEE', 'reps'),
    (burpee_hold_generator, 'BURPEE', 'hold'),
    (burpee_box_jump_rep_generator, 'BURPEE_BOX_JUMP', 'reps'),
    (burpee_box_jump_hold_generator, 'BURPEE_BOX_JUMP', 'hold'),
    (burpee_box_jump_over_rep_generator, 'BURPEE_BOX_JUMP_OVER', 'reps'),
    (burpee_box_jump_over_hold_generator, 'BURPEE_BOX_JUMP_OVER', 'hold'),
    (burpee_box_jump_step_up_over_rep_generator, 'BURPEE_BOX_JUMP_STEP_UP_OVER', 'reps'),
    (burpee_box_jump_step_up_over_hold_generator, 'BURPEE_BOX_JUMP_STEP_UP_OVER', 'hold'),
    (high_pull_burpee_rep_generator, 'HIGH_PULL_BURPEE', 'reps'),
    (high_pull_burpee_hold_generator, 'HIGH_PULL_BURPEE', 'hold'),
    (lateral_barbell_burpee_rep_generator, 'LATERAL_BARBELL_BURPEE', 'reps'),
    (lateral_barbell_burpee_hold_generator, 'LATERAL_BARBELL_BURPEE', 'hold'),
    (man_makers_rep_generator, 'MAN_MAKERS', 'reps'),
    (man_makers_hold_generator, 'MAN_MAKERS', 'hold'),
    (one_arm_burpee_rep_generator, 'ONE_ARM_BURPEE', 'reps'),
    (one_arm_burpee_hold_generator, 'ONE_ARM_BURPEE', 'hold'),
    (squat_plank_push_up_rep_generator, 'SQUAT_PLANK_PUSH_UP', 'reps'),
    (squat_plank_push_up_hold_generator, 'SQUAT_PLANK_PUSH_UP', 'hold'),
    (squat_thrusts_rep_generator, 'SQUAT_THRUSTS', 'reps'),
    (squat_thrusts_hold_generator, 'SQUAT_THRUSTS', 'hold'),
    (standing_t_rotation_balance_rep_generator, 'STANDING_T_ROTATION_BALANCE', 'reps'),
    (standing_t_rotation_balance_hold_generator, 'STANDING_T_ROTATION_BALANCE', 'hold'),
    (total_body_burpee_over_bar_rep_generator, 'TOTAL_BODY_BURPEE_OVER_BAR', 'reps'),
    (total_body_burpee_over_bar_hold_generator, 'TOTAL_BODY_BURPEE_OVER_BAR', 'hold'),
    (weighted_burpee_rep_generator, 'WEIGHTED_BURPEE', 'reps'),
    (weighted_burpee_hold_generator, 'WEIGHTED_BURPEE', 'hold'),
    (weighted_burpee_box_jump_rep_generator, 'WEIGHTED_BURPEE_BOX_JUMP', 'reps'),
    (weighted_burpee_box_jump_hold_generator, 'WEIGHTED_BURPEE_BOX_JUMP', 'hold'),
    (weighted_squat_plank_push_up_rep_generator, 'WEIGHTED_SQUAT_PLANK_PUSH_UP', 'reps'),
    (weighted_squat_plank_push_up_hold_generator, 'WEIGHTED_SQUAT_PLANK_PUSH_UP', 'hold'),
    (weighted_squat_thrusts_rep_generator, 'WEIGHTED_SQUAT_THRUSTS', 'reps'),
    (weighted_squat_thrusts_hold_generator, 'WEIGHTED_SQUAT_THRUSTS', 'hold'),
    (weighted_standing_t_rotation_balance_rep_generator, 'WEIGHTED_STANDING_T_ROTATION_BALANCE', 'reps'),
    (weighted_standing_t_rotation_balance_hold_generator, 'WEIGHTED_STANDING_T_ROTATION_BALANCE', 'hold'),
    ])
def test_exercise_generators(generator, exercise_name, execution):
    duration = "10reps" if execution == 'reps' else 'lap.button'
    description = exercise_name.replace('_', ' ').title() if execution == 'reps' else "10-count hold"
    result = generator(10)
    assert result['category'] == 'TOTAL_BODY'
    assert result['exerciseName'] == exercise_name
    assert result['duration'] == duration
    assert result['target'] == 'NO_TARGET'
    assert result['description'] == description