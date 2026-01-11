import logging
import os
import shutil
from typing import Any, List, Optional
from pathlib import Path
import yaml

from garminworkouts.config import configreader


class WorkoutCreator:
    @staticmethod
    def _write_workout_file(path: Path, base: dict, include_steps: Optional[List[str]] = None) -> None:
        """Write a workout YAML file.

        If include_steps is provided it will write the base mapping (without steps)
        and then append a steps block where each item is an include tag like
        '!include X.yaml'. This preserves custom YAML tags used by the app.
        """
        if include_steps is None:
            with path.open("w", encoding="utf-8") as fh:
                yaml.safe_dump(base, fh, sort_keys=False)
        else:
            base_no_steps = base.copy()
            base_no_steps.pop("steps", None)
            with path.open("w", encoding="utf-8") as fh:
                yaml.safe_dump(base_no_steps, fh, sort_keys=False)
                fh.write("steps:\n")
                for item in include_steps:
                    fh.write(f"  - {item}\n")

    @staticmethod
    def planning_folder(args, defaultPlanning: dict | None = None):
        try:
            planning: Any = defaultPlanning or configreader.read_config(os.path.join('.', 'events', 'planning',
                                                                                     'planning.yaml'))
        except FileNotFoundError:
            logging.error('Planning config not found')
            planning = {}

        args.trainingplan = ''.join(args.trainingplan) if isinstance(args.trainingplan, tuple) else args.trainingplan

        if args.trainingplan in planning:
            workouts = planning[args.trainingplan].get('workouts', [])
        else:
            workouts = ''
        return workouts

    @staticmethod
    def MesoCreator(mesocycle_index) -> None:
        folder: str = os.path.join('.', 'trainingplans', 'Running', 'Self', 'base2026')
        # Create a mesocycle: select a week number from the 4-week cycle based on index
        meso_name = f"Meso{mesocycle_index}"
        meso_folder = os.path.join(folder, meso_name)
        weeks: List[int] = [4 * (int(mesocycle_index) - 1) + i for i in [1, 2, 3, 4]]
        strength_days = [1, 3]
        running_days = [1, 3, 6, 7]
        cycling_days = [2, 4, 5]
        swimming_days = [1, 2, 3]
        running_test_weeks: List[int] = [4 * (int(mesocycle_index) - 1) + i for i in [1, 2]]

        # Logic to create and store the mesocycle with the name meso_name
        print(f"Creating {meso_name}")
        WorkoutCreator.RunningWorkoutCreator(meso_folder, weeks, running_days)
        WorkoutCreator.RunningTestWorkoutCreator(meso_folder, running_test_weeks)
        WorkoutCreator.CyclingWorkoutCreator(meso_folder, weeks, cycling_days)
        WorkoutCreator.SwimWorkoutCreator(meso_folder, weeks, swimming_days)
        WorkoutCreator.StrengthWorkoutCreator(meso_folder, weeks, strength_days)

    @staticmethod
    def StrengthWorkoutCreator(meso_folder: str, weeks: List[int], strength_days: List[int]) -> None:
        meso_path = Path(meso_folder)
        meso_path.mkdir(parents=True, exist_ok=True)

        for week in weeks:
            for day in strength_days:
                name_short = f"R{week}_{day}"
                workout_data = WorkoutCreator.StrengthWorkout(name_short)

                workout_file_path = meso_path / f"{name_short}_Strength.yaml"
                WorkoutCreator._write_workout_file(workout_file_path, workout_data)

    @staticmethod
    def SwimWorkoutCreator(meso_folder: str, weeks: List[int], swim_days: List[int]) -> None:
        meso_path = Path(meso_folder)
        meso_path.mkdir(parents=True, exist_ok=True)

        for week in weeks:
            for day in swim_days:
                name_short = f"R{week}_{day}"
                workout_data = WorkoutCreator.SwimWorkout(name_short)

                workout_file_path = meso_path / f"{name_short}_Swim.yaml"
                WorkoutCreator._write_workout_file(workout_file_path, workout_data)

    @staticmethod
    def SwimWorkout(name_short):
        workout_data = {
                    "name": str(name_short),
                    "description": "Swim",
                    "sport": "swimming",
                    "steps": [
                        {
                            "description": "Swim",
                            "duration": "0:30:00",
                            "target": {"type": "no.target"},
                            "type": "interval",
                        }
                    ],
                }

        return workout_data

    @staticmethod
    def StrengthWorkout(name_short):
        workout_data = {
            "name": str(name_short),
            "description": "Strength",
            "sport": "strength_training",
            "steps": [
                {
                    "description": "Strength",
                    "duration": "0:30:00",
                    "target": {"type": "no.target"},
                    "type": "interval",
                }
            ],
        }

        return workout_data

    @staticmethod
    def CyclingWorkoutCreator(meso_folder: str, weeks: List[int], cycling_days: List[int]) -> None:
        meso_path = Path(meso_folder)
        meso_path.mkdir(parents=True, exist_ok=True)

        for week in weeks:
            for day in cycling_days:
                duration = 120 if day in (6, 7) else 60
                name_short = f"R{week}_{day}"

                workout_data, include_steps = WorkoutCreator.P0_workout(name_short, "Bike", duration)
                workout_file_path = meso_path / f"{name_short}_Bike.yaml"
                WorkoutCreator._write_workout_file(workout_file_path, workout_data, include_steps)

    @staticmethod
    def RunningWorkoutCreator(meso_folder: str, weeks: List[int], running_days: List[int]) -> None:
        meso_path = Path(meso_folder)
        meso_path.mkdir(parents=True, exist_ok=True)

        for week in weeks:
            for day in running_days:
                duration = 90 if day == 6 else 60
                name_short = f"R{week}_{day}"

                workout_data, include_steps = WorkoutCreator.H0_workout(name_short, "Running", duration)
                workout_file_path = meso_path / f"{name_short}_Run.yaml"
                WorkoutCreator._write_workout_file(workout_file_path, workout_data, include_steps)

                # Warmup
                warmup_data, warmup_include = WorkoutCreator.H0_workout(name_short, "Running warmup", 30)
                warmup_file_path = meso_path / f"{name_short}_RunWarmup.yaml"
                WorkoutCreator._write_workout_file(warmup_file_path, warmup_data, warmup_include)

    @staticmethod
    def H0_workout(name_short, description="Running", duration=30) -> tuple[dict, List[str]]:
        workout_data = {
                    "name": str(name_short),
                    "description": description,
                    "sport": "running",
                }

        include_steps = [f"!include H0_{duration}min.yaml"]
        return workout_data, include_steps

    @staticmethod
    def P0_workout(name_short, description="Bike", duration=30) -> tuple[dict, List[str]]:
        workout_data = {
            "name": str(name_short),
            "description": description,
            "sport": "cycling",
        }

        include_steps = [f"!include P0_{duration}min.yaml"]
        return workout_data, include_steps

    @staticmethod
    def copy_and_rename_file(src_path, dest_dir, new_filename):
        """
        Copies a file from src_path to dest_dir and renames it to new_filename.
        Creates the destination directory if it doesn't exist.
        """
        try:
            # Validate source file
            if not os.path.isfile(src_path):
                raise FileNotFoundError(f"Source file not found: {src_path}")

            # Ensure destination directory exists
            os.makedirs(dest_dir, exist_ok=True)

            # Build full destination path
            dest_path = os.path.join(dest_dir, new_filename)

            # Copy and rename
            shutil.copy2(src_path, dest_path)  # copy2 preserves metadata
            print(f"File copied and renamed to: {dest_path}")

        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def RunningTestWorkoutCreator(meso_folder: str, weeks: List[int]) -> None:
        day = 6
        meso_path = Path(meso_folder)
        meso_path.mkdir(parents=True, exist_ok=True)

        distance = [1200, 3200]
        for week, duration in zip(weeks, distance):
            name_short = f"R{week}_{day}_RunTest"
            workout_data = {
                "name": str(name_short),
                "description": f"{duration}m Test",
                "sport": "running",
            }
            include_steps = [
                "!include R0_10min.yaml",
                "!include R1_5min.yaml",
                "!include R1p_5min.yaml",
                "!include R2_5min.yaml",
                f"!include R3p_{duration}m.yaml",
                "!include R0_25min.yaml",
            ]
            workout_file_path = meso_path / f"{name_short}.yaml"
            WorkoutCreator._write_workout_file(workout_file_path, workout_data, include_steps)
