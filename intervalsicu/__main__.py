#!/usr/bin/env python3

import argparse
import logging
import os
import sys
from garminworkouts.models.settings import settings
import account
from intervalsicu.intervals.client import IntervalsClient


def command_athlete_import(args) -> None:  # pragma: no cover
    """
    Import athlete data from Intervals.icu to Garmin Connect.
    This function retrieves athlete data and updates it in Garmin Connect.
    """
    with _intervals_client() as connection:
        connection.update_athlete_data()


def command_trainingplan_import(args) -> None:
    workouts, notes, _, plan = settings(args)

    with _intervals_client() as connection:
        connection.update_workouts(workouts=workouts, plan=plan)


def command_trainingplan_update(args) -> None:
    workouts, notes, _, plan = settings(args)

    with _intervals_client() as connection:
        connection.update_training_plan(workouts=workouts, plan=plan)


def _intervals_client() -> IntervalsClient:
    """
    Creates and returns an IntervalsClient instance using the API key and athlete ID from the account module.
    Returns:
        IntervalsClient: An instance of IntervalsClient initialized with API key and athlete ID.
    Raises:
        AttributeError: If the account module does not define INTERVALS_API_KEY and INTERVALS_ATHLETE_ID.
    """
    try:
        api_key = account.intervals_api_key
        athlete_id = account.intervals_athlete_id
    except AttributeError:
        raise AttributeError("account module must define INTERVALS_API_KEY and INTERVALS_ATHLETE_ID")

    return IntervalsClient(
        api_key=api_key,
        athlete_id=athlete_id
    )


def main() -> None:  # pragma: no cover
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Manage Garmin Connect workout(s)'
    )
    parser.add_argument('--debug',
                        action='store_true',
                        help='Enables more detailed messages')

    subparsers: argparse._SubParsersAction[argparse.ArgumentParser] = parser.add_subparsers(title='Commands')

    parser_import: argparse.ArgumentParser = subparsers.add_parser(
        'trainingplan-import',
        description='Import workout(s) from file(s) into Garmin Connect ')
    parser_import.add_argument(
        'trainingplan',
        help='File(s) with workout(s) to import, '
        'wildcards are supported e.g: sample_workouts/*.yaml '
        'Additionally internal trainingplan IDs (defined in planning.yaml) may be used')
    parser_import.set_defaults(func=command_trainingplan_import)

    parser_import = subparsers.add_parser(
        'trainingplan-update',
        description='Import workout(s) from file(s) into Garmin Connect ')
    parser_import.add_argument(
        'trainingplan',
        help='File(s) with workout(s) to update plan, '
        'wildcards are supported e.g: sample_workouts/*.yaml '
        'Additionally internal trainingplan IDs (defined in planning.yaml) may be used')
    parser_import.set_defaults(func=command_trainingplan_update)

    parser_import = subparsers.add_parser('athlete-import', description='Update athlete data in IntervalsICU')
    parser_import.set_defaults(func=command_athlete_import)
    args: argparse.Namespace = parser.parse_args()

    logging_level: int = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=logging_level,
                        handlers=[
                            logging.FileHandler(debug_file),
                            logging.StreamHandler(sys.stdout)
                        ])

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_usage()


debug_file = './debug.log'

if __name__ == '__main__':  # pragma: no cover
    try:
        os.remove(debug_file)
    except FileNotFoundError:
        pass
    if os.path.exists(debug_file):
        os.remove(debug_file)
    main()
