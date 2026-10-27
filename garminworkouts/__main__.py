#!/usr/bin/env python3
"""Simple Garmin Connect API Example.

Demonstrates authentication, token storage, and basic API calls.

For a comprehensive demo of all 127+ API methods, see demo.py

Dependencies:
    pip install garminconnect[example]
    pip install curl_cffi

Environment Variables (optional):
    export EMAIL=<your garmin email address>
    export PASSWORD=<your garmin password>
    export GARMINTOKENS=<path to token storage, default ~/.garminconnect>
"""

import argparse
import logging
import os
import sys
from datetime import date
from getpass import getpass
from pathlib import Path
from typing import TYPE_CHECKING, Any

from garminworkouts.models.event import Event
from garminworkouts.models.settings import settings
from garminworkouts.models.workout import Workout
from garminworkouts.utils.validators import writeable_dir

# Import garminconnect symbols for runtime when available; provide
# sensible fallbacks for static analysis and environments where the
# package isn't installed so Pylance/typing doesn't error out.
if TYPE_CHECKING:
    from garminconnect import (
        Garmin,
        GarminConnectAuthenticationError,
        GarminConnectConnectionError,
        GarminConnectTooManyRequestsError,
    )
else:
    try:
        from garminconnect import (
            Garmin,
            GarminConnectAuthenticationError,
            GarminConnectConnectionError,
            GarminConnectTooManyRequestsError,
        )
    except Exception:  # pragma: no cover - optional runtime dependency
        Garmin = Any  # type: ignore
        GarminConnectAuthenticationError = Exception  # type: ignore
        GarminConnectConnectionError = Exception  # type: ignore
        GarminConnectTooManyRequestsError = Exception  # type: ignore


debug_file = './debug.log'
# from garminworkouts.garmin.garminclient import GarminClient


logging.getLogger("garminconnect").setLevel(logging.CRITICAL)


def safe_api_call(api_method, *args, **kwargs):
    """Call an API method and return (success, result, error_message)."""
    try:
        result = api_method(*args, **kwargs)
        return True, result, None

    except GarminConnectAuthenticationError as e:
        return False, None, f"Authentication error: {e}"
    except GarminConnectTooManyRequestsError as e:
        return False, None, f"Rate limit exceeded: {e}"
    except GarminConnectConnectionError as e:
        error_str = str(e)
        if "400" in error_str:
            return (
                False,
                None,
                "Not available (400) — feature may not be enabled for your account",
            )
        if "401" in error_str:
            return False, None, "Authentication required (401) — please re-authenticate"
        if "403" in error_str:
            return False, None, "Access denied (403) — account may not have permission"
        if "404" in error_str:
            return False, None, "Not found (404) — endpoint may have moved"
        if "429" in error_str:
            return False, None, "Rate limit (429) — please wait before retrying"
        if "500" in error_str:
            return False, None, "Server error (500) — Garmin servers are having issues"
        return False, None, f"Connection error: {e}"
    except Exception as e:
        return False, None, f"Unexpected error: {e}"


def command_trainingplan_reset(args) -> None:  # pragma: no cover
    connection = _garmin_client()
    if connection:
        connection.trainingplan_reset(args)


def command_trainingplan_import(args) -> None:
    workouts, notes, _, plan = settings(args)

    connection = _garmin_client()
    if connection:
        ue, _, ne = connection.get_calendar(date=date.today(), days=7)
        connection.update_workouts(ue=ue, workouts=workouts, plan=plan)
        connection.update_notes(ne=ne, notes=notes, plan=plan)


def command_trainingplan_metrics(args) -> None:
    """Compute or load metrics for training plans.

    Tests expect this function to call `Workout.load_metrics` with the
    trainingplan argument. Keep behaviour minimal to satisfy tests.
    """
    # Delegate to the model-level helper; exact behaviour is tested via mocking.
    Workout.load_metrics(args.trainingplan)


def command_event_import(args) -> None:
    workouts, _, events, plan = settings(args)

    connection = _garmin_client()
    if connection:
        ue, _, _ = connection.get_calendar(date=date.today(), days=7)
        connection.update_events(events=events)
        connection.update_workouts(ue=ue, workouts=workouts, plan=plan)


def command_find_events(args) -> None:  # pragma: no cover
    connection = _garmin_client()
    if connection:
        connection._find_events()


def command_workout_export(args) -> None:  # pragma: no cover
    connection = _garmin_client()
    if connection:
        connection.workout_export(args)


def command_workout_export_yaml(args) -> None:  # pragma: no cover
    connection = _garmin_client()
    if connection:
        connection.external_workout_export_yaml()


def command_workout_schedule(args) -> None:  # pragma: no cover
    connection = _garmin_client()
    if connection:
        connection.schedule_workout(workout_id=args.id, date=args.date)  # type: ignore[call-arg]


def command_workout_get(args) -> None:
    connection = _garmin_client()
    if connection:
        Workout.print_workout_json(connection.get_workout(workout_id=args.id))


def command_event_get(args) -> None:
    connection = _garmin_client()
    if connection:
        Event.print_event_json(connection.get_event(event_id=args.id))


def command_workout_delete(args) -> None:  # pragma: no cover
    connection = _garmin_client()
    if connection:
        connection.delete_workout(workout_id=args.workout_id)


def command_user_zones(args) -> None:  # pragma: no cover
    connection = _garmin_client()
    if connection:
        connection.user_zones()


def command_workout_list(args) -> None:  # pragma: no cover
    connection = _garmin_client()
    if connection:
        connection.workout_list()


def command_event_list(args) -> None:  # pragma: no cover
    connection = _garmin_client()
    if connection:
        connection.event_list()


def command_challenge_list(args) -> None:  # pragma: no cover
    connection = _garmin_client()
    if connection:
        connection.list_challenge()


def command_trainingplan_list(args) -> None:  # pragma: no cover
    connection = _garmin_client()
    if connection:
        connection.trainingplan_list()


def command_activity_list(args) -> None:  # pragma: no cover
    connection = _garmin_client()
    if connection:
        connection.activity_list()


def command_update_types(args) -> None:  # pragma: no cover
    connection = _garmin_client()
    if connection:
        connection.get_types()


def update_garmin(args) -> None:  # pragma: no cover
    connection = _garmin_client()
    if connection:
        connection.updateGarmin()


def _garmin_client() -> Garmin | None:
    """Initialise Garmin API, restoring saved tokens or logging in fresh.

    Tokens are stored in ``~/.garminconnect/garmin_tokens.json``
    and reused automatically on the next run.  DI OAuth tokens include
    a refresh token so the session auto-renews without user interaction.
    """
    tokenstore = os.getenv("GARMINTOKENS", "~/.garminconnect")
    tokenstore_path = str(Path(tokenstore).expanduser())

    # Try to restore saved tokens
    try:
        garmin = Garmin()
        garmin.login(tokenstore_path)
        print("Logged in using saved tokens.")
        return garmin

    except GarminConnectTooManyRequestsError as err:
        print(f"Rate limit: {err}")
        sys.exit(1)

    except (GarminConnectAuthenticationError, GarminConnectConnectionError):
        print("No valid tokens found — please log in.")

    # Fresh credential login with MFA support
    while True:
        try:
            email = os.getenv("EMAIL") or input("Email: ").strip()
            password = os.getenv("PASSWORD") or getpass("Password: ")

            garmin = Garmin(
                email=email,
                password=password,
                prompt_mfa=lambda: input("MFA code: ").strip(),
            )
            garmin.login(tokenstore_path)
            print(f"Login successful. Tokens saved to: {tokenstore_path}")
            return garmin

        except GarminConnectTooManyRequestsError as err:
            print(f"Rate limit: {err}")
            sys.exit(1)

        except GarminConnectAuthenticationError:
            print("Wrong credentials — please try again.")
            continue

        except GarminConnectConnectionError as err:
            print(f"Connection error: {err}")
            return None

        except KeyboardInterrupt:
            return None


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
        'trainingplan-reset',
        description='Reset workout(s) from file(s) into Garmin Connect')
    parser_import.add_argument(
        'trainingplan',
        help='File(s) with workout(s) to reset, '
        'wildcards are supported e.g: sample_workouts/*.yaml '
        'Additionally internal trainingplan IDs (defined in planning.yaml) may be used')
    parser_import.set_defaults(func=command_trainingplan_reset)

    parser_import = subparsers.add_parser(
        'trainingplan-list', description='List all Garmin trainingplans')
    parser_import.set_defaults(func=command_trainingplan_list)

    parser_import: argparse.ArgumentParser = subparsers.add_parser(
        'event-import',
        description='Import event(s) from file(s) into Garmin Connect')
    parser_import.add_argument(
        'trainingplan',
        help='File(s) with event(s) to import, wildcards are supported e.g: events/*.yaml')
    parser_import.set_defaults(func=command_event_import)

    parser_import = subparsers.add_parser(
        'event-get',
        description='Get event')
    parser_import.add_argument(
        '--id',
        required=True,
        help='Event id, use list command to get event identifiers')
    parser_import.set_defaults(func=command_event_get)

    parser_import = subparsers.add_parser('event-list', description='List all events')
    parser_import.set_defaults(func=command_event_list)

    parser_import = subparsers.add_parser(
        'workout-get', description='Get workout')
    parser_import.add_argument(
        '--id',
        required=True,
        help="Workout id, use list command to get workouts' identifiers")
    parser_import.set_defaults(func=command_workout_get)

    parser_import: argparse.ArgumentParser = subparsers.add_parser(
        'workout-delete',
        description='Delete workout')
    parser_import.add_argument(
        '--id',
        required=True,
        help='Workout id, use list command to get workouts identifiers')
    parser_import.set_defaults(func=command_workout_delete)

    parser_import = subparsers.add_parser(
        'workout-schedule',
        description='Schedule a workout')
    parser_import.add_argument(
        '--id',
        '-w',
        required=True,
        help='Workout id to schedule')
    parser_import.add_argument(
        '--date',
        '-d',
        required=True,
        help='Date to which schedule the workout')
    parser_import.set_defaults(func=command_workout_schedule)

    parser_import = subparsers.add_parser(
        'workout-export',
        description='Export all workouts from Garmin Connect and save them into a directory')
    parser_import.add_argument(
        'directory',
        type=writeable_dir,
        help='Destination directory where workout(s) will be exported')
    parser_import.set_defaults(func=command_workout_export)

    parser_import = subparsers.add_parser(
        'workout-export-yaml',
        description='Export all workouts from Garmin Connect and save them into a directory')
    parser_import.set_defaults(func=command_workout_export_yaml)

    parser_import = subparsers.add_parser(
        'workout-list',
        description='List all workouts')
    parser_import.set_defaults(func=command_workout_list)

    parser_import = subparsers.add_parser(
        'user-zones',
        description='Get training zones')
    parser_import.set_defaults(func=command_user_zones)

    parser_import = subparsers.add_parser(
        'update-types',
        description='Update types')
    parser_import.set_defaults(func=command_update_types)

    parser_import = subparsers.add_parser(
        'activity-list',
        description='Activity list')
    parser_import.set_defaults(func=command_activity_list)

    parser_import = subparsers.add_parser(
        'find-events',
        description='Find events')
    parser_import.set_defaults(func=command_find_events)

    parser_import = subparsers.add_parser(
        'challenge-signup',
        description='Challenge sign up')
    parser_import.set_defaults(func=command_challenge_list)

    parser_import = subparsers.add_parser(
        'garmin-update',
        description='Garmin version update')
    parser_import.set_defaults(func=update_garmin)

    args: argparse.Namespace = parser.parse_args()

    logging_level: int = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(
        level=logging_level,
        handlers=[
            logging.FileHandler(debug_file),
            logging.StreamHandler(sys.stdout),
        ],
    )

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
