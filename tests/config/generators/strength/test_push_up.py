import pytest

from garminworkouts.config.generators.strength.push_up import (
    alternating_hands_medicine_ball_push_up_rep_generator,
    alternating_hands_medicine_ball_push_up_hold_generator,
    alternating_staggered_push_up_rep_generator,
    alternating_staggered_push_up_hold_generator,
    biceps_push_up_rep_generator,
    biceps_push_up_hold_generator,
    bosu_ball_push_up_rep_generator,
    bosu_ball_push_up_hold_generator,
    chest_press_with_band_rep_generator,
    chest_press_with_band_hold_generator,
    clapping_push_up_rep_generator,
    clapping_push_up_hold_generator,
    close_grip_medicine_ball_push_up_rep_generator,
    close_grip_medicine_ball_push_up_hold_generator,
    close_hands_push_up_rep_generator,
    close_hands_push_up_hold_generator,
    decline_push_up_rep_generator,
    decline_push_up_hold_generator,
    diamond_push_up_rep_generator,
    diamond_push_up_hold_generator,
    dynamic_push_up_rep_generator,
    dynamic_push_up_hold_generator,
    explosive_crossover_push_up_rep_generator,
    explosive_crossover_push_up_hold_generator,
    explosive_push_up_rep_generator,
    explosive_push_up_hold_generator,
    feet_elevated_side_to_side_push_up_rep_generator,
    feet_elevated_side_to_side_push_up_hold_generator,
    hand_release_push_up_rep_generator,
    hand_release_push_up_hold_generator,
    handstand_push_up_rep_generator,
    handstand_push_up_hold_generator,
    hindu_push_up_rep_generator,
    hindu_push_up_hold_generator,
    incline_push_up_rep_generator,
    incline_push_up_hold_generator,
    isometric_explosive_push_up_rep_generator,
    isometric_explosive_push_up_hold_generator,
    judo_push_up_rep_generator,
    judo_push_up_hold_generator,
    kipping_handstand_push_up_rep_generator,
    kipping_handstand_push_up_hold_generator,
    kipping_parallette_handstand_push_up_rep_generator,
    kipping_parallette_handstand_push_up_hold_generator,
    kneeling_push_up_rep_generator,
    kneeling_push_up_hold_generator,
    medicine_ball_chest_pass_rep_generator,
    medicine_ball_chest_pass_hold_generator,
    medicine_ball_push_up_rep_generator,
    medicine_ball_push_up_hold_generator,
    one_arm_push_up_rep_generator,
    one_arm_push_up_hold_generator,
    parallette_handstand_push_up_rep_generator,
    parallette_handstand_push_up_hold_generator,
    pike_push_up_rep_generator,
    pike_push_up_hold_generator,
    push_up_rep_generator,
    push_up_hold_generator,
    push_up_and_row_rep_generator,
    push_up_and_row_hold_generator,
    push_up_plus_rep_generator,
    push_up_plus_hold_generator,
    push_up_with_feet_on_swiss_ball_rep_generator,
    push_up_with_feet_on_swiss_ball_hold_generator,
    push_up_with_one_hand_on_medicine_ball_rep_generator,
    push_up_with_one_hand_on_medicine_ball_hold_generator,
    ring_handstand_push_up_rep_generator,
    ring_handstand_push_up_hold_generator,
    ring_push_up_rep_generator,
    ring_push_up_hold_generator,
    shoulder_push_up_rep_generator,
    shoulder_push_up_hold_generator,
    shoulder_tapping_push_up_rep_generator,
    shoulder_tapping_push_up_hold_generator,
    single_arm_medicine_ball_push_up_rep_generator,
    single_arm_medicine_ball_push_up_hold_generator,
    spiderman_push_up_rep_generator,
    spiderman_push_up_hold_generator,
    stacked_feet_push_up_rep_generator,
    stacked_feet_push_up_hold_generator,
    staggered_hands_push_up_rep_generator,
    staggered_hands_push_up_hold_generator,
    suspended_push_up_rep_generator,
    suspended_push_up_hold_generator,
    swiss_ball_push_up_rep_generator,
    swiss_ball_push_up_hold_generator,
    swiss_ball_push_up_plus_rep_generator,
    swiss_ball_push_up_plus_hold_generator,
    t_push_up_rep_generator,
    t_push_up_hold_generator,
    triple_stop_push_up_rep_generator,
    triple_stop_push_up_hold_generator,
    weighted_alternating_hands_medicine_ball_push_up_rep_generator,
    weighted_alternating_hands_medicine_ball_push_up_hold_generator,
    weighted_alternating_staggered_push_up_rep_generator,
    weighted_alternating_staggered_push_up_hold_generator,
    weighted_biceps_push_up_rep_generator,
    weighted_biceps_push_up_hold_generator,
    weighted_bosu_ball_push_up_rep_generator,
    weighted_bosu_ball_push_up_hold_generator,
    weighted_clapping_push_up_rep_generator,
    weighted_clapping_push_up_hold_generator,
    weighted_close_grip_medicine_ball_push_up_rep_generator,
    weighted_close_grip_medicine_ball_push_up_hold_generator,
    weighted_close_hands_push_up_rep_generator,
    weighted_close_hands_push_up_hold_generator,
    weighted_decline_push_up_rep_generator,
    weighted_decline_push_up_hold_generator,
    weighted_diamond_push_up_rep_generator,
    weighted_diamond_push_up_hold_generator,
    weighted_explosive_crossover_push_up_rep_generator,
    weighted_explosive_crossover_push_up_hold_generator,
    weighted_explosive_push_up_rep_generator,
    weighted_explosive_push_up_hold_generator,
    weighted_feet_elevated_side_to_side_push_up_rep_generator,
    weighted_feet_elevated_side_to_side_push_up_hold_generator,
    weighted_hand_release_push_up_rep_generator,
    weighted_hand_release_push_up_hold_generator,
    weighted_handstand_push_up_rep_generator,
    weighted_handstand_push_up_hold_generator,
    weighted_hindu_push_up_rep_generator,
    weighted_hindu_push_up_hold_generator,
    weighted_incline_push_up_rep_generator,
    weighted_incline_push_up_hold_generator,
    weighted_isometric_explosive_push_up_rep_generator,
    weighted_isometric_explosive_push_up_hold_generator,
    weighted_judo_push_up_rep_generator,
    weighted_judo_push_up_hold_generator,
    weighted_kneeling_push_up_rep_generator,
    weighted_kneeling_push_up_hold_generator,
    weighted_medicine_ball_push_up_rep_generator,
    weighted_medicine_ball_push_up_hold_generator,
    weighted_one_arm_push_up_rep_generator,
    weighted_one_arm_push_up_hold_generator,
    weighted_parallette_handstand_push_up_rep_generator,
    weighted_parallette_handstand_push_up_hold_generator,
    weighted_pike_push_up_rep_generator,
    weighted_pike_push_up_hold_generator,
    weighted_push_up_rep_generator,
    weighted_push_up_hold_generator,
    weighted_push_up_and_row_rep_generator,
    weighted_push_up_and_row_hold_generator,
    weighted_push_up_plus_rep_generator,
    weighted_push_up_plus_hold_generator,
    weighted_push_up_with_feet_on_swiss_ball_rep_generator,
    weighted_push_up_with_feet_on_swiss_ball_hold_generator,
    weighted_push_up_with_one_hand_on_medicine_ball_rep_generator,
    weighted_push_up_with_one_hand_on_medicine_ball_hold_generator,
    weighted_ring_handstand_push_up_rep_generator,
    weighted_ring_handstand_push_up_hold_generator,
    weighted_ring_push_up_rep_generator,
    weighted_ring_push_up_hold_generator,
    weighted_shoulder_push_up_rep_generator,
    weighted_shoulder_push_up_hold_generator,
    weighted_single_arm_medicine_ball_push_up_rep_generator,
    weighted_single_arm_medicine_ball_push_up_hold_generator,
    weighted_spiderman_push_up_rep_generator,
    weighted_spiderman_push_up_hold_generator,
    weighted_stacked_feet_push_up_rep_generator,
    weighted_stacked_feet_push_up_hold_generator,
    weighted_staggered_hands_push_up_rep_generator,
    weighted_staggered_hands_push_up_hold_generator,
    weighted_suspended_push_up_rep_generator,
    weighted_suspended_push_up_hold_generator,
    weighted_swiss_ball_push_up_rep_generator,
    weighted_swiss_ball_push_up_hold_generator,
    weighted_swiss_ball_push_up_plus_rep_generator,
    weighted_swiss_ball_push_up_plus_hold_generator,
    weighted_t_push_up_rep_generator,
    weighted_t_push_up_hold_generator,
    weighted_triple_stop_push_up_rep_generator,
    weighted_triple_stop_push_up_hold_generator,
    weighted_wide_hands_push_up_rep_generator,
    weighted_wide_hands_push_up_hold_generator,
    wide_grip_push_up_rep_generator,
    wide_grip_push_up_hold_generator,
    wide_hands_push_up_rep_generator,
    wide_hands_push_up_hold_generator,
    )


@pytest.mark.parametrize("generator, exercise_name, execution", [
    (alternating_hands_medicine_ball_push_up_rep_generator,
     'ALTERNATING_HANDS_MEDICINE_BALL_PUSH_UP',
     'reps'),
    (alternating_hands_medicine_ball_push_up_hold_generator,
     'ALTERNATING_HANDS_MEDICINE_BALL_PUSH_UP',
     'hold'),
    (alternating_staggered_push_up_rep_generator,
     'ALTERNATING_STAGGERED_PUSH_UP',
     'reps'),
    (alternating_staggered_push_up_hold_generator,
     'ALTERNATING_STAGGERED_PUSH_UP',
     'hold'),
    (biceps_push_up_rep_generator,
     'BICEPS_PUSH_UP',
     'reps'),
    (biceps_push_up_hold_generator,
     'BICEPS_PUSH_UP',
     'hold'),
    (bosu_ball_push_up_rep_generator,
     'BOSU_BALL_PUSH_UP',
     'reps'),
    (bosu_ball_push_up_hold_generator,
     'BOSU_BALL_PUSH_UP',
     'hold'),
    (chest_press_with_band_rep_generator,
     'CHEST_PRESS_WITH_BAND',
     'reps'),
    (chest_press_with_band_hold_generator,
     'CHEST_PRESS_WITH_BAND',
     'hold'),
    (clapping_push_up_rep_generator,
     'CLAPPING_PUSH_UP',
     'reps'),
    (clapping_push_up_hold_generator,
     'CLAPPING_PUSH_UP',
     'hold'),
    (close_grip_medicine_ball_push_up_rep_generator,
     'CLOSE_GRIP_MEDICINE_BALL_PUSH_UP',
     'reps'),
    (close_grip_medicine_ball_push_up_hold_generator,
     'CLOSE_GRIP_MEDICINE_BALL_PUSH_UP',
     'hold'),
    (close_hands_push_up_rep_generator,
     'CLOSE_HANDS_PUSH_UP',
     'reps'),
    (close_hands_push_up_hold_generator,
     'CLOSE_HANDS_PUSH_UP',
     'hold'),
    (decline_push_up_rep_generator,
     'DECLINE_PUSH_UP',
     'reps'),
    (decline_push_up_hold_generator,
     'DECLINE_PUSH_UP',
     'hold'),
    (diamond_push_up_rep_generator,
     'DIAMOND_PUSH_UP',
     'reps'),
    (diamond_push_up_hold_generator,
     'DIAMOND_PUSH_UP',
     'hold'),
    (dynamic_push_up_rep_generator,
     'DYNAMIC_PUSH_UP',
     'reps'),
    (dynamic_push_up_hold_generator,
     'DYNAMIC_PUSH_UP',
     'hold'),
    (explosive_crossover_push_up_rep_generator,
     'EXPLOSIVE_CROSSOVER_PUSH_UP',
     'reps'),
    (explosive_crossover_push_up_hold_generator,
     'EXPLOSIVE_CROSSOVER_PUSH_UP',
     'hold'),
    (explosive_push_up_rep_generator,
     'EXPLOSIVE_PUSH_UP',
     'reps'),
    (explosive_push_up_hold_generator,
     'EXPLOSIVE_PUSH_UP',
     'hold'),
    (feet_elevated_side_to_side_push_up_rep_generator,
     'FEET_ELEVATED_SIDE_TO_SIDE_PUSH_UP',
     'reps'),
    (feet_elevated_side_to_side_push_up_hold_generator,
     'FEET_ELEVATED_SIDE_TO_SIDE_PUSH_UP',
     'hold'),
    (hand_release_push_up_rep_generator,
     'HAND_RELEASE_PUSH_UP',
     'reps'),
    (hand_release_push_up_hold_generator,
     'HAND_RELEASE_PUSH_UP',
     'hold'),
    (handstand_push_up_rep_generator,
     'HANDSTAND_PUSH_UP',
     'reps'),
    (handstand_push_up_hold_generator,
     'HANDSTAND_PUSH_UP',
     'hold'),
    (hindu_push_up_rep_generator,
     'HINDU_PUSH_UP',
     'reps'),
    (hindu_push_up_hold_generator,
     'HINDU_PUSH_UP',
     'hold'),
    (incline_push_up_rep_generator,
     'INCLINE_PUSH_UP',
     'reps'),
    (incline_push_up_hold_generator,
     'INCLINE_PUSH_UP',
     'hold'),
    (isometric_explosive_push_up_rep_generator,
     'ISOMETRIC_EXPLOSIVE_PUSH_UP',
     'reps'),
    (isometric_explosive_push_up_hold_generator,
     'ISOMETRIC_EXPLOSIVE_PUSH_UP',
     'hold'),
    (judo_push_up_rep_generator,
     'JUDO_PUSH_UP',
     'reps'),
    (judo_push_up_hold_generator,
     'JUDO_PUSH_UP',
     'hold'),
    (kipping_handstand_push_up_rep_generator,
     'KIPPING_HANDSTAND_PUSH_UP',
     'reps'),
    (kipping_handstand_push_up_hold_generator,
     'KIPPING_HANDSTAND_PUSH_UP',
     'hold'),
    (kipping_parallette_handstand_push_up_rep_generator,
     'KIPPING_PARALLETTE_HANDSTAND_PUSH_UP',
     'reps'),
    (kipping_parallette_handstand_push_up_hold_generator,
     'KIPPING_PARALLETTE_HANDSTAND_PUSH_UP',
     'hold'),
    (kneeling_push_up_rep_generator,
     'KNEELING_PUSH_UP',
     'reps'),
    (kneeling_push_up_hold_generator,
     'KNEELING_PUSH_UP',
     'hold'),
    (medicine_ball_chest_pass_rep_generator,
     'MEDICINE_BALL_CHEST_PASS',
     'reps'),
    (medicine_ball_chest_pass_hold_generator,
     'MEDICINE_BALL_CHEST_PASS',
     'hold'),
    (medicine_ball_push_up_rep_generator,
     'MEDICINE_BALL_PUSH_UP',
     'reps'),
    (medicine_ball_push_up_hold_generator,
     'MEDICINE_BALL_PUSH_UP',
     'hold'),
    (one_arm_push_up_rep_generator,
     'ONE_ARM_PUSH_UP',
     'reps'),
    (one_arm_push_up_hold_generator,
     'ONE_ARM_PUSH_UP',
     'hold'),
    (parallette_handstand_push_up_rep_generator,
     'PARALLETTE_HANDSTAND_PUSH_UP',
     'reps'),
    (parallette_handstand_push_up_hold_generator,
     'PARALLETTE_HANDSTAND_PUSH_UP',
     'hold'),
    (pike_push_up_rep_generator,
     'PIKE_PUSH_UP',
     'reps'),
    (pike_push_up_hold_generator,
     'PIKE_PUSH_UP',
     'hold'),
    (push_up_rep_generator,
     'PUSH_UP',
     'reps'),
    (push_up_hold_generator,
     'PUSH_UP',
     'hold'),
    (push_up_and_row_rep_generator,
     'PUSH_UP_AND_ROW',
     'reps'),
    (push_up_and_row_hold_generator,
     'PUSH_UP_AND_ROW',
     'hold'),
    (push_up_plus_rep_generator,
     'PUSH_UP_PLUS',
     'reps'),
    (push_up_plus_hold_generator,
     'PUSH_UP_PLUS',
     'hold'),
    (push_up_with_feet_on_swiss_ball_rep_generator,
     'PUSH_UP_WITH_FEET_ON_SWISS_BALL',
     'reps'),
    (push_up_with_feet_on_swiss_ball_hold_generator,
     'PUSH_UP_WITH_FEET_ON_SWISS_BALL',
     'hold'),
    (push_up_with_one_hand_on_medicine_ball_rep_generator,
     'PUSH_UP_WITH_ONE_HAND_ON_MEDICINE_BALL',
     'reps'),
    (push_up_with_one_hand_on_medicine_ball_hold_generator,
     'PUSH_UP_WITH_ONE_HAND_ON_MEDICINE_BALL',
     'hold'),
    (ring_handstand_push_up_rep_generator,
     'RING_HANDSTAND_PUSH_UP',
     'reps'),
    (ring_handstand_push_up_hold_generator,
     'RING_HANDSTAND_PUSH_UP',
     'hold'),
    (ring_push_up_rep_generator,
     'RING_PUSH_UP',
     'reps'),
    (ring_push_up_hold_generator,
     'RING_PUSH_UP',
     'hold'),
    (shoulder_push_up_rep_generator,
     'SHOULDER_PUSH_UP',
     'reps'),
    (shoulder_push_up_hold_generator,
     'SHOULDER_PUSH_UP',
     'hold'),
    (shoulder_tapping_push_up_rep_generator,
     'SHOULDER_TAPPING_PUSH_UP',
     'reps'),
    (shoulder_tapping_push_up_hold_generator,
     'SHOULDER_TAPPING_PUSH_UP',
     'hold'),
    (single_arm_medicine_ball_push_up_rep_generator,
     'SINGLE_ARM_MEDICINE_BALL_PUSH_UP',
     'reps'),
    (single_arm_medicine_ball_push_up_hold_generator,
     'SINGLE_ARM_MEDICINE_BALL_PUSH_UP',
     'hold'),
    (spiderman_push_up_rep_generator,
     'SPIDERMAN_PUSH_UP',
     'reps'),
    (spiderman_push_up_hold_generator,
     'SPIDERMAN_PUSH_UP',
     'hold'),
    (stacked_feet_push_up_rep_generator,
     'STACKED_FEET_PUSH_UP',
     'reps'),
    (stacked_feet_push_up_hold_generator,
     'STACKED_FEET_PUSH_UP',
     'hold'),
    (staggered_hands_push_up_rep_generator,
     'STAGGERED_HANDS_PUSH_UP',
     'reps'),
    (staggered_hands_push_up_hold_generator,
     'STAGGERED_HANDS_PUSH_UP',
     'hold'),
    (suspended_push_up_rep_generator,
     'SUSPENDED_PUSH_UP',
     'reps'),
    (suspended_push_up_hold_generator,
     'SUSPENDED_PUSH_UP',
     'hold'),
    (swiss_ball_push_up_rep_generator,
     'SWISS_BALL_PUSH_UP',
     'reps'),
    (swiss_ball_push_up_hold_generator,
     'SWISS_BALL_PUSH_UP',
     'hold'),
    (swiss_ball_push_up_plus_rep_generator,
     'SWISS_BALL_PUSH_UP_PLUS',
     'reps'),
    (swiss_ball_push_up_plus_hold_generator,
     'SWISS_BALL_PUSH_UP_PLUS',
     'hold'),
    (t_push_up_rep_generator,
     'T_PUSH_UP',
     'reps'),
    (t_push_up_hold_generator,
     'T_PUSH_UP',
     'hold'),
    (triple_stop_push_up_rep_generator,
     'TRIPLE_STOP_PUSH_UP',
     'reps'),
    (triple_stop_push_up_hold_generator,
     'TRIPLE_STOP_PUSH_UP',
     'hold'),
    (weighted_alternating_hands_medicine_ball_push_up_rep_generator,
     'WEIGHTED_ALTERNATING_HANDS_MEDICINE_BALL_PUSH_UP',
     'reps'),
    (weighted_alternating_hands_medicine_ball_push_up_hold_generator,
     'WEIGHTED_ALTERNATING_HANDS_MEDICINE_BALL_PUSH_UP',
     'hold'),
    (weighted_alternating_staggered_push_up_rep_generator,
     'WEIGHTED_ALTERNATING_STAGGERED_PUSH_UP',
     'reps'),
    (weighted_alternating_staggered_push_up_hold_generator,
     'WEIGHTED_ALTERNATING_STAGGERED_PUSH_UP',
     'hold'),
    (weighted_biceps_push_up_rep_generator,
     'WEIGHTED_BICEPS_PUSH_UP',
     'reps'),
    (weighted_biceps_push_up_hold_generator,
     'WEIGHTED_BICEPS_PUSH_UP',
     'hold'),
    (weighted_bosu_ball_push_up_rep_generator,
     'WEIGHTED_BOSU_BALL_PUSH_UP',
     'reps'),
    (weighted_bosu_ball_push_up_hold_generator,
     'WEIGHTED_BOSU_BALL_PUSH_UP',
     'hold'),
    (weighted_clapping_push_up_rep_generator,
     'WEIGHTED_CLAPPING_PUSH_UP',
     'reps'),
    (weighted_clapping_push_up_hold_generator,
     'WEIGHTED_CLAPPING_PUSH_UP',
     'hold'),
    (weighted_close_grip_medicine_ball_push_up_rep_generator,
     'WEIGHTED_CLOSE_GRIP_MEDICINE_BALL_PUSH_UP',
     'reps'),
    (weighted_close_grip_medicine_ball_push_up_hold_generator,
     'WEIGHTED_CLOSE_GRIP_MEDICINE_BALL_PUSH_UP',
     'hold'),
    (weighted_close_hands_push_up_rep_generator,
     'WEIGHTED_CLOSE_HANDS_PUSH_UP',
     'reps'),
    (weighted_close_hands_push_up_hold_generator,
     'WEIGHTED_CLOSE_HANDS_PUSH_UP',
     'hold'),
    (weighted_decline_push_up_rep_generator,
     'WEIGHTED_DECLINE_PUSH_UP',
     'reps'),
    (weighted_decline_push_up_hold_generator,
     'WEIGHTED_DECLINE_PUSH_UP',
     'hold'),
    (weighted_diamond_push_up_rep_generator,
     'WEIGHTED_DIAMOND_PUSH_UP',
     'reps'),
    (weighted_diamond_push_up_hold_generator,
     'WEIGHTED_DIAMOND_PUSH_UP',
     'hold'),
    (weighted_explosive_crossover_push_up_rep_generator,
     'WEIGHTED_EXPLOSIVE_CROSSOVER_PUSH_UP',
     'reps'),
    (weighted_explosive_crossover_push_up_hold_generator,
     'WEIGHTED_EXPLOSIVE_CROSSOVER_PUSH_UP',
     'hold'),
    (weighted_explosive_push_up_rep_generator,
     'WEIGHTED_EXPLOSIVE_PUSH_UP',
     'reps'),
    (weighted_explosive_push_up_hold_generator,
     'WEIGHTED_EXPLOSIVE_PUSH_UP',
     'hold'),
    (weighted_feet_elevated_side_to_side_push_up_rep_generator,
     'WEIGHTED_FEET_ELEVATED_SIDE_TO_SIDE_PUSH_UP',
     'reps'),
    (weighted_feet_elevated_side_to_side_push_up_hold_generator,
     'WEIGHTED_FEET_ELEVATED_SIDE_TO_SIDE_PUSH_UP',
     'hold'),
    (weighted_hand_release_push_up_rep_generator,
     'WEIGHTED_HAND_RELEASE_PUSH_UP',
     'reps'),
    (weighted_hand_release_push_up_hold_generator,
     'WEIGHTED_HAND_RELEASE_PUSH_UP',
     'hold'),
    (weighted_handstand_push_up_rep_generator,
     'WEIGHTED_HANDSTAND_PUSH_UP',
     'reps'),
    (weighted_handstand_push_up_hold_generator,
     'WEIGHTED_HANDSTAND_PUSH_UP',
     'hold'),
    (weighted_hindu_push_up_rep_generator,
     'WEIGHTED_HINDU_PUSH_UP',
     'reps'),
    (weighted_hindu_push_up_hold_generator,
     'WEIGHTED_HINDU_PUSH_UP',
     'hold'),
    (weighted_incline_push_up_rep_generator,
     'WEIGHTED_INCLINE_PUSH_UP',
     'reps'),
    (weighted_incline_push_up_hold_generator,
     'WEIGHTED_INCLINE_PUSH_UP',
     'hold'),
    (weighted_isometric_explosive_push_up_rep_generator,
     'WEIGHTED_ISOMETRIC_EXPLOSIVE_PUSH_UP',
     'reps'),
    (weighted_isometric_explosive_push_up_hold_generator,
     'WEIGHTED_ISOMETRIC_EXPLOSIVE_PUSH_UP',
     'hold'),
    (weighted_judo_push_up_rep_generator,
     'WEIGHTED_JUDO_PUSH_UP',
     'reps'),
    (weighted_judo_push_up_hold_generator,
     'WEIGHTED_JUDO_PUSH_UP',
     'hold'),
    (weighted_kneeling_push_up_rep_generator,
     'WEIGHTED_KNEELING_PUSH_UP',
     'reps'),
    (weighted_kneeling_push_up_hold_generator,
     'WEIGHTED_KNEELING_PUSH_UP',
     'hold'),
    (weighted_medicine_ball_push_up_rep_generator,
     'WEIGHTED_MEDICINE_BALL_PUSH_UP',
     'reps'),
    (weighted_medicine_ball_push_up_hold_generator,
     'WEIGHTED_MEDICINE_BALL_PUSH_UP',
     'hold'),
    (weighted_one_arm_push_up_rep_generator,
     'WEIGHTED_ONE_ARM_PUSH_UP',
     'reps'),
    (weighted_one_arm_push_up_hold_generator,
     'WEIGHTED_ONE_ARM_PUSH_UP',
     'hold'),
    (weighted_parallette_handstand_push_up_rep_generator,
     'WEIGHTED_PARALLETTE_HANDSTAND_PUSH_UP',
     'reps'),
    (weighted_parallette_handstand_push_up_hold_generator,
     'WEIGHTED_PARALLETTE_HANDSTAND_PUSH_UP',
     'hold'),
    (weighted_pike_push_up_rep_generator,
     'WEIGHTED_PIKE_PUSH_UP',
     'reps'),
    (weighted_pike_push_up_hold_generator,
     'WEIGHTED_PIKE_PUSH_UP',
     'hold'),
    (weighted_push_up_rep_generator,
     'WEIGHTED_PUSH_UP',
     'reps'),
    (weighted_push_up_hold_generator,
     'WEIGHTED_PUSH_UP',
     'hold'),
    (weighted_push_up_and_row_rep_generator,
     'WEIGHTED_PUSH_UP_AND_ROW',
     'reps'),
    (weighted_push_up_and_row_hold_generator,
     'WEIGHTED_PUSH_UP_AND_ROW',
     'hold'),
    (weighted_push_up_plus_rep_generator,
     'WEIGHTED_PUSH_UP_PLUS',
     'reps'),
    (weighted_push_up_plus_hold_generator,
     'WEIGHTED_PUSH_UP_PLUS',
     'hold'),
    (weighted_push_up_with_feet_on_swiss_ball_rep_generator,
     'WEIGHTED_PUSH_UP_WITH_FEET_ON_SWISS_BALL',
     'reps'),
    (weighted_push_up_with_feet_on_swiss_ball_hold_generator,
     'WEIGHTED_PUSH_UP_WITH_FEET_ON_SWISS_BALL',
     'hold'),
    (weighted_push_up_with_one_hand_on_medicine_ball_rep_generator,
     'WEIGHTED_PUSH_UP_WITH_ONE_HAND_ON_MEDICINE_BALL',
     'reps'),
    (weighted_push_up_with_one_hand_on_medicine_ball_hold_generator,
     'WEIGHTED_PUSH_UP_WITH_ONE_HAND_ON_MEDICINE_BALL',
     'hold'),
    (weighted_ring_handstand_push_up_rep_generator,
     'WEIGHTED_RING_HANDSTAND_PUSH_UP',
     'reps'),
    (weighted_ring_handstand_push_up_hold_generator,
     'WEIGHTED_RING_HANDSTAND_PUSH_UP',
     'hold'),
    (weighted_ring_push_up_rep_generator,
     'WEIGHTED_RING_PUSH_UP',
     'reps'),
    (weighted_ring_push_up_hold_generator,
     'WEIGHTED_RING_PUSH_UP',
     'hold'),
    (weighted_shoulder_push_up_rep_generator,
     'WEIGHTED_SHOULDER_PUSH_UP',
     'reps'),
    (weighted_shoulder_push_up_hold_generator,
     'WEIGHTED_SHOULDER_PUSH_UP',
     'hold'),
    (weighted_single_arm_medicine_ball_push_up_rep_generator,
     'WEIGHTED_SINGLE_ARM_MEDICINE_BALL_PUSH_UP',
     'reps'),
    (weighted_single_arm_medicine_ball_push_up_hold_generator,
     'WEIGHTED_SINGLE_ARM_MEDICINE_BALL_PUSH_UP',
     'hold'),
    (weighted_spiderman_push_up_rep_generator,
     'WEIGHTED_SPIDERMAN_PUSH_UP',
     'reps'),
    (weighted_spiderman_push_up_hold_generator,
     'WEIGHTED_SPIDERMAN_PUSH_UP',
     'hold'),
    (weighted_stacked_feet_push_up_rep_generator,
     'WEIGHTED_STACKED_FEET_PUSH_UP',
     'reps'),
    (weighted_stacked_feet_push_up_hold_generator,
     'WEIGHTED_STACKED_FEET_PUSH_UP',
     'hold'),
    (weighted_staggered_hands_push_up_rep_generator,
     'WEIGHTED_STAGGERED_HANDS_PUSH_UP',
     'reps'),
    (weighted_staggered_hands_push_up_hold_generator,
     'WEIGHTED_STAGGERED_HANDS_PUSH_UP',
     'hold'),
    (weighted_suspended_push_up_rep_generator,
     'WEIGHTED_SUSPENDED_PUSH_UP',
     'reps'),
    (weighted_suspended_push_up_hold_generator,
     'WEIGHTED_SUSPENDED_PUSH_UP',
     'hold'),
    (weighted_swiss_ball_push_up_rep_generator,
     'WEIGHTED_SWISS_BALL_PUSH_UP',
     'reps'),
    (weighted_swiss_ball_push_up_hold_generator,
     'WEIGHTED_SWISS_BALL_PUSH_UP',
     'hold'),
    (weighted_swiss_ball_push_up_plus_rep_generator,
     'WEIGHTED_SWISS_BALL_PUSH_UP_PLUS',
     'reps'),
    (weighted_swiss_ball_push_up_plus_hold_generator,
     'WEIGHTED_SWISS_BALL_PUSH_UP_PLUS',
     'hold'),
    (weighted_t_push_up_rep_generator,
     'WEIGHTED_T_PUSH_UP',
     'reps'),
    (weighted_t_push_up_hold_generator,
     'WEIGHTED_T_PUSH_UP',
     'hold'),
    (weighted_triple_stop_push_up_rep_generator,
     'WEIGHTED_TRIPLE_STOP_PUSH_UP',
     'reps'),
    (weighted_triple_stop_push_up_hold_generator,
     'WEIGHTED_TRIPLE_STOP_PUSH_UP',
     'hold'),
    (weighted_wide_hands_push_up_rep_generator,
     'WEIGHTED_WIDE_HANDS_PUSH_UP',
     'reps'),
    (weighted_wide_hands_push_up_hold_generator,
     'WEIGHTED_WIDE_HANDS_PUSH_UP',
     'hold'),
    (wide_grip_push_up_rep_generator,
     'WIDE_GRIP_PUSH_UP',
     'reps'),
    (wide_grip_push_up_hold_generator,
     'WIDE_GRIP_PUSH_UP',
     'hold'),
    (wide_hands_push_up_rep_generator,
     'WIDE_HANDS_PUSH_UP',
     'reps'),
    (wide_hands_push_up_hold_generator,
     'WIDE_HANDS_PUSH_UP',
     'hold'),
    ])
def test_exercise_generators(generator, exercise_name, execution):
    duration = "10reps" if execution == 'reps' else 'lap.button'
    description = exercise_name.replace('_', ' ').title() if execution == 'reps' else "10-count hold"
    result = generator(10)
    assert result['category'] == 'PUSH_UP'
    assert result['exerciseName'] == exercise_name
    assert result['duration'] == duration
    assert result['target'] == 'NO_TARGET'
    assert result['description'] == description
