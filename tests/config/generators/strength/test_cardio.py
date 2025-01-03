import pytest

from garminworkouts.config.generators.strength.cardio import (
    bob_and_weave_circle_rep_generator,
    bob_and_weave_circle_hold_generator,
    cardio_core_crawl_rep_generator,
    cardio_core_crawl_hold_generator,
    double_under_rep_generator,
    double_under_hold_generator,
    jump_rope_rep_generator,
    jump_rope_hold_generator,
    jump_rope_crossover_rep_generator,
    jump_rope_crossover_hold_generator,
    jump_rope_jog_rep_generator,
    jump_rope_jog_hold_generator,
    jumping_jacks_rep_generator,
    jumping_jacks_hold_generator,
    ski_moguls_rep_generator,
    ski_moguls_hold_generator,
    split_jacks_rep_generator,
    split_jacks_hold_generator,
    squat_jacks_rep_generator,
    squat_jacks_hold_generator,
    triple_under_rep_generator,
    triple_under_hold_generator,
    weighted_bob_and_weave_circle_rep_generator,
    weighted_bob_and_weave_circle_hold_generator,
    weighted_cardio_core_crawl_rep_generator,
    weighted_cardio_core_crawl_hold_generator,
    weighted_double_under_rep_generator,
    weighted_double_under_hold_generator,
    weighted_jump_rope_rep_generator,
    weighted_jump_rope_hold_generator,
    weighted_jump_rope_crossover_rep_generator,
    weighted_jump_rope_crossover_hold_generator,
    weighted_jump_rope_jog_rep_generator,
    weighted_jump_rope_jog_hold_generator,
    weighted_jumping_jacks_rep_generator,
    weighted_jumping_jacks_hold_generator,
    weighted_ski_moguls_rep_generator,
    weighted_ski_moguls_hold_generator,
    weighted_split_jacks_rep_generator,
    weighted_split_jacks_hold_generator,
    weighted_squat_jacks_rep_generator,
    weighted_squat_jacks_hold_generator,
    weighted_triple_under_rep_generator,
    weighted_triple_under_hold_generator,
    )


@pytest.mark.parametrize("generator, exercise_name, execution", [
    (bob_and_weave_circle_rep_generator, 'BOB_AND_WEAVE_CIRCLE', 'reps'),
    (bob_and_weave_circle_hold_generator, 'BOB_AND_WEAVE_CIRCLE', 'hold'),
    (cardio_core_crawl_rep_generator, 'CARDIO_CORE_CRAWL', 'reps'),
    (cardio_core_crawl_hold_generator, 'CARDIO_CORE_CRAWL', 'hold'),
    (double_under_rep_generator, 'DOUBLE_UNDER', 'reps'),
    (double_under_hold_generator, 'DOUBLE_UNDER', 'hold'),
    (jump_rope_rep_generator, 'JUMP_ROPE', 'reps'),
    (jump_rope_hold_generator, 'JUMP_ROPE', 'hold'),
    (jump_rope_crossover_rep_generator, 'JUMP_ROPE_CROSSOVER', 'reps'),
    (jump_rope_crossover_hold_generator, 'JUMP_ROPE_CROSSOVER', 'hold'),
    (jump_rope_jog_rep_generator, 'JUMP_ROPE_JOG', 'reps'),
    (jump_rope_jog_hold_generator, 'JUMP_ROPE_JOG', 'hold'),
    (jumping_jacks_rep_generator, 'JUMPING_JACKS', 'reps'),
    (jumping_jacks_hold_generator, 'JUMPING_JACKS', 'hold'),
    (ski_moguls_rep_generator, 'SKI_MOGULS', 'reps'),
    (ski_moguls_hold_generator, 'SKI_MOGULS', 'hold'),
    (split_jacks_rep_generator, 'SPLIT_JACKS', 'reps'),
    (split_jacks_hold_generator, 'SPLIT_JACKS', 'hold'),
    (squat_jacks_rep_generator, 'SQUAT_JACKS', 'reps'),
    (squat_jacks_hold_generator, 'SQUAT_JACKS', 'hold'),
    (triple_under_rep_generator, 'TRIPLE_UNDER', 'reps'),
    (triple_under_hold_generator, 'TRIPLE_UNDER', 'hold'),
    (weighted_bob_and_weave_circle_rep_generator, 'WEIGHTED_BOB_AND_WEAVE_CIRCLE', 'reps'),
    (weighted_bob_and_weave_circle_hold_generator, 'WEIGHTED_BOB_AND_WEAVE_CIRCLE', 'hold'),
    (weighted_cardio_core_crawl_rep_generator, 'WEIGHTED_CARDIO_CORE_CRAWL', 'reps'),
    (weighted_cardio_core_crawl_hold_generator, 'WEIGHTED_CARDIO_CORE_CRAWL', 'hold'),
    (weighted_double_under_rep_generator, 'WEIGHTED_DOUBLE_UNDER', 'reps'),
    (weighted_double_under_hold_generator, 'WEIGHTED_DOUBLE_UNDER', 'hold'),
    (weighted_jump_rope_rep_generator, 'WEIGHTED_JUMP_ROPE', 'reps'),
    (weighted_jump_rope_hold_generator, 'WEIGHTED_JUMP_ROPE', 'hold'),
    (weighted_jump_rope_crossover_rep_generator, 'WEIGHTED_JUMP_ROPE_CROSSOVER', 'reps'),
    (weighted_jump_rope_crossover_hold_generator, 'WEIGHTED_JUMP_ROPE_CROSSOVER', 'hold'),
    (weighted_jump_rope_jog_rep_generator, 'WEIGHTED_JUMP_ROPE_JOG', 'reps'),
    (weighted_jump_rope_jog_hold_generator, 'WEIGHTED_JUMP_ROPE_JOG', 'hold'),
    (weighted_jumping_jacks_rep_generator, 'WEIGHTED_JUMPING_JACKS', 'reps'),
    (weighted_jumping_jacks_hold_generator, 'WEIGHTED_JUMPING_JACKS', 'hold'),
    (weighted_ski_moguls_rep_generator, 'WEIGHTED_SKI_MOGULS', 'reps'),
    (weighted_ski_moguls_hold_generator, 'WEIGHTED_SKI_MOGULS', 'hold'),
    (weighted_split_jacks_rep_generator, 'WEIGHTED_SPLIT_JACKS', 'reps'),
    (weighted_split_jacks_hold_generator, 'WEIGHTED_SPLIT_JACKS', 'hold'),
    (weighted_squat_jacks_rep_generator, 'WEIGHTED_SQUAT_JACKS', 'reps'),
    (weighted_squat_jacks_hold_generator, 'WEIGHTED_SQUAT_JACKS', 'hold'),
    (weighted_triple_under_rep_generator, 'WEIGHTED_TRIPLE_UNDER', 'reps'),
    (weighted_triple_under_hold_generator, 'WEIGHTED_TRIPLE_UNDER', 'hold'),
    ])
def test_exercise_generators(generator, exercise_name, execution):
    duration = "10reps" if execution == 'reps' else 'lap.button'
    description = exercise_name.replace('_', ' ').title() if execution == 'reps' else "10-count hold"
    result = generator(10)
    assert result['category'] == 'CARDIO'
    assert result['exerciseName'] == exercise_name
    assert result['duration'] == duration
    assert result['target'] == 'NO_TARGET'
    assert result['description'] == description