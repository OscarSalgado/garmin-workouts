import pytest

from garminworkouts.config.generators.strength.chop import (
    cable_pull_through_rep_generator,
    cable_pull_through_hold_generator,
    cable_rotational_lift_rep_generator,
    cable_rotational_lift_hold_generator,
    cable_woodchop_rep_generator,
    cable_woodchop_hold_generator,
    chop_rep_generator,
    chop_hold_generator,
    cross_chop_to_knee_rep_generator,
    cross_chop_to_knee_hold_generator,
    dumbbell_chop_rep_generator,
    dumbbell_chop_hold_generator,
    half_kneeling_rotation_rep_generator,
    half_kneeling_rotation_hold_generator,
    half_kneeling_rotational_chop_rep_generator,
    half_kneeling_rotational_chop_hold_generator,
    half_kneeling_rotational_reverse_chop_rep_generator,
    half_kneeling_rotational_reverse_chop_hold_generator,
    half_kneeling_stability_chop_rep_generator,
    half_kneeling_stability_chop_hold_generator,
    half_kneeling_stability_reverse_chop_rep_generator,
    half_kneeling_stability_reverse_chop_hold_generator,
    kneeling_rotational_chop_rep_generator,
    kneeling_rotational_chop_hold_generator,
    kneeling_rotational_reverse_chop_rep_generator,
    kneeling_rotational_reverse_chop_hold_generator,
    kneeling_stability_chop_rep_generator,
    kneeling_stability_chop_hold_generator,
    kneeling_woodchopper_rep_generator,
    kneeling_woodchopper_hold_generator,
    medicine_ball_wood_chops_rep_generator,
    medicine_ball_wood_chops_hold_generator,
    power_squat_chops_rep_generator,
    power_squat_chops_hold_generator,
    standing_rotational_chop_rep_generator,
    standing_rotational_chop_hold_generator,
    standing_split_rotational_chop_rep_generator,
    standing_split_rotational_chop_hold_generator,
    standing_split_rotational_reverse_chop_rep_generator,
    standing_split_rotational_reverse_chop_hold_generator,
    standing_stability_reverse_chop_rep_generator,
    standing_stability_reverse_chop_hold_generator,
    weighted_cross_chop_to_knee_rep_generator,
    weighted_cross_chop_to_knee_hold_generator,
    weighted_half_kneeling_rotation_rep_generator,
    weighted_half_kneeling_rotation_hold_generator,
    weighted_power_squat_chops_rep_generator,
    weighted_power_squat_chops_hold_generator,
    )


@pytest.mark.parametrize("generator, exercise_name, execution", [
    (cable_pull_through_rep_generator, 'CABLE_PULL_THROUGH', 'reps'),
    (cable_pull_through_hold_generator, 'CABLE_PULL_THROUGH', 'hold'),
    (cable_rotational_lift_rep_generator, 'CABLE_ROTATIONAL_LIFT', 'reps'),
    (cable_rotational_lift_hold_generator, 'CABLE_ROTATIONAL_LIFT', 'hold'),
    (cable_woodchop_rep_generator, 'CABLE_WOODCHOP', 'reps'),
    (cable_woodchop_hold_generator, 'CABLE_WOODCHOP', 'hold'),
    (chop_rep_generator, 'CHOP', 'reps'),
    (chop_hold_generator, 'CHOP', 'hold'),
    (cross_chop_to_knee_rep_generator, 'CROSS_CHOP_TO_KNEE', 'reps'),
    (cross_chop_to_knee_hold_generator, 'CROSS_CHOP_TO_KNEE', 'hold'),
    (dumbbell_chop_rep_generator, 'DUMBBELL_CHOP', 'reps'),
    (dumbbell_chop_hold_generator, 'DUMBBELL_CHOP', 'hold'),
    (half_kneeling_rotation_rep_generator, 'HALF_KNEELING_ROTATION', 'reps'),
    (half_kneeling_rotation_hold_generator, 'HALF_KNEELING_ROTATION', 'hold'),
    (half_kneeling_rotational_chop_rep_generator, 'HALF_KNEELING_ROTATIONAL_CHOP', 'reps'),
    (half_kneeling_rotational_chop_hold_generator, 'HALF_KNEELING_ROTATIONAL_CHOP', 'hold'),
    (half_kneeling_rotational_reverse_chop_rep_generator, 'HALF_KNEELING_ROTATIONAL_REVERSE_CHOP', 'reps'),
    (half_kneeling_rotational_reverse_chop_hold_generator, 'HALF_KNEELING_ROTATIONAL_REVERSE_CHOP', 'hold'),
    (half_kneeling_stability_chop_rep_generator, 'HALF_KNEELING_STABILITY_CHOP', 'reps'),
    (half_kneeling_stability_chop_hold_generator, 'HALF_KNEELING_STABILITY_CHOP', 'hold'),
    (half_kneeling_stability_reverse_chop_rep_generator, 'HALF_KNEELING_STABILITY_REVERSE_CHOP', 'reps'),
    (half_kneeling_stability_reverse_chop_hold_generator, 'HALF_KNEELING_STABILITY_REVERSE_CHOP', 'hold'),
    (kneeling_rotational_chop_rep_generator, 'KNEELING_ROTATIONAL_CHOP', 'reps'),
    (kneeling_rotational_chop_hold_generator, 'KNEELING_ROTATIONAL_CHOP', 'hold'),
    (kneeling_rotational_reverse_chop_rep_generator, 'KNEELING_ROTATIONAL_REVERSE_CHOP', 'reps'),
    (kneeling_rotational_reverse_chop_hold_generator, 'KNEELING_ROTATIONAL_REVERSE_CHOP', 'hold'),
    (kneeling_stability_chop_rep_generator, 'KNEELING_STABILITY_CHOP', 'reps'),
    (kneeling_stability_chop_hold_generator, 'KNEELING_STABILITY_CHOP', 'hold'),
    (kneeling_woodchopper_rep_generator, 'KNEELING_WOODCHOPPER', 'reps'),
    (kneeling_woodchopper_hold_generator, 'KNEELING_WOODCHOPPER', 'hold'),
    (medicine_ball_wood_chops_rep_generator, 'MEDICINE_BALL_WOOD_CHOPS', 'reps'),
    (medicine_ball_wood_chops_hold_generator, 'MEDICINE_BALL_WOOD_CHOPS', 'hold'),
    (power_squat_chops_rep_generator, 'POWER_SQUAT_CHOPS', 'reps'),
    (power_squat_chops_hold_generator, 'POWER_SQUAT_CHOPS', 'hold'),
    (standing_rotational_chop_rep_generator, 'STANDING_ROTATIONAL_CHOP', 'reps'),
    (standing_rotational_chop_hold_generator, 'STANDING_ROTATIONAL_CHOP', 'hold'),
    (standing_split_rotational_chop_rep_generator, 'STANDING_SPLIT_ROTATIONAL_CHOP', 'reps'),
    (standing_split_rotational_chop_hold_generator, 'STANDING_SPLIT_ROTATIONAL_CHOP', 'hold'),
    (standing_split_rotational_reverse_chop_rep_generator, 'STANDING_SPLIT_ROTATIONAL_REVERSE_CHOP', 'reps'),
    (standing_split_rotational_reverse_chop_hold_generator, 'STANDING_SPLIT_ROTATIONAL_REVERSE_CHOP', 'hold'),
    (standing_stability_reverse_chop_rep_generator, 'STANDING_STABILITY_REVERSE_CHOP', 'reps'),
    (standing_stability_reverse_chop_hold_generator, 'STANDING_STABILITY_REVERSE_CHOP', 'hold'),
    (weighted_cross_chop_to_knee_rep_generator, 'WEIGHTED_CROSS_CHOP_TO_KNEE', 'reps'),
    (weighted_cross_chop_to_knee_hold_generator, 'WEIGHTED_CROSS_CHOP_TO_KNEE', 'hold'),
    (weighted_half_kneeling_rotation_rep_generator, 'WEIGHTED_HALF_KNEELING_ROTATION', 'reps'),
    (weighted_half_kneeling_rotation_hold_generator, 'WEIGHTED_HALF_KNEELING_ROTATION', 'hold'),
    (weighted_power_squat_chops_rep_generator, 'WEIGHTED_POWER_SQUAT_CHOPS', 'reps'),
    (weighted_power_squat_chops_hold_generator, 'WEIGHTED_POWER_SQUAT_CHOPS', 'hold'),
    ])
def test_exercise_generators(generator, exercise_name, execution):
    duration = "10reps" if execution == 'reps' else 'lap.button'
    description = exercise_name.replace('_', ' ').title() if execution == 'reps' else "10-count hold"
    result = generator(10)
    assert result['category'] == 'CHOP'
    assert result['exerciseName'] == exercise_name
    assert result['duration'] == duration
    assert result['target'] == 'NO_TARGET'
    assert result['description'] == description