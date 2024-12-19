import pytest

from garminworkouts.config.generators.strength.carry import (
    bar_holds_rep_generator,
    bar_holds_hold_generator,
    carry_rep_generator,
    carry_hold_generator,
    dumbbell_waiter_carry_rep_generator,
    dumbbell_waiter_carry_hold_generator,
    farmers_carry_rep_generator,
    farmers_carry_hold_generator,
    farmers_carry_on_toes_rep_generator,
    farmers_carry_on_toes_hold_generator,
    farmers_carry_walk_lunge_rep_generator,
    farmers_carry_walk_lunge_hold_generator,
    farmers_walk_rep_generator,
    farmers_walk_hold_generator,
    farmers_walk_on_toes_rep_generator,
    farmers_walk_on_toes_hold_generator,
    hex_dumbbell_hold_rep_generator,
    hex_dumbbell_hold_hold_generator,
    overhead_carry_rep_generator,
    overhead_carry_hold_generator,
    )


@pytest.mark.parametrize("generator, exercise_name, execution", [
    (bar_holds_rep_generator, 'BAR_HOLDS', 'reps'),
    (bar_holds_hold_generator, 'BAR_HOLDS', 'hold'),
    (carry_rep_generator, 'CARRY', 'reps'),
    (carry_hold_generator, 'CARRY', 'hold'),
    (dumbbell_waiter_carry_rep_generator, 'DUMBBELL_WAITER_CARRY', 'reps'),
    (dumbbell_waiter_carry_hold_generator, 'DUMBBELL_WAITER_CARRY', 'hold'),
    (farmers_carry_rep_generator, 'FARMERS_CARRY', 'reps'),
    (farmers_carry_hold_generator, 'FARMERS_CARRY', 'hold'),
    (farmers_carry_on_toes_rep_generator, 'FARMERS_CARRY_ON_TOES', 'reps'),
    (farmers_carry_on_toes_hold_generator, 'FARMERS_CARRY_ON_TOES', 'hold'),
    (farmers_carry_walk_lunge_rep_generator, 'FARMERS_CARRY_WALK_LUNGE', 'reps'),
    (farmers_carry_walk_lunge_hold_generator, 'FARMERS_CARRY_WALK_LUNGE', 'hold'),
    (farmers_walk_rep_generator, 'FARMERS_WALK', 'reps'),
    (farmers_walk_hold_generator, 'FARMERS_WALK', 'hold'),
    (farmers_walk_on_toes_rep_generator, 'FARMERS_WALK_ON_TOES', 'reps'),
    (farmers_walk_on_toes_hold_generator, 'FARMERS_WALK_ON_TOES', 'hold'),
    (hex_dumbbell_hold_rep_generator, 'HEX_DUMBBELL_HOLD', 'reps'),
    (hex_dumbbell_hold_hold_generator, 'HEX_DUMBBELL_HOLD', 'hold'),
    (overhead_carry_rep_generator, 'OVERHEAD_CARRY', 'reps'),
    (overhead_carry_hold_generator, 'OVERHEAD_CARRY', 'hold'),
    ])
def test_exercise_generators(generator, exercise_name, execution):
    duration = "10reps" if execution == 'reps' else 'lap.button'
    description = exercise_name.replace('_', ' ').title() if execution == 'reps' else "10-count hold"
    result = generator(10)
    assert result['category'] == 'CARRY'
    assert result['exerciseName'] == exercise_name
    assert result['duration'] == duration
    assert result['target'] == 'NO_TARGET'
    assert result['description'] == description
