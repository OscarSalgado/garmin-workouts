from garminworkouts.config.generators.base import step_generator


def S0_step_generator(duration) -> dict:
    return step_generator(
        duration=duration,
        target='S0',
        secondary='H0',
        description='S0 pace zone')


def S1_step_generator(duration) -> dict:
    return step_generator(
        duration=duration,
        target='S1',
        secondary='H1',
        description='S1 pace zone')


def S1p_step_generator(duration) -> dict:
    return step_generator(
        duration=duration,
        target='S1p',
        secondary='H1p',
        description='S1+ pace zone')


def S2_step_generator(duration) -> dict:
    return step_generator(
        duration=duration,
        target='S2',
        secondary='H2',
        description='S2 pace zone')


def S3_step_generator(duration) -> dict:
    return step_generator(
        duration=duration,
        target='S3',
        secondary='H3',
        description='S3 pace zone')


def S3p_step_generator(duration) -> dict:
    return step_generator(
        duration=duration,
        target='S3p',
        description='S3+ pace zone')


def S4_step_generator(duration) -> dict:
    return step_generator(
        duration=duration,
        target='S4',
        description='S4 pace zone')


def S5_step_generator(duration) -> dict:
    return step_generator(
        duration=duration,
        target='S5',
        description='S5 pace zone')


def S6_step_generator(duration) -> dict:
    return step_generator(
        duration=duration,
        target='S6',
        description='S6 pace zone')


def S7_step_generator(duration) -> dict:
    return step_generator(
        duration=duration,
        target='S7',
        description='S7 pace zone')
