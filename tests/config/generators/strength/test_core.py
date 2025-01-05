import pytest

from garminworkouts.config.generators.strength.core import (
    abs_jabs_rep_generator,
    abs_jabs_hold_generator,
    alternating_plate_reach_rep_generator,
    alternating_plate_reach_hold_generator,
    alternating_slide_out_rep_generator,
    alternating_slide_out_hold_generator,
    barbell_rollout_rep_generator,
    barbell_rollout_hold_generator,
    body_bar_oblique_twist_rep_generator,
    body_bar_oblique_twist_hold_generator,
    cable_core_press_rep_generator,
    cable_core_press_hold_generator,
    cable_side_bend_rep_generator,
    cable_side_bend_hold_generator,
    core_rep_generator,
    core_hold_generator,
    crescent_circle_rep_generator,
    crescent_circle_hold_generator,
    cycling_russian_twist_rep_generator,
    cycling_russian_twist_hold_generator,
    elevated_feet_russian_twist_rep_generator,
    elevated_feet_russian_twist_hold_generator,
    ghd_back_extensions_rep_generator,
    ghd_back_extensions_hold_generator,
    half_turkish_get_up_rep_generator,
    half_turkish_get_up_hold_generator,
    hanging_l_sit_rep_generator,
    hanging_l_sit_hold_generator,
    inchworm_rep_generator,
    inchworm_hold_generator,
    kettlebell_windmill_rep_generator,
    kettlebell_windmill_hold_generator,
    kneeling_ab_wheel_rep_generator,
    kneeling_ab_wheel_hold_generator,
    l_sit_rep_generator,
    l_sit_hold_generator,
    modified_front_lever_rep_generator,
    modified_front_lever_hold_generator,
    open_knee_tucks_rep_generator,
    open_knee_tucks_hold_generator,
    overhead_walk_rep_generator,
    overhead_walk_hold_generator,
    ring_l_sit_rep_generator,
    ring_l_sit_hold_generator,
    russian_twist_rep_generator,
    russian_twist_hold_generator,
    side_abs_leg_lift_rep_generator,
    side_abs_leg_lift_hold_generator,
    side_bend_rep_generator,
    side_bend_hold_generator,
    swiss_ball_jackknife_rep_generator,
    swiss_ball_jackknife_hold_generator,
    swiss_ball_pike_rep_generator,
    swiss_ball_pike_hold_generator,
    swiss_ball_rollout_rep_generator,
    swiss_ball_rollout_hold_generator,
    toes_to_elbows_rep_generator,
    toes_to_elbows_hold_generator,
    triangle_hip_press_rep_generator,
    triangle_hip_press_hold_generator,
    trx_suspended_jackknife_rep_generator,
    trx_suspended_jackknife_hold_generator,
    turkish_get_up_rep_generator,
    turkish_get_up_hold_generator,
    u_boat_rep_generator,
    u_boat_hold_generator,
    weighted_ring_l_sit_rep_generator,
    weighted_ring_l_sit_hold_generator,
    weighted_abs_jabs_rep_generator,
    weighted_abs_jabs_hold_generator,
    weighted_alternating_slide_out_rep_generator,
    weighted_alternating_slide_out_hold_generator,
    weighted_barbell_rollout_rep_generator,
    weighted_barbell_rollout_hold_generator,
    weighted_crescent_circle_rep_generator,
    weighted_crescent_circle_hold_generator,
    weighted_cycling_russian_twist_rep_generator,
    weighted_cycling_russian_twist_hold_generator,
    weighted_elevated_feet_russian_twist_rep_generator,
    weighted_elevated_feet_russian_twist_hold_generator,
    weighted_ghd_back_extensions_rep_generator,
    weighted_ghd_back_extensions_hold_generator,
    weighted_hanging_l_sit_rep_generator,
    weighted_hanging_l_sit_hold_generator,
    weighted_kneeling_ab_wheel_rep_generator,
    weighted_kneeling_ab_wheel_hold_generator,
    weighted_l_sit_rep_generator,
    weighted_l_sit_hold_generator,
    weighted_modified_front_lever_rep_generator,
    weighted_modified_front_lever_hold_generator,
    weighted_open_knee_tucks_rep_generator,
    weighted_open_knee_tucks_hold_generator,
    weighted_side_abs_leg_lift_rep_generator,
    weighted_side_abs_leg_lift_hold_generator,
    weighted_side_bend_rep_generator,
    weighted_side_bend_hold_generator,
    weighted_swiss_ball_jackknife_rep_generator,
    weighted_swiss_ball_jackknife_hold_generator,
    weighted_swiss_ball_pike_rep_generator,
    weighted_swiss_ball_pike_hold_generator,
    weighted_swiss_ball_rollout_rep_generator,
    weighted_swiss_ball_rollout_hold_generator,
    weighted_triangle_hip_press_rep_generator,
    weighted_triangle_hip_press_hold_generator,
    weighted_trx_suspended_jackknife_rep_generator,
    weighted_trx_suspended_jackknife_hold_generator,
    weighted_u_boat_rep_generator,
    weighted_u_boat_hold_generator,
    weighted_windmill_switches_rep_generator,
    weighted_windmill_switches_hold_generator,
    windmill_switches_rep_generator,
    windmill_switches_hold_generator,
    )


@pytest.mark.parametrize("generator, exercise_name, execution", [
    (abs_jabs_rep_generator,
     'ABS_JABS',
     'reps'),
    (abs_jabs_hold_generator,
     'ABS_JABS',
     'hold'),
    (alternating_plate_reach_rep_generator,
     'ALTERNATING_PLATE_REACH',
     'reps'),
    (alternating_plate_reach_hold_generator,
     'ALTERNATING_PLATE_REACH',
     'hold'),
    (alternating_slide_out_rep_generator,
     'ALTERNATING_SLIDE_OUT',
     'reps'),
    (alternating_slide_out_hold_generator,
     'ALTERNATING_SLIDE_OUT',
     'hold'),
    (barbell_rollout_rep_generator,
     'BARBELL_ROLLOUT',
     'reps'),
    (barbell_rollout_hold_generator,
     'BARBELL_ROLLOUT',
     'hold'),
    (body_bar_oblique_twist_rep_generator,
     'BODY_BAR_OBLIQUE_TWIST',
     'reps'),
    (body_bar_oblique_twist_hold_generator,
     'BODY_BAR_OBLIQUE_TWIST',
     'hold'),
    (cable_core_press_rep_generator,
     'CABLE_CORE_PRESS',
     'reps'),
    (cable_core_press_hold_generator,
     'CABLE_CORE_PRESS',
     'hold'),
    (cable_side_bend_rep_generator,
     'CABLE_SIDE_BEND',
     'reps'),
    (cable_side_bend_hold_generator,
     'CABLE_SIDE_BEND',
     'hold'),
    (core_rep_generator,
     'CORE',
     'reps'),
    (core_hold_generator,
     'CORE',
     'hold'),
    (crescent_circle_rep_generator,
     'CRESCENT_CIRCLE',
     'reps'),
    (crescent_circle_hold_generator,
     'CRESCENT_CIRCLE',
     'hold'),
    (cycling_russian_twist_rep_generator,
     'CYCLING_RUSSIAN_TWIST',
     'reps'),
    (cycling_russian_twist_hold_generator,
     'CYCLING_RUSSIAN_TWIST',
     'hold'),
    (elevated_feet_russian_twist_rep_generator,
     'ELEVATED_FEET_RUSSIAN_TWIST',
     'reps'),
    (elevated_feet_russian_twist_hold_generator,
     'ELEVATED_FEET_RUSSIAN_TWIST',
     'hold'),
    (ghd_back_extensions_rep_generator,
     'GHD_BACK_EXTENSIONS',
     'reps'),
    (ghd_back_extensions_hold_generator,
     'GHD_BACK_EXTENSIONS',
     'hold'),
    (half_turkish_get_up_rep_generator,
     'HALF_TURKISH_GET_UP',
     'reps'),
    (half_turkish_get_up_hold_generator,
     'HALF_TURKISH_GET_UP',
     'hold'),
    (hanging_l_sit_rep_generator,
     'HANGING_L_SIT',
     'reps'),
    (hanging_l_sit_hold_generator,
     'HANGING_L_SIT',
     'hold'),
    (inchworm_rep_generator,
     'INCHWORM',
     'reps'),
    (inchworm_hold_generator,
     'INCHWORM',
     'hold'),
    (kettlebell_windmill_rep_generator,
     'KETTLEBELL_WINDMILL',
     'reps'),
    (kettlebell_windmill_hold_generator,
     'KETTLEBELL_WINDMILL',
     'hold'),
    (kneeling_ab_wheel_rep_generator,
     'KNEELING_AB_WHEEL',
     'reps'),
    (kneeling_ab_wheel_hold_generator,
     'KNEELING_AB_WHEEL',
     'hold'),
    (l_sit_rep_generator,
     'L_SIT',
     'reps'),
    (l_sit_hold_generator,
     'L_SIT',
     'hold'),
    (modified_front_lever_rep_generator,
     'MODIFIED_FRONT_LEVER',
     'reps'),
    (modified_front_lever_hold_generator,
     'MODIFIED_FRONT_LEVER',
     'hold'),
    (open_knee_tucks_rep_generator,
     'OPEN_KNEE_TUCKS',
     'reps'),
    (open_knee_tucks_hold_generator,
     'OPEN_KNEE_TUCKS',
     'hold'),
    (overhead_walk_rep_generator,
     'OVERHEAD_WALK',
     'reps'),
    (overhead_walk_hold_generator,
     'OVERHEAD_WALK',
     'hold'),
    (ring_l_sit_rep_generator,
     'RING_L_SIT',
     'reps'),
    (ring_l_sit_hold_generator,
     'RING_L_SIT',
     'hold'),
    (russian_twist_rep_generator,
     'RUSSIAN_TWIST',
     'reps'),
    (russian_twist_hold_generator,
     'RUSSIAN_TWIST',
     'hold'),
    (side_abs_leg_lift_rep_generator,
     'SIDE_ABS_LEG_LIFT',
     'reps'),
    (side_abs_leg_lift_hold_generator,
     'SIDE_ABS_LEG_LIFT',
     'hold'),
    (side_bend_rep_generator,
     'SIDE_BEND',
     'reps'),
    (side_bend_hold_generator,
     'SIDE_BEND',
     'hold'),
    (swiss_ball_jackknife_rep_generator,
     'SWISS_BALL_JACKKNIFE',
     'reps'),
    (swiss_ball_jackknife_hold_generator,
     'SWISS_BALL_JACKKNIFE',
     'hold'),
    (swiss_ball_pike_rep_generator,
     'SWISS_BALL_PIKE',
     'reps'),
    (swiss_ball_pike_hold_generator,
     'SWISS_BALL_PIKE',
     'hold'),
    (swiss_ball_rollout_rep_generator,
     'SWISS_BALL_ROLLOUT',
     'reps'),
    (swiss_ball_rollout_hold_generator,
     'SWISS_BALL_ROLLOUT',
     'hold'),
    (toes_to_elbows_rep_generator,
     'TOES_TO_ELBOWS',
     'reps'),
    (toes_to_elbows_hold_generator,
     'TOES_TO_ELBOWS',
     'hold'),
    (triangle_hip_press_rep_generator,
     'TRIANGLE_HIP_PRESS',
     'reps'),
    (triangle_hip_press_hold_generator,
     'TRIANGLE_HIP_PRESS',
     'hold'),
    (trx_suspended_jackknife_rep_generator,
     'TRX_SUSPENDED_JACKKNIFE',
     'reps'),
    (trx_suspended_jackknife_hold_generator,
     'TRX_SUSPENDED_JACKKNIFE',
     'hold'),
    (turkish_get_up_rep_generator,
     'TURKISH_GET_UP',
     'reps'),
    (turkish_get_up_hold_generator,
     'TURKISH_GET_UP',
     'hold'),
    (u_boat_rep_generator,
     'U_BOAT',
     'reps'),
    (u_boat_hold_generator,
     'U_BOAT',
     'hold'),
    (weighted_ring_l_sit_rep_generator,
     'WEIGHTED_RING_L_SIT',
     'reps'),
    (weighted_ring_l_sit_hold_generator,
     'WEIGHTED_RING_L_SIT',
     'hold'),
    (weighted_abs_jabs_rep_generator,
     'WEIGHTED_ABS_JABS',
     'reps'),
    (weighted_abs_jabs_hold_generator,
     'WEIGHTED_ABS_JABS',
     'hold'),
    (weighted_alternating_slide_out_rep_generator,
     'WEIGHTED_ALTERNATING_SLIDE_OUT',
     'reps'),
    (weighted_alternating_slide_out_hold_generator,
     'WEIGHTED_ALTERNATING_SLIDE_OUT',
     'hold'),
    (weighted_barbell_rollout_rep_generator,
     'WEIGHTED_BARBELL_ROLLOUT',
     'reps'),
    (weighted_barbell_rollout_hold_generator,
     'WEIGHTED_BARBELL_ROLLOUT',
     'hold'),
    (weighted_crescent_circle_rep_generator,
     'WEIGHTED_CRESCENT_CIRCLE',
     'reps'),
    (weighted_crescent_circle_hold_generator,
     'WEIGHTED_CRESCENT_CIRCLE',
     'hold'),
    (weighted_cycling_russian_twist_rep_generator,
     'WEIGHTED_CYCLING_RUSSIAN_TWIST',
     'reps'),
    (weighted_cycling_russian_twist_hold_generator,
     'WEIGHTED_CYCLING_RUSSIAN_TWIST',
     'hold'),
    (weighted_elevated_feet_russian_twist_rep_generator,
     'WEIGHTED_ELEVATED_FEET_RUSSIAN_TWIST',
     'reps'),
    (weighted_elevated_feet_russian_twist_hold_generator,
     'WEIGHTED_ELEVATED_FEET_RUSSIAN_TWIST',
     'hold'),
    (weighted_ghd_back_extensions_rep_generator,
     'WEIGHTED_GHD_BACK_EXTENSIONS',
     'reps'),
    (weighted_ghd_back_extensions_hold_generator,
     'WEIGHTED_GHD_BACK_EXTENSIONS',
     'hold'),
    (weighted_hanging_l_sit_rep_generator,
     'WEIGHTED_HANGING_L_SIT',
     'reps'),
    (weighted_hanging_l_sit_hold_generator,
     'WEIGHTED_HANGING_L_SIT',
     'hold'),
    (weighted_kneeling_ab_wheel_rep_generator,
     'WEIGHTED_KNEELING_AB_WHEEL',
     'reps'),
    (weighted_kneeling_ab_wheel_hold_generator,
     'WEIGHTED_KNEELING_AB_WHEEL',
     'hold'),
    (weighted_l_sit_rep_generator,
     'WEIGHTED_L_SIT',
     'reps'),
    (weighted_l_sit_hold_generator,
     'WEIGHTED_L_SIT',
     'hold'),
    (weighted_modified_front_lever_rep_generator,
     'WEIGHTED_MODIFIED_FRONT_LEVER',
     'reps'),
    (weighted_modified_front_lever_hold_generator,
     'WEIGHTED_MODIFIED_FRONT_LEVER',
     'hold'),
    (weighted_open_knee_tucks_rep_generator,
     'WEIGHTED_OPEN_KNEE_TUCKS',
     'reps'),
    (weighted_open_knee_tucks_hold_generator,
     'WEIGHTED_OPEN_KNEE_TUCKS',
     'hold'),
    (weighted_side_abs_leg_lift_rep_generator,
     'WEIGHTED_SIDE_ABS_LEG_LIFT',
     'reps'),
    (weighted_side_abs_leg_lift_hold_generator,
     'WEIGHTED_SIDE_ABS_LEG_LIFT',
     'hold'),
    (weighted_side_bend_rep_generator,
     'WEIGHTED_SIDE_BEND',
     'reps'),
    (weighted_side_bend_hold_generator,
     'WEIGHTED_SIDE_BEND',
     'hold'),
    (weighted_swiss_ball_jackknife_rep_generator,
     'WEIGHTED_SWISS_BALL_JACKKNIFE',
     'reps'),
    (weighted_swiss_ball_jackknife_hold_generator,
     'WEIGHTED_SWISS_BALL_JACKKNIFE',
     'hold'),
    (weighted_swiss_ball_pike_rep_generator,
     'WEIGHTED_SWISS_BALL_PIKE',
     'reps'),
    (weighted_swiss_ball_pike_hold_generator,
     'WEIGHTED_SWISS_BALL_PIKE',
     'hold'),
    (weighted_swiss_ball_rollout_rep_generator,
     'WEIGHTED_SWISS_BALL_ROLLOUT',
     'reps'),
    (weighted_swiss_ball_rollout_hold_generator,
     'WEIGHTED_SWISS_BALL_ROLLOUT',
     'hold'),
    (weighted_triangle_hip_press_rep_generator,
     'WEIGHTED_TRIANGLE_HIP_PRESS',
     'reps'),
    (weighted_triangle_hip_press_hold_generator,
     'WEIGHTED_TRIANGLE_HIP_PRESS',
     'hold'),
    (weighted_trx_suspended_jackknife_rep_generator,
     'WEIGHTED_TRX_SUSPENDED_JACKKNIFE',
     'reps'),
    (weighted_trx_suspended_jackknife_hold_generator,
     'WEIGHTED_TRX_SUSPENDED_JACKKNIFE',
     'hold'),
    (weighted_u_boat_rep_generator,
     'WEIGHTED_U_BOAT',
     'reps'),
    (weighted_u_boat_hold_generator,
     'WEIGHTED_U_BOAT',
     'hold'),
    (weighted_windmill_switches_rep_generator,
     'WEIGHTED_WINDMILL_SWITCHES',
     'reps'),
    (weighted_windmill_switches_hold_generator,
     'WEIGHTED_WINDMILL_SWITCHES',
     'hold'),
    (windmill_switches_rep_generator,
     'WINDMILL_SWITCHES',
     'reps'),
    (windmill_switches_hold_generator,
     'WINDMILL_SWITCHES',
     'hold'),
    ])
def test_exercise_generators(generator, exercise_name, execution):
    duration = "10reps" if execution == 'reps' else 'lap.button'
    description = exercise_name.replace('_', ' ').title() if execution == 'reps' else "10-count hold"
    result = generator(10)
    assert result['category'] == 'CORE'
    assert result['exerciseName'] == exercise_name
    assert result['duration'] == duration
    assert result['target'] == 'NO_TARGET'
    assert result['description'] == description
