import unittest
from datetime import date
from unittest.mock import patch
import account
import logging
import os
from garminworkouts.models.fields import _STEPS
from garminworkouts.models.workout import Workout
from garminworkouts.models.pace import Pace
from garminworkouts.models.power import Power
from garminworkouts.config import configreader


def get_athlete_values():
    """Get athlete configuration values for tests."""
    cfg = account.get_athlete_config()
    return {
        'fmin': cfg['fmin'],
        'rfmax': cfg['rfmax'],
        'rflt': cfg['rflt'],
        'sfmax': cfg['sfmax'],
        'sflt': cfg['sflt'],
        'cfmax': cfg['cfmax'],
        'cflt': cfg['cflt'],
        'vV02': cfg['vV02'],
        'rFTP': cfg['rFTP'],
        'cFTP': cfg['cFTP'],
    }


class TestWorkout(unittest.TestCase):
    def test_null_workout(self) -> None:
        a = get_athlete_values()
        with self.assertRaises(ValueError):
            Workout(
                config={'name': 'name'},
                target=[],
                vVO2=Pace('3:30'),
                fmin=a['fmin'],
                rfmax=a['rfmax'],
                rflt=a['rflt'],
                sfmax=a['sfmax'],
                sflt=a['sflt'],
                cfmax=a['cfmax'],
                cflt=a['cflt'],
                rFTP=Power('200'),
                cFTP=Power('200'),
                plan='',
                race=date.today()
            ).create_workout()

    def test_get_workout_name(self) -> None:
        a = get_athlete_values()
        # Create a Workout instance with a specific configuration
        workout_file: str = os.path.join('.', 'workouts', 'cardio_training', 'ADVANCED', 'BBtO4iZ.yaml')
        config: dict = configreader.read_config(workout_file)
        workout = Workout(
            config=config,
            target=[],
            vVO2=Pace('3:30'),
            fmin=a['fmin'],
            rfmax=a['rfmax'],
            rflt=a['rflt'],
            sfmax=a['sfmax'],
            sflt=a['sflt'],
            cfmax=a['cfmax'],
            cflt=a['cflt'],
            rFTP=Power('200'),
            cFTP=Power('200'),
            plan='',
            race=date.today()
        )

        # Call the get_workout_name method
        workout_name: str = workout.get_workout_name()

        # Assert that the returned workout name is correct
        self.assertEqual(workout_name, "Tabata Alternating Lunges, Crunches, Burpees & Planks")

    def test_get_workout_name_short(self) -> None:
        a = get_athlete_values()
        # Create a Workout instance with a specific configuration
        workout_file: str = os.path.join('.', 'workouts', 'cardio_training', 'ADVANCED', 'BBtO4iZ.yaml')
        config: dict = configreader.read_config(workout_file)
        config['name'] = '0_1'
        config['description'] = ''
        workout = Workout(
            config=config,
            target=[],
            vVO2=Pace('3:30'),
            fmin=a['fmin'],
            rfmax=a['rfmax'],
            rflt=a['rflt'],
            sfmax=a['sfmax'],
            sflt=a['sflt'],
            cfmax=a['cfmax'],
            cflt=a['cflt'],
            rFTP=Power('200'),
            cFTP=Power('200'),
            plan='',
            race=date.today()
        )

        # Call the get_workout_name method
        workout_name: str = workout.get_workout_name()
        self.assertEqual(workout_name, '0_1')

    def test_get_workout_name_med(self) -> None:
        a = get_athlete_values()
        # Create a Workout instance with a specific configuration
        workout_file: str = os.path.join('.', 'workouts', 'cardio_training', 'ADVANCED', 'BBtO4iZ.yaml')
        config: dict = configreader.read_config(workout_file)
        config['name'] = '0_1'
        config['description'] = 'Description'
        workout = Workout(
            config=config,
            target=[],
            vVO2=Pace('3:30'),
            fmin=a['fmin'],
            rfmax=a['rfmax'],
            rflt=a['rflt'],
            sfmax=a['sfmax'],
            sflt=a['sflt'],
            cfmax=a['cfmax'],
            cflt=a['cflt'],
            rFTP=Power('200'),
            cFTP=Power('200'),
            plan='plan',
            race=date.today()
        )

        # Call the get_workout_name method
        workout_name: str = workout.get_workout_name()
        self.assertEqual(workout_name, '0_1-Description')

    def test_get_workout_name_long(self) -> None:
        a = get_athlete_values()
        # Create a Workout instance with a specific configuration
        workout_file: str = os.path.join('.', 'workouts', 'cardio_training', 'ADVANCED', 'BBtO4iZ.yaml')
        config: dict = configreader.read_config(workout_file)
        config['name'] = '0_1'
        config['description'] = 'Long description for a long workout name'
        workout = Workout(
            config=config,
            target=[],
            vVO2=Pace('3:30'),
            fmin=a['fmin'],
            rfmax=a['rfmax'],
            rflt=a['rflt'],
            sfmax=a['sfmax'],
            sflt=a['sflt'],
            cfmax=a['cfmax'],
            cflt=a['cflt'],
            rFTP=Power('200'),
            cFTP=Power('200'),
            plan='',
            race=date.today()
        )

        # Call the get_workout_name method
        workout_name: str = workout.get_workout_name()
        self.assertEqual(workout_name, '0_1-Long')

    def test_get_workout_date(self) -> None:
        a = get_athlete_values()
        # Create a Workout instance with a specific configuration
        workout = Workout(
            config={},
            target=[],
            vVO2=Pace('5:00'),
            rfmax=200,
            rflt=185,
            sfmax=200,
            sflt=185,
            cfmax=200,
            cflt=185,
            rFTP=Power('400w'),
            cFTP=Power('200w'),
            plan='',
            race=date.today()
        )

        # Call the get_workout_date method
        workout_date, week, day = workout.get_workout_date()

        # Assert that the returned workout date, fmin, and fmax are correct
        self.assertEqual(workout_date, date.today())
        self.assertEqual(week, 0)
        self.assertEqual(day, 0)

    def test_print_workout_summary(self) -> None:
        a = get_athlete_values()
        workout: dict = {
            'workoutId': '123',
            'workoutName': 'Test Workout',
            'description': 'This is a test workout'
        }

        expected_output = '123 Test Workout         This is a test workout'

        with patch('builtins.print') as mock_print:
            Workout.print_workout_summary(workout)
            mock_print.assert_called_once_with(expected_output)

    def test_extract_workout_author(self) -> None:
        a = get_athlete_values()
        workout: dict = {
            'author': {
                'name': 'John Doe',
                'email': 'johndoe@example.com'
            }
        }

        expected_author: dict = {
            'name': 'John Doe',
            'email': 'johndoe@example.com'
        }

        author: dict = Workout.extract_workout_author(workout)

        self.assertEqual(author, expected_author)

    def test_extract_workout_author_no_author(self) -> None:
        a = get_athlete_values()
        workout: dict = {}

        author: dict = Workout.extract_workout_author(workout)

        self.assertIsNone(author)

    def test_extract_workout_author_missing_name(self) -> None:
        a = get_athlete_values()
        workout: dict = {
            'author': {
                'email': 'johndoe@example.com'
            }
        }

        expected_author: dict = {
            'email': 'johndoe@example.com'
        }

        author: dict = Workout.extract_workout_author(workout)

        self.assertEqual(author, expected_author)

    def test_extract_workout_author_missing_email(self) -> None:
        a = get_athlete_values()
        workout: dict = {
            'author': {
                'name': 'John Doe'
            }
        }

        expected_author: dict = {
            'name': 'John Doe'
        }

        author: dict = Workout.extract_workout_author(workout)

        self.assertEqual(author, expected_author)

    def test_create_workout(self) -> None:
        a = get_athlete_values()
        workout_file: str = os.path.join('.', 'workouts', 'cardio_training', 'ADVANCED', 'BBtO4iZ.yaml')
        config: dict = configreader.read_config(workout_file)
        config['description'] = ''
        workout = Workout(
            config=config,
            target=[],
            vVO2=Pace('3:30'),
            fmin=a['fmin'],
            rfmax=a['rfmax'],
            rflt=a['rflt'],
            sfmax=a['sfmax'],
            sflt=a['sflt'],
            cfmax=a['cfmax'],
            cflt=a['cflt'],
            rFTP=Power('200'),
            cFTP=Power('200'),
            plan='',
            race=date.today()
        )

        workout_id = '123'
        workout_owner_id = '456'
        workout_author: dict = {
            'name': 'John Doe',
            'email': 'johndoe@example.com'
        }

        expected_workout: dict = {
            'workoutId': '123',
            'ownerId': '456',
            'workoutName': 'Tabata Alternating Lunges, Crunches, Burpees & Planks',
            'description': '. Plan: . ',
            'sportType': {'sportTypeId': 6, 'sportTypeKey': 'cardio_training'},
            'subSportType': None,
            'author': {'name': 'John Doe', 'email': 'johndoe@example.com'},
            'estimatedDurationInSecs': None,
            'estimatedDistanceInMeters': None,
            'avgTrainingSpeed': None,
            'workoutSegments': [
                {
                    'segmentOrder': 1,
                    'sportType': {'sportTypeId': 6, 'sportTypeKey': 'cardio_training'},
                    'workoutSteps': workout._steps(workout.config.get(_STEPS))
                }
            ],
        }

        created_workout: dict = workout.create_workout(workout_id, workout_owner_id, workout_author)

        self.assertEqual(created_workout, expected_workout)

    def test_print_workout_json(self) -> None:
        a = get_athlete_values()
        workout = {
            'workoutId': '123',
            'workoutName': 'Test Workout',
            'description': 'This is a test workout'
        }

        expected_output = '{"workoutId": "123", "workoutName": "Test Workout", "description": "This is a test workout"}'

        with patch('builtins.print') as mock_print:
            Workout.print_workout_json(workout)
            mock_print.assert_called_once_with(expected_output)

    def test_extract_workout_owner_id(self) -> None:
        a = get_athlete_values()
        workout: dict = {
            'ownerId': '12345'
        }

        owner_id: str = Workout.extract_workout_owner_id(workout)

        self.assertEqual(owner_id, '12345')

    def test_running_workout_with_plan(self) -> None:
        a = get_athlete_values()
        workout_file: str = os.path.join('.', 'trainingplans', 'Running', 'Napier', 'Half', 'Advanced', 'Meso1',
                                         '21_1.yaml')
        config: dict = configreader.read_config(workout_file)
        target: dict = configreader.read_config(r'target.yaml')
        workout = Workout(
            config=config,
            target=target,
            vVO2=Pace('3:30'),
            fmin=a['fmin'],
            rfmax=a['rfmax'],
            rflt=a['rflt'],
            sfmax=a['sfmax'],
            sflt=a['sflt'],
            cfmax=a['cfmax'],
            cflt=a['cflt'],
            rFTP=a['rFTP'],
            cFTP=a['cFTP'],
            plan='5K Training Plan',
            race=date.today()
        )
        # Generate expected description dynamically based on actual athlete values
        description: str | None = workout._generate_description()
        # Verify description contains expected elements
        assert description is not None
        assert 'Plan: 5K Training Plan' in description
        assert 'Estimated Duration' in description

    def test_running_workout_without_plan(self) -> None:
        a = get_athlete_values()
        workout_file: str = os.path.join('.', 'trainingplans', 'Running', 'Napier', 'Half', 'Advanced', 'Meso1',
                                         '21_1.yaml')
        config: dict = configreader.read_config(workout_file)
        target: dict = configreader.read_config(r'target.yaml')
        workout = Workout(
            config=config,
            target=target,
            vVO2=Pace('3:30'),
            fmin=a['fmin'],
            rfmax=a['rfmax'],
            rflt=a['rflt'],
            sfmax=a['sfmax'],
            sflt=a['sflt'],
            cfmax=a['cfmax'],
            cflt=a['cflt'],
            rFTP=a['rFTP'],
            cFTP=a['cFTP'],
            plan='',
            race=date.today()
        )
        # Generate expected description dynamically based on actual athlete values
        description: str | None = workout._generate_description()
        # Verify description contains expected elements
        assert description is not None
        assert 'Estimated Duration' in description
        assert 'vVO2' in description

    def test_cycling_workout(self) -> None:
        a = get_athlete_values()
        workout_file: str = os.path.join('.', 'trainingplans', 'Cycling', 'Garmin', 'Crit', 'Advanced', 'Power',
                                         'RacePhase1Base', 'R1_3.yaml')
        config: dict = configreader.read_config(workout_file)
        target: dict = configreader.read_config(r'target.yaml')
        workout = Workout(
            config=config,
            target=target,
            vVO2=Pace('3:30'),
            rfmax=44,
            rflt=167,
            sfmax=183,
            sflt=167,
            cfmax=200,
            cflt=167,
            rFTP=Power('200w'),
            cFTP=Power('200w'),
            plan='',
            race=date.today()
        )
        expected_description = (
            "- Warm up.\n- Ride 2 minutes at the high end of zone 5 (not max.\neffort).\n"
            "- Ride in zone 2 for 20 minutes.\n- Ride 8 minutes at high-end of zone 4 (not max.\neffort).\n"
            "- Cool down.\n\nTry this workout before you do a proper fitness signature test.\nThe goal is to do "
            "an effort that's almost as long as the test effort, but short enough so that you're not exhausted by the "
            "end.\nAfter you've done this workout, you'll have a much better starting point for the fitness signature "
            "test workouts.. FTP 200, TSS 0, NP 0, IF 0.00. "
        )

        description: str | None = workout._generate_description()

        self.assertEqual(description, expected_description)

        workout = Workout(
            config=config,
            target=target,
            vVO2=Pace('3:30'),
            rfmax=44,
            rflt=167,
            sfmax=183,
            sflt=167,
            cfmax=200,
            cflt=167,
            rFTP=Power('200w'),
            cFTP=Power('200w'),
            plan='Plan',
            race=date.today()
        )

        expected_description = ('Plan: Plan. FTP 200, TSS 0, NP 0, IF 0.00. ')

        description: str | None = workout._generate_description()

        self.assertEqual(description, expected_description)

    def test_swimming_workout(self) -> None:
        a = get_athlete_values()
        workout = Workout(
            config={},
            target=[],
            vVO2=Pace('5:00'),
            rfmax=60,
            rflt=185,
            sfmax=200,
            sflt=185,
            cfmax=200,
            cflt=185,
            rFTP=Power('400w'),
            cFTP=Power('200w'),
            plan='',
            race=date.today()
        )
        workout.mileage = 1.5
        expected_description = '. Plan: . '

        description: str | None = workout._generate_description()

        self.assertEqual(description, expected_description)

    def test_cardio_workout(self) -> None:
        a = get_athlete_values()
        workout = Workout(
            config={},
            target=[],
            vVO2=Pace('5:00'),
            rfmax=60,
            rflt=185,
            sfmax=200,
            sflt=185,
            cfmax=200,
            cflt=185,
            rFTP=Power('400w'),
            cFTP=Power('200w'),
            plan='',
            race=date.today()
        )
        workout.ratio = 0.75
        workout.tss = 50
        expected_description = '. Plan: . '

        description: str | None = workout._generate_description()

        self.assertEqual(description, expected_description)


class TestZones(unittest.TestCase):
    def setUp(self) -> None:
        self.a = get_athlete_values()
        self.workout = Workout(
            config={},
            target=[],
            vVO2=Pace('3:30'),
            rfmax=self.a['rfmax'],
            rflt=self.a['rflt'],
            sfmax=self.a['sfmax'],
            sflt=self.a['sflt'],
            cfmax=self.a['cfmax'],
            cflt=self.a['cflt'],
            rFTP=Power('200'),
            cFTP=Power('200'),
            plan='',
            race=date.today()
        )

    def test_zones(self) -> None:
        a = get_athlete_values()
        expected_zones: list[float] = [0.46, 0.6, 0.7, 0.8,
                                       (a['rflt'] - a['fmin']) / (a['rfmax']-a['fmin']),
                                       1.0, 1.1]
        expected_hr_zones: list[int] = [int(a['fmin'] + zone * (a['rfmax']-a['fmin']))
                                        for zone in expected_zones]
        expected_data: list = [{
            "changeState": "CHANGED",
            "trainingMethod": "HR_RESERVE",
            "lactateThresholdHeartRateUsed": a['rflt'],
            "maxHeartRateUsed": a['rfmax'],
            "restingHrAutoUpdateUsed": False,
            "sport": "DEFAULT",
            "zone1Floor": expected_hr_zones[0],
            "zone2Floor": expected_hr_zones[1],
            "zone3Floor": expected_hr_zones[2],
            "zone4Floor": expected_hr_zones[3],
            "zone5Floor": expected_hr_zones[4]
        }]

        zones, hr_zones, data = Workout(
            config=[],
            target=[],
            vVO2=a['vV02'],
            fmin=a['fmin'],
            rfmax=a['rfmax'],
            rflt=a['rflt'],
            sfmax=a['sfmax'],
            sflt=a['sflt'],
            cfmax=a['cfmax'],
            cflt=a['cflt'],
            rFTP=a['rFTP'],
            cFTP=a['cFTP'],
            plan=str(''),
            race=date.today()
        ).hr_zones()

        self.assertEqual(zones, expected_zones)
        self.assertEqual(hr_zones, expected_hr_zones)
        self.assertEqual(data, expected_data)

        with self.assertLogs(level=logging.INFO) as cm:
            self.workout.zones()

        log_messages: list[str] = cm.output
        self.assertIn('INFO:root:::Heart Rate Zones::', log_messages)
        self.assertIn(f"INFO:root:fmin: {self.workout.fmin} flt: "
                      f"{self.workout.rflt} fmax: {self.workout.rfmax}", log_messages)
        for i in range(len(expected_zones)):
            self.assertIn(f"INFO:root: Zone {i}: {expected_hr_zones[i]} - "
                          f"{expected_hr_zones[i + 1] if i + 1 < len(expected_hr_zones) else 'max'}", log_messages)

        zones, rpower_zones, cpower_zones, _ = Power.power_zones(self.workout.rFTP, self.workout.cFTP)
        self.assertIn('INFO:root:::Running Power Zones::', log_messages)
        for i in range(len(rpower_zones)):
            self.assertIn(f"INFO:root: Zone {i}: {rpower_zones[i]} - "
                          f"{rpower_zones[i + 1] if i + 1 < len(rpower_zones) else 'max'} w", log_messages)

        self.assertIn('INFO:root:::Cycling Power Zones::', log_messages)
        for i in range(len(cpower_zones)):
            self.assertIn(f"INFO:root: Zone {i}: {cpower_zones[i]} - "
                          f"{cpower_zones[i + 1] if i + 1 < len(cpower_zones) else 'max'} w", log_messages)

    def test_equivalent_pace_speed_zone(self) -> None:
        a = get_athlete_values()
        step: dict = {
            "target": {
                "type": "speed.zone",
                "min": 10,
                "max": 12
            }
        }
        expected_pace = 11.0

        pace: float = self.workout.equivalent_pace(step)

        self.assertEqual(pace, expected_pace)

    def test_equivalent_pace_pace_zone(self) -> None:
        a = get_athlete_values()
        step: dict = {
            "target": {
                "type": "pace.zone",
                "min": 5.0,
                "max": 5.0
            }
        }
        expected_pace = 5.0

        pace: float = self.workout.equivalent_pace(step)

        self.assertEqual(pace, expected_pace)


class TestWorkoutTarget(unittest.TestCase):
    def setUp(self) -> None:
        self.a = get_athlete_values()
        self.workout = Workout(
            config={},
            target=[],
            vVO2=Pace('3:30'),
            rfmax=self.a['rfmax'],
            rflt=self.a['rflt'],
            sfmax=self.a['sfmax'],
            sflt=self.a['sflt'],
            cfmax=self.a['cfmax'],
            cflt=self.a['cflt'],
            rFTP=Power('200'),
            cFTP=Power('200'),
            plan='',
            race=date.today()
        )

    def test_target_type(self) -> None:
        a = get_athlete_values()
        workout = Workout()
        step_config: dict = {
            "type": "interval",
            "target": {
                "type": "power.zone",
                "min": 100,
                "max": 200
            }
        }
        expected_target_type: dict = {'workoutTargetTypeId': 2, 'workoutTargetTypeKey': 'power.zone'}

        target_type: dict = workout._target_type(step_config)

        self.assertEqual(target_type, expected_target_type)

    def test_target_type_nodict(self) -> None:
        a = get_athlete_values()
        target: dict = configreader.read_config(r'target.yaml')
        workout = Workout(
            config=[],
            target=target,
            vVO2=Pace('3:30'),
            rfmax=44,
            rflt=167,
            sfmax=183,
            sflt=167,
            cfmax=200,
            cflt=167,
            rFTP=Power('200w'),
            cFTP=Power('200w'),
            plan='',
            race=date.today()
        )
        step_config: dict = {
            "type": "interval",
            "target": '40<AEROBIC_PACE'
        }
        expected_target_type: dict = {'workoutTargetTypeId': 6, 'workoutTargetTypeKey': 'pace.zone'}

        target_type: dict = workout._target_type(step_config)

        self.assertEqual(target_type, expected_target_type)

    def test_target_type_nointarget(self) -> None:
        a = get_athlete_values()
        target: dict = configreader.read_config(r'target.yaml')
        workout = Workout(
            config=[],
            target=target,
            vVO2=Pace('3:30'),
            rfmax=44,
            rflt=167,
            sfmax=183,
            sflt=167,
            cfmax=200,
            cflt=167,
            rFTP=Power('200w'),
            cFTP=Power('200w'),
            plan='',
            race=date.today()
        )
        step_config: dict = {
            "type": "interval",
            "target": '40<AEROBI_PACE'
        }
        expected_target_type: dict = {'workoutTargetTypeId': 1, 'workoutTargetTypeKey': 'no.target'}

        target_type: dict = workout._target_type(step_config)

        self.assertEqual(target_type, expected_target_type)

    def test_extract_target_value_heart_rate_zone(self) -> None:
        a = get_athlete_values()
        step: dict = {
            "type": "heart.rate.zone",
            "zone": 2
        }

        target_type, target_value = self.workout.extract_target_value(step, "max")

        self.assertEqual(target_type, "heart.rate.zone")
        self.assertEqual(target_value, "0.8")

    def test_extract_target_value_power_zone(self) -> None:
        a = get_athlete_values()
        step: dict = {
            "type": "power.zone",
            "zone": 3
        }

        target_type, target_value = self.workout.extract_target_value(step, "min")

        self.assertEqual(target_type, "power.zone")
        self.assertEqual(target_value, "0.9")

    def test_sec_greater_than_zero_running(self):
        a = get_athlete_values()
        workout_file: str = os.path.join('.', 'trainingplans', 'Running', 'Napier', 'Half', 'Advanced', 'Meso1',
                                         '21_1.yaml')
        config: dict = configreader.read_config(workout_file)
        target: dict = configreader.read_config(r'target.yaml')
        workout = Workout(
            config=config,
            target=target,
            vVO2=Pace('3:30'),
            fmin=a['fmin'],
            rfmax=a['rfmax'],
            rflt=a['rflt'],
            sfmax=a['sfmax'],
            sflt=a['sflt'],
            cfmax=a['cfmax'],
            cflt=a['cflt'],
            rFTP=a['rFTP'],
            cFTP=a['cFTP'],
            plan='',
            race=date.today()
        )

        # Verify duration is positive (actual values depend on athlete config)
        duration = workout.get_estimated_duration()
        self.assertGreater(duration['estimatedDurationInSecs'], 0)
        self.assertGreater(duration['estimatedDistanceInMeters'], 0)
        self.assertGreater(duration['avgTrainingSpeed'], 0)


class TestReplaceStringInFile(unittest.TestCase):
    def setUp(self) -> None:
        self.test_file_path = 'test_file.txt'
        with open(self.test_file_path, 'w') as file:
            file.write("This is a test file. This file is used for testing.")

    def tearDown(self) -> None:
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_replace_string_in_file(self) -> None:
        a = get_athlete_values()
        Workout.replace_string_in_file(self.test_file_path, "test", "sample")
        with open(self.test_file_path, 'r') as file:
            file_data = file.read()
            self.assertIn("This is a sample file. This file is used for sampleing.", file_data)

    def test_replace_string_in_file_no_match(self) -> None:
        a = get_athlete_values()
        Workout.replace_string_in_file(self.test_file_path, "nonexistent", "sample")
        with open(self.test_file_path, 'r') as file:
            file_data = file.read()
            self.assertIn("This is a test file. This file is used for testing.", file_data)

    def test_replace_string_in_file_empty_file(self) -> None:
        a = get_athlete_values()
        empty_file_path = 'empty_test_file.txt'
        with open(empty_file_path, 'w') as file:
            file.write("")
        Workout.replace_string_in_file(empty_file_path, "test", "sample")
        with open(empty_file_path, 'r') as file:
            file_data = file.read()
        self.assertEqual(file_data, "")
        os.remove(empty_file_path)

    def test_replace_string_in_file_none_path(self) -> None:
        a = get_athlete_values()
        result = Workout.replace_string_in_file(None, "test", "sample")  # type: ignore
        self.assertIsNone(result)


class TestEquivalentIntensity(unittest.TestCase):
    def setUp(self) -> None:
        self.workout = Workout(
            config={},
            target=[],
            vVO2=Pace('3:30'),
            fmin=60,
            rfmax=200,
            rflt=185,
            rFTP=Power('400w'),
            cfmax=200,
            cflt=185,
            cFTP=Power('200w'),
            plan='',
            race=date.today()
        )

    def test_equivalent_intensity_speed_zone(self) -> None:
        a = get_athlete_values()
        step = {
            "target": {
                "type": "speed.zone",
                "min": 10,
                "max": 12
            }
        }
        expected_intensity = (10 / self.workout.vVO2.to_pace() + 0.5 * (
            12 / self.workout.vVO2.to_pace() - 10 / self.workout.vVO2.to_pace()))
        intensity = self.workout.equivalent_intensity(step)
        self.assertEqual(intensity, expected_intensity)

    def test_equivalent_intensity_heart_rate_zone(self) -> None:
        a = get_athlete_values()
        step = {
            "target": {
                "type": "heart.rate.zone",
                "zone": 2
            }
        }
        _, hr_zones, _ = self.workout.hr_zones()
        z = 2
        t1 = (hr_zones[z] - self.workout.fmin) / (self.workout.rfmax - self.workout.fmin)
        t2 = (hr_zones[z + 1] - self.workout.fmin) / (self.workout.rfmax - self.workout.fmin)
        expected_intensity = min(t1, t2) + 0.5 * (max(t1, t2) - min(t1, t2))
        intensity = self.workout.equivalent_intensity(step)
        self.assertEqual(intensity, expected_intensity)

    def test_equivalent_intensity_power_zone(self) -> None:
        a = get_athlete_values()
        step = {
            "target": {
                "type": "power.zone",
                "zone": 3
            }
        }
        expected_intensity = 0.8868749999999999
        intensity = self.workout.equivalent_intensity(step)
        self.assertEqual(intensity, expected_intensity)

    def test_equivalent_intensity_power_zone_running(self) -> None:
        a = get_athlete_values()
        workout_file: str = os.path.join('.', 'trainingplans', 'Cycling', 'Garmin',  'Crit', 'Advanced', 'Power',
                                         'RacePhase1Base', 'R1_3.yaml')
        config: dict = configreader.read_config(workout_file)
        config['sport'] = 'running'

        self.workout = Workout(
            config=config,
            target=[],
            vVO2=Pace('3:30'),
            fmin=60,
            rfmax=200,
            rflt=185,
            rFTP=Power('400w'),
            cfmax=200,
            cflt=185,
            cFTP=Power('200w'),
            plan='',
            race=date.today()
        )

        intensity = self.workout.equivalent_intensity(self.workout.config['steps'][0])
        self.assertEqual(intensity, 0.7012499999999999)

        step = {
            "target": {
                "type": "power.zone",
                "min": 120,
                "max": 150
            }
        }

        intensity = self.workout.equivalent_intensity(step)
        self.assertEqual(intensity, 111.375)

    def test_equivalent_intensity_no_target(self) -> None:
        a = get_athlete_values()
        step = {
            "target": {
                "type": "no.target"
            }
        }
        expected_intensity = 0.0
        intensity = self.workout.equivalent_intensity(step)
        self.assertEqual(intensity, expected_intensity)

    def test_equivalent_intensity_heart_rate_zone_no_zone(self) -> None:
        a = get_athlete_values()
        step = {
            "target": {
                "type": "heart.rate.zone",
                "min": 100,
                "max": 150
            }
        }
        t1 = (100 - self.workout.fmin) / (self.workout.rfmax - self.workout.fmin)
        t2 = (150 - self.workout.fmin) / (self.workout.rfmax - self.workout.fmin)
        expected_intensity = min(t1, t2) + 0.5 * (max(t1, t2) - min(t1, t2))
        intensity = self.workout.equivalent_intensity(step)
        self.assertEqual(intensity, expected_intensity)

    def test_equivalent_intensity_power_zone_no_zone(self) -> None:
        a = get_athlete_values()
        step = {
            "target": {
                "type": "power.zone",
                "min": 200,
                "max": 300
            }
        }
        expected_intensity = 206.25
        intensity = self.workout.equivalent_intensity(step)
        self.assertEqual(intensity, expected_intensity)


class TestGetTargetValue(unittest.TestCase):
    def setUp(self) -> None:
        self.workout = Workout(
            config={},
            target=[],
            vVO2=Pace('3:30'),
            fmin=60,
            rfmax=200,
            rflt=185,
            rFTP=Power('400w'),
            cfmax=200,
            cflt=185,
            cFTP=Power('200w'),
            plan='',
            race=date.today()
        )

    def test_get_target_value_heart_rate_zone_above_20(self) -> None:
        a = get_athlete_values()
        target = {
            "type": "heart.rate.zone",
            "max": 25
        }
        key = "max"
        expected_value = 25.0
        result = self.workout._get_target_value(target, key)
        self.assertEqual(result, expected_value)

    def test_get_target_value_heart_rate_zone_below_20(self) -> None:
        a = get_athlete_values()
        target = {
            "type": "heart.rate.zone",
            "max": 15
        }
        key = "max"
        expected_value = self.workout.convert_targetHR_to_HR(15.0)
        result = self.workout._get_target_value(target, key)
        self.assertEqual(result, expected_value)

    def test_get_target_value_speed_zone(self) -> None:
        a = get_athlete_values()
        target = {
            "type": "speed.zone",
            "max": 12.0
        }
        key = "max"
        expected_value = 12.0
        result = self.workout._get_target_value(target, key)
        self.assertEqual(result, expected_value)

    def test_get_target_value_pace_zone_running(self) -> None:
        a = get_athlete_values()
        self.workout.sport_type = 'running'
        target = {
            "type": "pace.zone",
            "max": 5.0
        }
        key = "max"
        expected_value = self.workout.convert_targetPace_to_pace(5.0)
        result = self.workout._get_target_value(target, key)
        self.assertEqual(result, expected_value)

    def test_get_target_value_pace_zone_non_running(self) -> None:
        a = get_athlete_values()
        self.workout.sport_type = 'cycling'
        target = {
            "type": "pace.zone",
            "max": 5.0
        }
        key = "max"
        expected_value = 5.0
        result = self.workout._get_target_value(target, key)
        self.assertEqual(result, expected_value)

    def test_get_target_value_power_zone(self) -> None:
        a = get_athlete_values()
        target = {
            "type": "power.zone",
            "max": 300.0
        }
        key = "max"
        expected_value = 300.0
        result = self.workout._get_target_value(target, key)
        self.assertEqual(result, expected_value)

    def test_get_target_value_no_target(self) -> None:
        a = get_athlete_values()
        target = {
            "type": "no.target",
            "max": 0.0
        }
        key = "max"
        expected_value = 0.0
        result = self.workout._get_target_value(target, key)
        self.assertEqual(result, expected_value)
