import pytest

from garminworkouts.config.generators.strength.leg_curl import (
    band_good_morning_rep_generator,
    band_good_morning_hold_generator,
    bar_good_morning_rep_generator,
    bar_good_morning_hold_generator,
    good_morning_rep_generator,
    good_morning_hold_generator,
    leg_curl_rep_generator,
    leg_curl_hold_generator,
    seated_barbell_good_morning_rep_generator,
    seated_barbell_good_morning_hold_generator,
    single_leg_barbell_good_morning_rep_generator,
    single_leg_barbell_good_morning_hold_generator,
    single_leg_sliding_leg_curl_rep_generator,
    single_leg_sliding_leg_curl_hold_generator,
    sliding_leg_curl_rep_generator,
    sliding_leg_curl_hold_generator,
    split_barbell_good_morning_rep_generator,
    split_barbell_good_morning_hold_generator,
    split_stance_extension_rep_generator,
    split_stance_extension_hold_generator,
    staggered_stance_good_morning_rep_generator,
    staggered_stance_good_morning_hold_generator,
    swiss_ball_hip_raise_and_leg_curl_rep_generator,
    swiss_ball_hip_raise_and_leg_curl_hold_generator,
    weighted_leg_curl_rep_generator,
    weighted_leg_curl_hold_generator,
    zercher_good_morning_rep_generator,
    zercher_good_morning_hold_generator,
    )


@pytest.mark.parametrize("generator, exercise_name, execution", [
    (band_good_morning_rep_generator,
     'BAND_GOOD_MORNING',
     'reps'),
    (band_good_morning_hold_generator,
     'BAND_GOOD_MORNING',
     'hold'),
    (bar_good_morning_rep_generator,
     'BAR_GOOD_MORNING',
     'reps'),
    (bar_good_morning_hold_generator,
     'BAR_GOOD_MORNING',
     'hold'),
    (good_morning_rep_generator,
     'GOOD_MORNING',
     'reps'),
    (good_morning_hold_generator,
     'GOOD_MORNING',
     'hold'),
    (leg_curl_rep_generator,
     'LEG_CURL',
     'reps'),
    (leg_curl_hold_generator,
     'LEG_CURL',
     'hold'),
    (seated_barbell_good_morning_rep_generator,
     'SEATED_BARBELL_GOOD_MORNING',
     'reps'),
    (seated_barbell_good_morning_hold_generator,
     'SEATED_BARBELL_GOOD_MORNING',
     'hold'),
    (single_leg_barbell_good_morning_rep_generator,
     'SINGLE_LEG_BARBELL_GOOD_MORNING',
     'reps'),
    (single_leg_barbell_good_morning_hold_generator,
     'SINGLE_LEG_BARBELL_GOOD_MORNING',
     'hold'),
    (single_leg_sliding_leg_curl_rep_generator,
     'SINGLE_LEG_SLIDING_LEG_CURL',
     'reps'),
    (single_leg_sliding_leg_curl_hold_generator,
     'SINGLE_LEG_SLIDING_LEG_CURL',
     'hold'),
    (sliding_leg_curl_rep_generator,
     'SLIDING_LEG_CURL',
     'reps'),
    (sliding_leg_curl_hold_generator,
     'SLIDING_LEG_CURL',
     'hold'),
    (split_barbell_good_morning_rep_generator,
     'SPLIT_BARBELL_GOOD_MORNING',
     'reps'),
    (split_barbell_good_morning_hold_generator,
     'SPLIT_BARBELL_GOOD_MORNING',
     'hold'),
    (split_stance_extension_rep_generator,
     'SPLIT_STANCE_EXTENSION',
     'reps'),
    (split_stance_extension_hold_generator,
     'SPLIT_STANCE_EXTENSION',
     'hold'),
    (staggered_stance_good_morning_rep_generator,
     'STAGGERED_STANCE_GOOD_MORNING',
     'reps'),
    (staggered_stance_good_morning_hold_generator,
     'STAGGERED_STANCE_GOOD_MORNING',
     'hold'),
    (swiss_ball_hip_raise_and_leg_curl_rep_generator,
     'SWISS_BALL_HIP_RAISE_AND_LEG_CURL',
     'reps'),
    (swiss_ball_hip_raise_and_leg_curl_hold_generator,
     'SWISS_BALL_HIP_RAISE_AND_LEG_CURL',
     'hold'),
    (weighted_leg_curl_rep_generator,
     'WEIGHTED_LEG_CURL',
     'reps'),
    (weighted_leg_curl_hold_generator,
     'WEIGHTED_LEG_CURL',
     'hold'),
    (zercher_good_morning_rep_generator,
     'ZERCHER_GOOD_MORNING',
     'reps'),
    (zercher_good_morning_hold_generator,
     'ZERCHER_GOOD_MORNING',
     'hold'),
    ])
def test_exercise_generators(generator, exercise_name, execution):
    duration = "10reps" if execution == 'reps' else 'lap.button'
    description = exercise_name.replace('_', ' ').title() if execution == 'reps' else "10-count hold"
    result = generator(10)
    assert result['category'] == 'LEG_CURL'
    assert result['exerciseName'] == exercise_name
    assert result['duration'] == duration
    assert result['target'] == 'NO_TARGET'
    assert result['description'] == description
