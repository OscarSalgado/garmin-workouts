from garminworkouts.config.generators.base import step_generator


def Pseries_generator(duration, objective) -> list[dict]:
    return [
        step_generator(
            type='recovery' if int(objective[0][1]) < int(objective[1][1]) else 'interval',
            duration=duration[0],
            target=objective[0],
            description=f'{objective[0]} power zone'),
        step_generator(
            type='interval' if int(objective[0][1]) < int(objective[1][1]) else 'recovery',
            duration=duration[1],
            target=objective[1],
            description=f'{objective[1]} power zone')
    ]
