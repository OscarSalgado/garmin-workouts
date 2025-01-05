import pytest

from garminworkouts.config.generators.strength.curl import (
    alternating_dumbbell_biceps_curl_rep_generator,
    alternating_dumbbell_biceps_curl_hold_generator,
    alternating_dumbbell_biceps_curl_on_swiss_ball_rep_generator,
    alternating_dumbbell_biceps_curl_on_swiss_ball_hold_generator,
    alternating_incline_dumbbell_biceps_curl_rep_generator,
    alternating_incline_dumbbell_biceps_curl_hold_generator,
    barbell_biceps_curl_rep_generator,
    barbell_biceps_curl_hold_generator,
    barbell_reverse_wrist_curl_rep_generator,
    barbell_reverse_wrist_curl_hold_generator,
    barbell_wrist_curl_rep_generator,
    barbell_wrist_curl_hold_generator,
    behind_the_back_barbell_reverse_wrist_curl_rep_generator,
    behind_the_back_barbell_reverse_wrist_curl_hold_generator,
    behind_the_back_one_arm_cable_curl_rep_generator,
    behind_the_back_one_arm_cable_curl_hold_generator,
    cable_biceps_curl_rep_generator,
    cable_biceps_curl_hold_generator,
    cable_hammer_curl_rep_generator,
    cable_hammer_curl_hold_generator,
    cheating_barbell_biceps_curl_rep_generator,
    cheating_barbell_biceps_curl_hold_generator,
    close_grip_ez_bar_biceps_curl_rep_generator,
    close_grip_ez_bar_biceps_curl_hold_generator,
    cross_body_dumbbell_hammer_curl_rep_generator,
    cross_body_dumbbell_hammer_curl_hold_generator,
    curl_rep_generator,
    curl_hold_generator,
    dead_hang_biceps_curl_rep_generator,
    dead_hang_biceps_curl_hold_generator,
    decline_hammer_curl_rep_generator,
    decline_hammer_curl_hold_generator,
    dumbbell_biceps_curl_rep_generator,
    dumbbell_biceps_curl_hold_generator,
    dumbbell_biceps_curl_with_static_hold_rep_generator,
    dumbbell_biceps_curl_with_static_hold_hold_generator,
    dumbbell_hammer_curl_rep_generator,
    dumbbell_hammer_curl_hold_generator,
    dumbbell_reverse_wrist_curl_rep_generator,
    dumbbell_reverse_wrist_curl_hold_generator,
    dumbbell_wrist_curl_rep_generator,
    dumbbell_wrist_curl_hold_generator,
    ez_bar_preacher_curl_rep_generator,
    ez_bar_preacher_curl_hold_generator,
    forward_bend_biceps_curl_rep_generator,
    forward_bend_biceps_curl_hold_generator,
    hammer_curl_to_press_rep_generator,
    hammer_curl_to_press_hold_generator,
    incline_dumbbell_biceps_curl_rep_generator,
    incline_dumbbell_biceps_curl_hold_generator,
    incline_offset_thumb_dumbbell_curl_rep_generator,
    incline_offset_thumb_dumbbell_curl_hold_generator,
    kettlebell_biceps_curl_rep_generator,
    kettlebell_biceps_curl_hold_generator,
    lying_concentration_cable_curl_rep_generator,
    lying_concentration_cable_curl_hold_generator,
    one_arm_concentration_curl_rep_generator,
    one_arm_concentration_curl_hold_generator,
    one_arm_preacher_curl_rep_generator,
    one_arm_preacher_curl_hold_generator,
    plate_pinch_curl_rep_generator,
    plate_pinch_curl_hold_generator,
    preacher_curl_with_cable_rep_generator,
    preacher_curl_with_cable_hold_generator,
    reverse_ez_bar_curl_rep_generator,
    reverse_ez_bar_curl_hold_generator,
    reverse_grip_barbell_biceps_curl_rep_generator,
    reverse_grip_barbell_biceps_curl_hold_generator,
    reverse_grip_wrist_curl_rep_generator,
    reverse_grip_wrist_curl_hold_generator,
    seated_alternating_dumbbell_biceps_curl_rep_generator,
    seated_alternating_dumbbell_biceps_curl_hold_generator,
    seated_dumbbell_biceps_curl_rep_generator,
    seated_dumbbell_biceps_curl_hold_generator,
    seated_reverse_dumbbell_curl_rep_generator,
    seated_reverse_dumbbell_curl_hold_generator,
    split_stance_offset_pinky_dumbbell_curl_rep_generator,
    split_stance_offset_pinky_dumbbell_curl_hold_generator,
    standing_alternating_dumbbell_curls_rep_generator,
    standing_alternating_dumbbell_curls_hold_generator,
    standing_dumbbell_biceps_curl_rep_generator,
    standing_dumbbell_biceps_curl_hold_generator,
    standing_ez_bar_biceps_curl_rep_generator,
    standing_ez_bar_biceps_curl_hold_generator,
    standing_zottman_biceps_curl_rep_generator,
    standing_zottman_biceps_curl_hold_generator,
    static_curl_rep_generator,
    static_curl_hold_generator,
    swiss_ball_dumbbell_overhead_triceps_extension_rep_generator,
    swiss_ball_dumbbell_overhead_triceps_extension_hold_generator,
    swiss_ball_ez_bar_preacher_curl_rep_generator,
    swiss_ball_ez_bar_preacher_curl_hold_generator,
    twisting_standing_dumbbell_biceps_curl_rep_generator,
    twisting_standing_dumbbell_biceps_curl_hold_generator,
    wide_grip_ez_bar_biceps_curl_rep_generator,
    wide_grip_ez_bar_biceps_curl_hold_generator,
    )


@pytest.mark.parametrize("generator, exercise_name, execution", [
    (alternating_dumbbell_biceps_curl_rep_generator,
     'ALTERNATING_DUMBBELL_BICEPS_CURL',
     'reps'),
    (alternating_dumbbell_biceps_curl_hold_generator,
     'ALTERNATING_DUMBBELL_BICEPS_CURL',
     'hold'),
    (alternating_dumbbell_biceps_curl_on_swiss_ball_rep_generator,
     'ALTERNATING_DUMBBELL_BICEPS_CURL_ON_SWISS_BALL',
     'reps'),
    (alternating_dumbbell_biceps_curl_on_swiss_ball_hold_generator,
     'ALTERNATING_DUMBBELL_BICEPS_CURL_ON_SWISS_BALL',
     'hold'),
    (alternating_incline_dumbbell_biceps_curl_rep_generator,
     'ALTERNATING_INCLINE_DUMBBELL_BICEPS_CURL',
     'reps'),
    (alternating_incline_dumbbell_biceps_curl_hold_generator,
     'ALTERNATING_INCLINE_DUMBBELL_BICEPS_CURL',
     'hold'),
    (barbell_biceps_curl_rep_generator,
     'BARBELL_BICEPS_CURL',
     'reps'),
    (barbell_biceps_curl_hold_generator,
     'BARBELL_BICEPS_CURL',
     'hold'),
    (barbell_reverse_wrist_curl_rep_generator,
     'BARBELL_REVERSE_WRIST_CURL',
     'reps'),
    (barbell_reverse_wrist_curl_hold_generator,
     'BARBELL_REVERSE_WRIST_CURL',
     'hold'),
    (barbell_wrist_curl_rep_generator,
     'BARBELL_WRIST_CURL',
     'reps'),
    (barbell_wrist_curl_hold_generator,
     'BARBELL_WRIST_CURL',
     'hold'),
    (behind_the_back_barbell_reverse_wrist_curl_rep_generator,
     'BEHIND_THE_BACK_BARBELL_REVERSE_WRIST_CURL',
     'reps'),
    (behind_the_back_barbell_reverse_wrist_curl_hold_generator,
     'BEHIND_THE_BACK_BARBELL_REVERSE_WRIST_CURL',
     'hold'),
    (behind_the_back_one_arm_cable_curl_rep_generator,
     'BEHIND_THE_BACK_ONE_ARM_CABLE_CURL',
     'reps'),
    (behind_the_back_one_arm_cable_curl_hold_generator,
     'BEHIND_THE_BACK_ONE_ARM_CABLE_CURL',
     'hold'),
    (cable_biceps_curl_rep_generator,
     'CABLE_BICEPS_CURL',
     'reps'),
    (cable_biceps_curl_hold_generator,
     'CABLE_BICEPS_CURL',
     'hold'),
    (cable_hammer_curl_rep_generator,
     'CABLE_HAMMER_CURL',
     'reps'),
    (cable_hammer_curl_hold_generator,
     'CABLE_HAMMER_CURL',
     'hold'),
    (cheating_barbell_biceps_curl_rep_generator,
     'CHEATING_BARBELL_BICEPS_CURL',
     'reps'),
    (cheating_barbell_biceps_curl_hold_generator,
     'CHEATING_BARBELL_BICEPS_CURL',
     'hold'),
    (close_grip_ez_bar_biceps_curl_rep_generator,
     'CLOSE_GRIP_EZ_BAR_BICEPS_CURL',
     'reps'),
    (close_grip_ez_bar_biceps_curl_hold_generator,
     'CLOSE_GRIP_EZ_BAR_BICEPS_CURL',
     'hold'),
    (cross_body_dumbbell_hammer_curl_rep_generator,
     'CROSS_BODY_DUMBBELL_HAMMER_CURL',
     'reps'),
    (cross_body_dumbbell_hammer_curl_hold_generator,
     'CROSS_BODY_DUMBBELL_HAMMER_CURL',
     'hold'),
    (curl_rep_generator,
     'CURL',
     'reps'),
    (curl_hold_generator,
     'CURL',
     'hold'),
    (dead_hang_biceps_curl_rep_generator,
     'DEAD_HANG_BICEPS_CURL',
     'reps'),
    (dead_hang_biceps_curl_hold_generator,
     'DEAD_HANG_BICEPS_CURL',
     'hold'),
    (decline_hammer_curl_rep_generator,
     'DECLINE_HAMMER_CURL',
     'reps'),
    (decline_hammer_curl_hold_generator,
     'DECLINE_HAMMER_CURL',
     'hold'),
    (dumbbell_biceps_curl_rep_generator,
     'DUMBBELL_BICEPS_CURL',
     'reps'),
    (dumbbell_biceps_curl_hold_generator,
     'DUMBBELL_BICEPS_CURL',
     'hold'),
    (dumbbell_biceps_curl_with_static_hold_rep_generator,
     'DUMBBELL_BICEPS_CURL_WITH_STATIC_HOLD',
     'reps'),
    (dumbbell_biceps_curl_with_static_hold_hold_generator,
     'DUMBBELL_BICEPS_CURL_WITH_STATIC_HOLD',
     'hold'),
    (dumbbell_hammer_curl_rep_generator,
     'DUMBBELL_HAMMER_CURL',
     'reps'),
    (dumbbell_hammer_curl_hold_generator,
     'DUMBBELL_HAMMER_CURL',
     'hold'),
    (dumbbell_reverse_wrist_curl_rep_generator,
     'DUMBBELL_REVERSE_WRIST_CURL',
     'reps'),
    (dumbbell_reverse_wrist_curl_hold_generator,
     'DUMBBELL_REVERSE_WRIST_CURL',
     'hold'),
    (dumbbell_wrist_curl_rep_generator,
     'DUMBBELL_WRIST_CURL',
     'reps'),
    (dumbbell_wrist_curl_hold_generator,
     'DUMBBELL_WRIST_CURL',
     'hold'),
    (ez_bar_preacher_curl_rep_generator,
     'EZ_BAR_PREACHER_CURL',
     'reps'),
    (ez_bar_preacher_curl_hold_generator,
     'EZ_BAR_PREACHER_CURL',
     'hold'),
    (forward_bend_biceps_curl_rep_generator,
     'FORWARD_BEND_BICEPS_CURL',
     'reps'),
    (forward_bend_biceps_curl_hold_generator,
     'FORWARD_BEND_BICEPS_CURL',
     'hold'),
    (hammer_curl_to_press_rep_generator,
     'HAMMER_CURL_TO_PRESS',
     'reps'),
    (hammer_curl_to_press_hold_generator,
     'HAMMER_CURL_TO_PRESS',
     'hold'),
    (incline_dumbbell_biceps_curl_rep_generator,
     'INCLINE_DUMBBELL_BICEPS_CURL',
     'reps'),
    (incline_dumbbell_biceps_curl_hold_generator,
     'INCLINE_DUMBBELL_BICEPS_CURL',
     'hold'),
    (incline_offset_thumb_dumbbell_curl_rep_generator,
     'INCLINE_OFFSET_THUMB_DUMBBELL_CURL',
     'reps'),
    (incline_offset_thumb_dumbbell_curl_hold_generator,
     'INCLINE_OFFSET_THUMB_DUMBBELL_CURL',
     'hold'),
    (kettlebell_biceps_curl_rep_generator,
     'KETTLEBELL_BICEPS_CURL',
     'reps'),
    (kettlebell_biceps_curl_hold_generator,
     'KETTLEBELL_BICEPS_CURL',
     'hold'),
    (lying_concentration_cable_curl_rep_generator,
     'LYING_CONCENTRATION_CABLE_CURL',
     'reps'),
    (lying_concentration_cable_curl_hold_generator,
     'LYING_CONCENTRATION_CABLE_CURL',
     'hold'),
    (one_arm_concentration_curl_rep_generator,
     'ONE_ARM_CONCENTRATION_CURL',
     'reps'),
    (one_arm_concentration_curl_hold_generator,
     'ONE_ARM_CONCENTRATION_CURL',
     'hold'),
    (one_arm_preacher_curl_rep_generator,
     'ONE_ARM_PREACHER_CURL',
     'reps'),
    (one_arm_preacher_curl_hold_generator,
     'ONE_ARM_PREACHER_CURL',
     'hold'),
    (plate_pinch_curl_rep_generator,
     'PLATE_PINCH_CURL',
     'reps'),
    (plate_pinch_curl_hold_generator,
     'PLATE_PINCH_CURL',
     'hold'),
    (preacher_curl_with_cable_rep_generator,
     'PREACHER_CURL_WITH_CABLE',
     'reps'),
    (preacher_curl_with_cable_hold_generator,
     'PREACHER_CURL_WITH_CABLE',
     'hold'),
    (reverse_ez_bar_curl_rep_generator,
     'REVERSE_EZ_BAR_CURL',
     'reps'),
    (reverse_ez_bar_curl_hold_generator,
     'REVERSE_EZ_BAR_CURL',
     'hold'),
    (reverse_grip_barbell_biceps_curl_rep_generator,
     'REVERSE_GRIP_BARBELL_BICEPS_CURL',
     'reps'),
    (reverse_grip_barbell_biceps_curl_hold_generator,
     'REVERSE_GRIP_BARBELL_BICEPS_CURL',
     'hold'),
    (reverse_grip_wrist_curl_rep_generator,
     'REVERSE_GRIP_WRIST_CURL',
     'reps'),
    (reverse_grip_wrist_curl_hold_generator,
     'REVERSE_GRIP_WRIST_CURL',
     'hold'),
    (seated_alternating_dumbbell_biceps_curl_rep_generator,
     'SEATED_ALTERNATING_DUMBBELL_BICEPS_CURL',
     'reps'),
    (seated_alternating_dumbbell_biceps_curl_hold_generator,
     'SEATED_ALTERNATING_DUMBBELL_BICEPS_CURL',
     'hold'),
    (seated_dumbbell_biceps_curl_rep_generator,
     'SEATED_DUMBBELL_BICEPS_CURL',
     'reps'),
    (seated_dumbbell_biceps_curl_hold_generator,
     'SEATED_DUMBBELL_BICEPS_CURL',
     'hold'),
    (seated_reverse_dumbbell_curl_rep_generator,
     'SEATED_REVERSE_DUMBBELL_CURL',
     'reps'),
    (seated_reverse_dumbbell_curl_hold_generator,
     'SEATED_REVERSE_DUMBBELL_CURL',
     'hold'),
    (split_stance_offset_pinky_dumbbell_curl_rep_generator,
     'SPLIT_STANCE_OFFSET_PINKY_DUMBBELL_CURL',
     'reps'),
    (split_stance_offset_pinky_dumbbell_curl_hold_generator,
     'SPLIT_STANCE_OFFSET_PINKY_DUMBBELL_CURL',
     'hold'),
    (standing_alternating_dumbbell_curls_rep_generator,
     'STANDING_ALTERNATING_DUMBBELL_CURLS',
     'reps'),
    (standing_alternating_dumbbell_curls_hold_generator,
     'STANDING_ALTERNATING_DUMBBELL_CURLS',
     'hold'),
    (standing_dumbbell_biceps_curl_rep_generator,
     'STANDING_DUMBBELL_BICEPS_CURL',
     'reps'),
    (standing_dumbbell_biceps_curl_hold_generator,
     'STANDING_DUMBBELL_BICEPS_CURL',
     'hold'),
    (standing_ez_bar_biceps_curl_rep_generator,
     'STANDING_EZ_BAR_BICEPS_CURL',
     'reps'),
    (standing_ez_bar_biceps_curl_hold_generator,
     'STANDING_EZ_BAR_BICEPS_CURL',
     'hold'),
    (standing_zottman_biceps_curl_rep_generator,
     'STANDING_ZOTTMAN_BICEPS_CURL',
     'reps'),
    (standing_zottman_biceps_curl_hold_generator,
     'STANDING_ZOTTMAN_BICEPS_CURL',
     'hold'),
    (static_curl_rep_generator,
     'STATIC_CURL',
     'reps'),
    (static_curl_hold_generator,
     'STATIC_CURL',
     'hold'),
    (swiss_ball_dumbbell_overhead_triceps_extension_rep_generator,
     'SWISS_BALL_DUMBBELL_OVERHEAD_TRICEPS_EXTENSION',
     'reps'),
    (swiss_ball_dumbbell_overhead_triceps_extension_hold_generator,
     'SWISS_BALL_DUMBBELL_OVERHEAD_TRICEPS_EXTENSION',
     'hold'),
    (swiss_ball_ez_bar_preacher_curl_rep_generator,
     'SWISS_BALL_EZ_BAR_PREACHER_CURL',
     'reps'),
    (swiss_ball_ez_bar_preacher_curl_hold_generator,
     'SWISS_BALL_EZ_BAR_PREACHER_CURL',
     'hold'),
    (twisting_standing_dumbbell_biceps_curl_rep_generator,
     'TWISTING_STANDING_DUMBBELL_BICEPS_CURL',
     'reps'),
    (twisting_standing_dumbbell_biceps_curl_hold_generator,
     'TWISTING_STANDING_DUMBBELL_BICEPS_CURL',
     'hold'),
    (wide_grip_ez_bar_biceps_curl_rep_generator,
     'WIDE_GRIP_EZ_BAR_BICEPS_CURL',
     'reps'),
    (wide_grip_ez_bar_biceps_curl_hold_generator,
     'WIDE_GRIP_EZ_BAR_BICEPS_CURL',
     'hold'),
    ])
def test_exercise_generators(generator, exercise_name, execution):
    duration = "10reps" if execution == 'reps' else 'lap.button'
    description = exercise_name.replace('_', ' ').title() if execution == 'reps' else "10-count hold"
    result = generator(10)
    assert result['category'] == 'CURL'
    assert result['exerciseName'] == exercise_name
    assert result['duration'] == duration
    assert result['target'] == 'NO_TARGET'
    assert result['description'] == description
