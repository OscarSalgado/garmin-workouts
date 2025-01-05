import pytest

from garminworkouts.config.generators.strength.row import (
    alternating_dumbbell_row_rep_generator,
    alternating_dumbbell_row_hold_generator,
    banded_face_pulls_rep_generator,
    banded_face_pulls_hold_generator,
    barbell_row_rep_generator,
    barbell_row_hold_generator,
    barbell_straight_leg_deadlift_to_row_rep_generator,
    barbell_straight_leg_deadlift_to_row_hold_generator,
    bent_over_row_with_barbell_rep_generator,
    bent_over_row_with_barbell_hold_generator,
    bent_over_row_with_dumbell_rep_generator,
    bent_over_row_with_dumbell_hold_generator,
    cable_row_standing_rep_generator,
    cable_row_standing_hold_generator,
    chest_supported_dumbbell_row_rep_generator,
    chest_supported_dumbbell_row_hold_generator,
    decline_ring_row_rep_generator,
    decline_ring_row_hold_generator,
    dumbbell_row_rep_generator,
    dumbbell_row_hold_generator,
    elevated_feet_inverted_row_rep_generator,
    elevated_feet_inverted_row_hold_generator,
    elevated_ring_row_rep_generator,
    elevated_ring_row_hold_generator,
    face_pull_rep_generator,
    face_pull_hold_generator,
    face_pull_with_external_rotation_rep_generator,
    face_pull_with_external_rotation_hold_generator,
    indoor_row_rep_generator,
    indoor_row_hold_generator,
    inverted_row_rep_generator,
    inverted_row_hold_generator,
    inverted_row_with_feet_on_swiss_ball_rep_generator,
    inverted_row_with_feet_on_swiss_ball_hold_generator,
    kettlebell_row_rep_generator,
    kettlebell_row_hold_generator,
    modified_inverted_row_rep_generator,
    modified_inverted_row_hold_generator,
    neutral_grip_alternating_dumbbell_row_rep_generator,
    neutral_grip_alternating_dumbbell_row_hold_generator,
    one_arm_bent_over_row_rep_generator,
    one_arm_bent_over_row_hold_generator,
    one_legged_dumbbell_row_rep_generator,
    one_legged_dumbbell_row_hold_generator,
    renegade_row_rep_generator,
    renegade_row_hold_generator,
    reverse_grip_barbell_row_rep_generator,
    reverse_grip_barbell_row_hold_generator,
    ring_row_rep_generator,
    ring_row_hold_generator,
    rope_handle_cable_row_rep_generator,
    rope_handle_cable_row_hold_generator,
    row_rep_generator,
    row_hold_generator,
    seated_cable_row_rep_generator,
    seated_cable_row_hold_generator,
    seated_dumbbell_row_rep_generator,
    seated_dumbbell_row_hold_generator,
    seated_underhand_grip_cable_row_rep_generator,
    seated_underhand_grip_cable_row_hold_generator,
    single_arm_cable_row_rep_generator,
    single_arm_cable_row_hold_generator,
    single_arm_cable_row_and_rotation_rep_generator,
    single_arm_cable_row_and_rotation_hold_generator,
    single_arm_inverted_row_rep_generator,
    single_arm_inverted_row_hold_generator,
    single_arm_neutral_grip_dumbbell_row_rep_generator,
    single_arm_neutral_grip_dumbbell_row_hold_generator,
    single_arm_neutral_grip_dumbbell_row_and_rotation_rep_generator,
    single_arm_neutral_grip_dumbbell_row_and_rotation_hold_generator,
    suspended_inverted_row_rep_generator,
    suspended_inverted_row_hold_generator,
    t_bar_row_rep_generator,
    t_bar_row_hold_generator,
    towel_grip_inverted_row_rep_generator,
    towel_grip_inverted_row_hold_generator,
    trx_inverted_row_rep_generator,
    trx_inverted_row_hold_generator,
    underhand_grip_cable_row_rep_generator,
    underhand_grip_cable_row_hold_generator,
    v_grip_cable_row_rep_generator,
    v_grip_cable_row_hold_generator,
    weighted_elevated_feet_inverted_row_rep_generator,
    weighted_elevated_feet_inverted_row_hold_generator,
    weighted_inverted_row_rep_generator,
    weighted_inverted_row_hold_generator,
    weighted_inverted_row_with_feet_on_swiss_ball_rep_generator,
    weighted_inverted_row_with_feet_on_swiss_ball_hold_generator,
    weighted_modified_inverted_row_rep_generator,
    weighted_modified_inverted_row_hold_generator,
    weighted_row_rep_generator,
    weighted_row_hold_generator,
    weighted_single_arm_inverted_row_rep_generator,
    weighted_single_arm_inverted_row_hold_generator,
    weighted_suspended_inverted_row_rep_generator,
    weighted_suspended_inverted_row_hold_generator,
    weighted_towel_grip_inverted_row_rep_generator,
    weighted_towel_grip_inverted_row_hold_generator,
    weighted_trx_inverted_row_rep_generator,
    weighted_trx_inverted_row_hold_generator,
    wide_grip_seated_cable_row_rep_generator,
    wide_grip_seated_cable_row_hold_generator,
    )


@pytest.mark.parametrize("generator, exercise_name, execution", [
    (alternating_dumbbell_row_rep_generator,
     'ALTERNATING_DUMBBELL_ROW',
     'reps'),
    (alternating_dumbbell_row_hold_generator,
     'ALTERNATING_DUMBBELL_ROW',
     'hold'),
    (banded_face_pulls_rep_generator,
     'BANDED_FACE_PULLS',
     'reps'),
    (banded_face_pulls_hold_generator,
     'BANDED_FACE_PULLS',
     'hold'),
    (barbell_row_rep_generator,
     'BARBELL_ROW',
     'reps'),
    (barbell_row_hold_generator,
     'BARBELL_ROW',
     'hold'),
    (barbell_straight_leg_deadlift_to_row_rep_generator,
     'BARBELL_STRAIGHT_LEG_DEADLIFT_TO_ROW',
     'reps'),
    (barbell_straight_leg_deadlift_to_row_hold_generator,
     'BARBELL_STRAIGHT_LEG_DEADLIFT_TO_ROW',
     'hold'),
    (bent_over_row_with_barbell_rep_generator,
     'BENT_OVER_ROW_WITH_BARBELL',
     'reps'),
    (bent_over_row_with_barbell_hold_generator,
     'BENT_OVER_ROW_WITH_BARBELL',
     'hold'),
    (bent_over_row_with_dumbell_rep_generator,
     'BENT_OVER_ROW_WITH_DUMBELL',
     'reps'),
    (bent_over_row_with_dumbell_hold_generator,
     'BENT_OVER_ROW_WITH_DUMBELL',
     'hold'),
    (cable_row_standing_rep_generator,
     'CABLE_ROW_STANDING',
     'reps'),
    (cable_row_standing_hold_generator,
     'CABLE_ROW_STANDING',
     'hold'),
    (chest_supported_dumbbell_row_rep_generator,
     'CHEST_SUPPORTED_DUMBBELL_ROW',
     'reps'),
    (chest_supported_dumbbell_row_hold_generator,
     'CHEST_SUPPORTED_DUMBBELL_ROW',
     'hold'),
    (decline_ring_row_rep_generator,
     'DECLINE_RING_ROW',
     'reps'),
    (decline_ring_row_hold_generator,
     'DECLINE_RING_ROW',
     'hold'),
    (dumbbell_row_rep_generator,
     'DUMBBELL_ROW',
     'reps'),
    (dumbbell_row_hold_generator,
     'DUMBBELL_ROW',
     'hold'),
    (elevated_feet_inverted_row_rep_generator,
     'ELEVATED_FEET_INVERTED_ROW',
     'reps'),
    (elevated_feet_inverted_row_hold_generator,
     'ELEVATED_FEET_INVERTED_ROW',
     'hold'),
    (elevated_ring_row_rep_generator,
     'ELEVATED_RING_ROW',
     'reps'),
    (elevated_ring_row_hold_generator,
     'ELEVATED_RING_ROW',
     'hold'),
    (face_pull_rep_generator,
     'FACE_PULL',
     'reps'),
    (face_pull_hold_generator,
     'FACE_PULL',
     'hold'),
    (face_pull_with_external_rotation_rep_generator,
     'FACE_PULL_WITH_EXTERNAL_ROTATION',
     'reps'),
    (face_pull_with_external_rotation_hold_generator,
     'FACE_PULL_WITH_EXTERNAL_ROTATION',
     'hold'),
    (indoor_row_rep_generator,
     'INDOOR_ROW',
     'reps'),
    (indoor_row_hold_generator,
     'INDOOR_ROW',
     'hold'),
    (inverted_row_rep_generator,
     'INVERTED_ROW',
     'reps'),
    (inverted_row_hold_generator,
     'INVERTED_ROW',
     'hold'),
    (inverted_row_with_feet_on_swiss_ball_rep_generator,
     'INVERTED_ROW_WITH_FEET_ON_SWISS_BALL',
     'reps'),
    (inverted_row_with_feet_on_swiss_ball_hold_generator,
     'INVERTED_ROW_WITH_FEET_ON_SWISS_BALL',
     'hold'),
    (kettlebell_row_rep_generator,
     'KETTLEBELL_ROW',
     'reps'),
    (kettlebell_row_hold_generator,
     'KETTLEBELL_ROW',
     'hold'),
    (modified_inverted_row_rep_generator,
     'MODIFIED_INVERTED_ROW',
     'reps'),
    (modified_inverted_row_hold_generator,
     'MODIFIED_INVERTED_ROW',
     'hold'),
    (neutral_grip_alternating_dumbbell_row_rep_generator,
     'NEUTRAL_GRIP_ALTERNATING_DUMBBELL_ROW',
     'reps'),
    (neutral_grip_alternating_dumbbell_row_hold_generator,
     'NEUTRAL_GRIP_ALTERNATING_DUMBBELL_ROW',
     'hold'),
    (one_arm_bent_over_row_rep_generator,
     'ONE_ARM_BENT_OVER_ROW',
     'reps'),
    (one_arm_bent_over_row_hold_generator,
     'ONE_ARM_BENT_OVER_ROW',
     'hold'),
    (one_legged_dumbbell_row_rep_generator,
     'ONE_LEGGED_DUMBBELL_ROW',
     'reps'),
    (one_legged_dumbbell_row_hold_generator,
     'ONE_LEGGED_DUMBBELL_ROW',
     'hold'),
    (renegade_row_rep_generator,
     'RENEGADE_ROW',
     'reps'),
    (renegade_row_hold_generator,
     'RENEGADE_ROW',
     'hold'),
    (reverse_grip_barbell_row_rep_generator,
     'REVERSE_GRIP_BARBELL_ROW',
     'reps'),
    (reverse_grip_barbell_row_hold_generator,
     'REVERSE_GRIP_BARBELL_ROW',
     'hold'),
    (ring_row_rep_generator,
     'RING_ROW',
     'reps'),
    (ring_row_hold_generator,
     'RING_ROW',
     'hold'),
    (rope_handle_cable_row_rep_generator,
     'ROPE_HANDLE_CABLE_ROW',
     'reps'),
    (rope_handle_cable_row_hold_generator,
     'ROPE_HANDLE_CABLE_ROW',
     'hold'),
    (row_rep_generator,
     'ROW',
     'reps'),
    (row_hold_generator,
     'ROW',
     'hold'),
    (seated_cable_row_rep_generator,
     'SEATED_CABLE_ROW',
     'reps'),
    (seated_cable_row_hold_generator,
     'SEATED_CABLE_ROW',
     'hold'),
    (seated_dumbbell_row_rep_generator,
     'SEATED_DUMBBELL_ROW',
     'reps'),
    (seated_dumbbell_row_hold_generator,
     'SEATED_DUMBBELL_ROW',
     'hold'),
    (seated_underhand_grip_cable_row_rep_generator,
     'SEATED_UNDERHAND_GRIP_CABLE_ROW',
     'reps'),
    (seated_underhand_grip_cable_row_hold_generator,
     'SEATED_UNDERHAND_GRIP_CABLE_ROW',
     'hold'),
    (single_arm_cable_row_rep_generator,
     'SINGLE_ARM_CABLE_ROW',
     'reps'),
    (single_arm_cable_row_hold_generator,
     'SINGLE_ARM_CABLE_ROW',
     'hold'),
    (single_arm_cable_row_and_rotation_rep_generator,
     'SINGLE_ARM_CABLE_ROW_AND_ROTATION',
     'reps'),
    (single_arm_cable_row_and_rotation_hold_generator,
     'SINGLE_ARM_CABLE_ROW_AND_ROTATION',
     'hold'),
    (single_arm_inverted_row_rep_generator,
     'SINGLE_ARM_INVERTED_ROW',
     'reps'),
    (single_arm_inverted_row_hold_generator,
     'SINGLE_ARM_INVERTED_ROW',
     'hold'),
    (single_arm_neutral_grip_dumbbell_row_rep_generator,
     'SINGLE_ARM_NEUTRAL_GRIP_DUMBBELL_ROW',
     'reps'),
    (single_arm_neutral_grip_dumbbell_row_hold_generator,
     'SINGLE_ARM_NEUTRAL_GRIP_DUMBBELL_ROW',
     'hold'),
    (single_arm_neutral_grip_dumbbell_row_and_rotation_rep_generator,
     'SINGLE_ARM_NEUTRAL_GRIP_DUMBBELL_ROW_AND_ROTATION',
     'reps'),
    (single_arm_neutral_grip_dumbbell_row_and_rotation_hold_generator,
     'SINGLE_ARM_NEUTRAL_GRIP_DUMBBELL_ROW_AND_ROTATION',
     'hold'),
    (suspended_inverted_row_rep_generator,
     'SUSPENDED_INVERTED_ROW',
     'reps'),
    (suspended_inverted_row_hold_generator,
     'SUSPENDED_INVERTED_ROW',
     'hold'),
    (t_bar_row_rep_generator,
     'T_BAR_ROW',
     'reps'),
    (t_bar_row_hold_generator,
     'T_BAR_ROW',
     'hold'),
    (towel_grip_inverted_row_rep_generator,
     'TOWEL_GRIP_INVERTED_ROW',
     'reps'),
    (towel_grip_inverted_row_hold_generator,
     'TOWEL_GRIP_INVERTED_ROW',
     'hold'),
    (trx_inverted_row_rep_generator,
     'TRX_INVERTED_ROW',
     'reps'),
    (trx_inverted_row_hold_generator,
     'TRX_INVERTED_ROW',
     'hold'),
    (underhand_grip_cable_row_rep_generator,
     'UNDERHAND_GRIP_CABLE_ROW',
     'reps'),
    (underhand_grip_cable_row_hold_generator,
     'UNDERHAND_GRIP_CABLE_ROW',
     'hold'),
    (v_grip_cable_row_rep_generator,
     'V_GRIP_CABLE_ROW',
     'reps'),
    (v_grip_cable_row_hold_generator,
     'V_GRIP_CABLE_ROW',
     'hold'),
    (weighted_elevated_feet_inverted_row_rep_generator,
     'WEIGHTED_ELEVATED_FEET_INVERTED_ROW',
     'reps'),
    (weighted_elevated_feet_inverted_row_hold_generator,
     'WEIGHTED_ELEVATED_FEET_INVERTED_ROW',
     'hold'),
    (weighted_inverted_row_rep_generator,
     'WEIGHTED_INVERTED_ROW',
     'reps'),
    (weighted_inverted_row_hold_generator,
     'WEIGHTED_INVERTED_ROW',
     'hold'),
    (weighted_inverted_row_with_feet_on_swiss_ball_rep_generator,
     'WEIGHTED_INVERTED_ROW_WITH_FEET_ON_SWISS_BALL',
     'reps'),
    (weighted_inverted_row_with_feet_on_swiss_ball_hold_generator,
     'WEIGHTED_INVERTED_ROW_WITH_FEET_ON_SWISS_BALL',
     'hold'),
    (weighted_modified_inverted_row_rep_generator,
     'WEIGHTED_MODIFIED_INVERTED_ROW',
     'reps'),
    (weighted_modified_inverted_row_hold_generator,
     'WEIGHTED_MODIFIED_INVERTED_ROW',
     'hold'),
    (weighted_row_rep_generator,
     'WEIGHTED_ROW',
     'reps'),
    (weighted_row_hold_generator,
     'WEIGHTED_ROW',
     'hold'),
    (weighted_single_arm_inverted_row_rep_generator,
     'WEIGHTED_SINGLE_ARM_INVERTED_ROW',
     'reps'),
    (weighted_single_arm_inverted_row_hold_generator,
     'WEIGHTED_SINGLE_ARM_INVERTED_ROW',
     'hold'),
    (weighted_suspended_inverted_row_rep_generator,
     'WEIGHTED_SUSPENDED_INVERTED_ROW',
     'reps'),
    (weighted_suspended_inverted_row_hold_generator,
     'WEIGHTED_SUSPENDED_INVERTED_ROW',
     'hold'),
    (weighted_towel_grip_inverted_row_rep_generator,
     'WEIGHTED_TOWEL_GRIP_INVERTED_ROW',
     'reps'),
    (weighted_towel_grip_inverted_row_hold_generator,
     'WEIGHTED_TOWEL_GRIP_INVERTED_ROW',
     'hold'),
    (weighted_trx_inverted_row_rep_generator,
     'WEIGHTED_TRX_INVERTED_ROW',
     'reps'),
    (weighted_trx_inverted_row_hold_generator,
     'WEIGHTED_TRX_INVERTED_ROW',
     'hold'),
    (wide_grip_seated_cable_row_rep_generator,
     'WIDE_GRIP_SEATED_CABLE_ROW',
     'reps'),
    (wide_grip_seated_cable_row_hold_generator,
     'WIDE_GRIP_SEATED_CABLE_ROW',
     'hold'),
    ])
def test_exercise_generators(generator, exercise_name, execution):
    duration = "10reps" if execution == 'reps' else 'lap.button'
    description = exercise_name.replace('_', ' ').title() if execution == 'reps' else "10-count hold"
    result = generator(10)
    assert result['category'] == 'ROW'
    assert result['exerciseName'] == exercise_name
    assert result['duration'] == duration
    assert result['target'] == 'NO_TARGET'
    assert result['description'] == description
