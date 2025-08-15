from garminworkouts.config.generators.base import step_generator


def P0_step_generator(duration) -> dict:
    return step_generator(
        duration=duration,
        target='P0',
        secondary='H0',
        description='P0 power zone')


def P1_step_generator(duration) -> dict:
    return step_generator(
        duration=duration,
        target='P1',
        secondary='H1',
        description='P1 power zone')


def P1p_step_generator(duration) -> dict:
    return step_generator(
        duration=duration,
        target='P1p',
        secondary='H1p',
        description='P1+ power zone')


def P2_step_generator(duration) -> dict:
    return step_generator(
        duration=duration,
        target='P2',
        secondary='H2',
        description='P2 power zone')


def P3_step_generator(duration) -> dict:
    return step_generator(
        duration=duration,
        target='P3',
        secondary='H3',
        description='P3 power zone')


def P3p_step_generator(duration) -> dict:
    return step_generator(
        duration=duration,
        target='P3p',
        description='P3+ power zone')


def P4_step_generator(duration) -> dict:
    return step_generator(
        duration=duration,
        target='P4',
        description='P4 power zone')


def P5_step_generator(duration) -> dict:
    return step_generator(
        duration=duration,
        target='P5',
        description='P5 power zone')


def P6_step_generator(duration) -> dict:
    return step_generator(
        duration=duration,
        target='P6',
        description='P6 power zone')


def P7_step_generator(duration) -> dict:
    return step_generator(
        duration=duration,
        target='P7',
        description='P7 power zone')


def Hcyclingoutdoor_step_generator(duration) -> dict:
    return step_generator(
        duration=duration,
        target='Hcyclingoutdoor',
        secondary='BikeCadence',
        description='Cycling outdoor heart rate zone')


def H0c_step_generator(duration) -> dict:
    return step_generator(
        duration=duration,
        target='H0c',
        description='R0 heart rate zone')
