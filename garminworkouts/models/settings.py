import glob
import logging
import os
from datetime import date
from typing import Any

import account
from garminworkouts.config import configreader
from garminworkouts.models.event import Event
from garminworkouts.models.note import Note
from garminworkouts.models.workout import Workout

logger = logging.getLogger(__name__)


def settings(args, defaultPlanning=None) -> tuple[list[Workout], list[Note], list[Event], str]:
    workout_files, race, plan = planning_workout_files(args, defaultPlanning)

    try:
        target: dict[Any, Any] = configreader.read_config(r'target.yaml')
        combined: list[Workout | Note | Event] = []
        athlete_config = account.get_athlete_config()
        workout_configs: list[dict[Any, Any]] = [configreader.read_config(
            workout_file) for workout_file in workout_files]
        for workout_config in workout_configs:
            if 'goal' in workout_config:
                combined.append(Event(workout_config))
            if 'steps' in workout_config:
                combined.append(Workout(
                    workout_config,
                    target,
                    athlete_config['vV02'],
                    athlete_config['fmin'],
                    athlete_config['rfmax'],
                    athlete_config['rflt'],
                    athlete_config['rFTP'],
                    athlete_config['cfmax'],
                    athlete_config['cflt'],
                    athlete_config['cFTP'],
                    athlete_config['sfmax'],
                    athlete_config['sflt'],
                    plan,
                    race))
            if 'content' in workout_config:
                combined.append(Note(workout_config))

        notes: list[Note] = [w for w in combined if isinstance(w, Note)]
        workouts: list[Workout] = [w for w in combined if isinstance(w, Workout)]
        events: list[Event] = [w for w in combined if isinstance(w, Event)]
        return workouts, notes, events, plan

    except FileNotFoundError as e:
        logger.error("Error reading config file: %s", e)
        return [], [], [], ''


def planning_workout_files(args, defaultPlanning: dict | None = None):
    try:
        planning: Any = defaultPlanning or configreader.read_config(os.path.join('.', 'events', 'planning',
                                                                                 'planning.yaml'))
    except FileNotFoundError:
        logger.error('Planning config not found')
        planning = {}

    args.trainingplan = ''.join(args.trainingplan) if isinstance(args.trainingplan, tuple) else args.trainingplan

    if args.trainingplan in planning:
        workouts = planning[args.trainingplan].get('workouts', [])
        workout_files = [file for pattern in (workouts if isinstance(workouts, list) else [workouts])
                         for file in glob.glob(pattern)]
        race: date = date.today()
        plan: str | Any = args.trainingplan

        race_info = planning[args.trainingplan]
        race = date(race_info.get('year', date.today().year),
                    race_info.get('month', date.today().month),
                    race_info.get('day', date.today().day))
    elif '.yaml' in args.trainingplan:
        workout_files = glob.glob(args.trainingplan)
        plan = ''
        race = date.today()
    else:
        logger.error('%s not found in planning, please check "planning.yaml"', args.trainingplan)
        workout_files = []
        plan = ''
        race = date.today()

    return workout_files, race, plan
