from datetime import date
from typing import List, Tuple, Union, Any
import glob
import os
from garminworkouts.config import configreader
from garminworkouts.models.event import Event
from garminworkouts.models.workout import Workout
from garminworkouts.models.note import Note
import account
import logging


def settings(args, defaultPlanning=None) -> Tuple[List[Workout], List[Note], list[Event], str]:
    workout_files, race, plan = planning_workout_files(args, defaultPlanning)

    try:
        target: dict[Any, Any] = configreader.read_config(r'target.yaml')
        combined: List[Union[Workout, Note, Event]] = []
        workout_configs: list[dict[Any, Any]] = [configreader.read_config(
            workout_file) for workout_file in workout_files]
        for workout_config in workout_configs:
            if 'goal' in workout_config:
                combined.append(Event(workout_config))
            if 'steps' in workout_config:
                combined.append(Workout(
                    workout_config,
                    target,
                    account.vV02,
                    account.fmin,
                    account.rfmax,
                    account.rflt,
                    account.rFTP,
                    account.cfmax,
                    account.cflt,
                    account.cFTP,
                    account.sfmax,
                    account.sflt,
                    plan,
                    race))
            if 'content' in workout_config:
                combined.append(Note(workout_config))

        notes: List[Note] = [w for w in combined if isinstance(w, Note)]
        workouts: List[Workout] = [w for w in combined if isinstance(w, Workout)]
        events: List[Event] = [w for w in combined if isinstance(w, Event)]
        return workouts, notes, events, plan

    except FileNotFoundError as e:
        logging.error(f"Error reading config file: {e}")
        return [], [], [], ''


def planning_workout_files(args, defaultPlanning: dict | None = None):
    try:
        planning: Any = defaultPlanning or configreader.read_config(os.path.join('.', 'events', 'planning',
                                                                                 'planning.yaml'))
    except FileNotFoundError:
        logging.error('Planning config not found')
        planning = {}

    args.trainingplan = ''.join(args.trainingplan) if isinstance(args.trainingplan, tuple) else args.trainingplan

    if args.trainingplan in planning:
        workouts = planning[args.trainingplan].get('workouts', [])
        workout_files = [file for pattern in (workouts if isinstance(workouts, list) else [workouts])
                         for file in glob.glob(pattern)]
        race: date = date.today()
        plan: Union[str, Any] = args.trainingplan

        race_info = planning[args.trainingplan]
        race = date(race_info.get('year', date.today().year),
                    race_info.get('month', date.today().month),
                    race_info.get('day', date.today().day))
    elif '.yaml' in args.trainingplan:
        workout_files = glob.glob(args.trainingplan)
        plan = ''
        race = date.today()
    else:
        logging.error(f'{args.trainingplan} not found in planning, please check "planning.yaml"')
        workout_files = []
        plan = ''
        race = date.today()

    return workout_files, race, plan
