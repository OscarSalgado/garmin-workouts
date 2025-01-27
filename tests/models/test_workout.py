import unittest
from datetime import date, timedelta
from unittest.mock import patch
import account
import logging
import os
from garminworkouts.models.fields import _STEPS
from garminworkouts.models.workout import Workout
from garminworkouts.models.pace import Pace
from garminworkouts.models.power import Power
from garminworkouts.config import configreader


class TestWorkout(unittest.TestCase):
    def test_null_workout(self) -> None:
        with self.assertRaises(ValueError):
            Workout(
                config={'name': 'name'},
                target=[],
                vVO2=Pace('3:30'),
                fmin=account.fmin,
                fmax=account.fmax,
                flt=account.flt,
                rFTP=Power('200'),
                cFTP=Power('200'),
                plan='',
                race=date.today()
            ).create_workout()

    def test_get_workout_name(self) -> None:
        # Create a Workout instance with a specific configuration
        workout_file: str = os.path.join('.', 'workouts', 'cardio_training', 'ADVANCED', 'BBtO4iZ.yaml')
        config: dict = configreader.read_config(workout_file)
        workout = Workout(
            config=config,
            target=[],
            vVO2=Pace('3:30'),
            fmin=account.fmin,
            fmax=account.fmax,
            flt=account.flt,
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
        # Create a Workout instance with a specific configuration
        workout_file: str = os.path.join('.', 'workouts', 'cardio_training', 'ADVANCED', 'BBtO4iZ.yaml')
        config: dict = configreader.read_config(workout_file)
        config['name'] = '0_1'
        config['description'] = ''
        workout = Workout(
            config=config,
            target=[],
            vVO2=Pace('3:30'),
            fmin=account.fmin,
            fmax=account.fmax,
            flt=account.flt,
            rFTP=Power('200'),
            cFTP=Power('200'),
            plan='',
            race=date.today()
        )

        # Call the get_workout_name method
        workout_name: str = workout.get_workout_name()
        self.assertEqual(workout_name, '0_1')

    def test_get_workout_name_med(self) -> None:
        # Create a Workout instance with a specific configuration
        workout_file: str = os.path.join('.', 'workouts', 'cardio_training', 'ADVANCED', 'BBtO4iZ.yaml')
        config: dict = configreader.read_config(workout_file)
        config['name'] = '0_1'
        config['description'] = 'Description'
        workout = Workout(
            config=config,
            target=[],
            vVO2=Pace('3:30'),
            fmin=account.fmin,
            fmax=account.fmax,
            flt=account.flt,
            rFTP=Power('200'),
            cFTP=Power('200'),
            plan='plan',
            race=date.today()
        )

        # Call the get_workout_name method
        workout_name: str = workout.get_workout_name()
        self.assertEqual(workout_name, '0_1-Description')

    def test_get_workout_name_long(self) -> None:
        # Create a Workout instance with a specific configuration
        workout_file: str = os.path.join('.', 'workouts', 'cardio_training', 'ADVANCED', 'BBtO4iZ.yaml')
        config: dict = configreader.read_config(workout_file)
        config['name'] = '0_1'
        config['description'] = 'Long description for a long workout name'
        workout = Workout(
            config=config,
            target=[],
            vVO2=Pace('3:30'),
            fmin=account.fmin,
            fmax=account.fmax,
            flt=account.flt,
            rFTP=Power('200'),
            cFTP=Power('200'),
            plan='',
            race=date.today()
        )

        # Call the get_workout_name method
        workout_name: str = workout.get_workout_name()
        self.assertEqual(workout_name, '0_1-Long')

    def test_get_workout_date(self) -> None:
        # Create a Workout instance with a specific configuration
        workout = Workout(
            config={},
            target=[],
            vVO2=Pace('5:00'),
            fmin=60,
            fmax=200,
            flt=185,
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
        workout: dict = {}

        author: dict = Workout.extract_workout_author(workout)

        self.assertIsNone(author)

    def test_extract_workout_author_missing_name(self) -> None:
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
        workout_file: str = os.path.join('.', 'workouts', 'cardio_training', 'ADVANCED', 'BBtO4iZ.yaml')
        config: dict = configreader.read_config(workout_file)
        config['description'] = ''
        workout = Workout(
            config=config,
            target=[],
            vVO2=Pace('3:30'),
            fmin=account.fmin,
            fmax=account.fmax,
            flt=account.flt,
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
            'description': '. Plan: . ECOs: 0',
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
        workout: dict = {
            'ownerId': '12345'
        }

        owner_id: str = Workout.extract_workout_owner_id(workout)

        self.assertEqual(owner_id, '12345')

    def test_running_workout_with_plan(self) -> None:
        workout_file: str = os.path.join('.', 'trainingplans', 'Running', 'Napier', 'Half', 'Advanced', 'Meso1',
                                         '21_1.yaml')
        config: dict = configreader.read_config(workout_file)
        target: dict = configreader.read_config(r'target.yaml')
        workout = Workout(
            config=config,
            target=target,
            vVO2=Pace('3:30'),
            fmin=44,
            fmax=183,
            flt=167,
            rFTP=Power('200'),
            cFTP=Power('200'),
            plan='5K Training Plan',
            race=date.today()
        )
        expected_description = (
            'Plan: 5K Training Plan. Estimated Duration: 0:50:00; 8.87 km. 5:38 min/km - 62.06% vVO2. '
            'rTSS: 32.0. ECOs: 100.0. '
        )

        description: str | None = workout._generate_description()

        self.assertEqual(description, expected_description)

    def test_running_workout_without_plan(self) -> None:
        workout_file: str = os.path.join('.', 'trainingplans', 'Running', 'Napier', 'Half', 'Advanced', 'Meso1',
                                         '21_1.yaml')
        config: dict = configreader.read_config(workout_file)
        target: dict = configreader.read_config(r'target.yaml')
        workout = Workout(
            config=config,
            target=target,
            vVO2=Pace('3:30'),
            fmin=44,
            fmax=183,
            flt=167,
            rFTP=Power('200w'),
            cFTP=Power('200w'),
            plan='',
            race=date.today()
        )
        expected_description = (
            'W1-Short Run. Estimated Duration: 0:50:00; 8.87 km. 5:38 min/km - 62.06% vVO2. '
            'rTSS: 32.0. ECOs: 100.0. '
        )

        description: str | None = workout._generate_description()

        self.assertEqual(description, expected_description)

    def test_cycling_workout(self) -> None:
        workout_file: str = os.path.join('.', 'trainingplans', 'Cycling', 'Garmin', 'Crit', 'Advanced', 'Power',
                                         'RacePhase1Base', 'R1_3.yaml')
        config: dict = configreader.read_config(workout_file)
        target: dict = configreader.read_config(r'target.yaml')
        workout = Workout(
            config=config,
            target=target,
            vVO2=Pace('3:30'),
            fmin=44,
            fmax=183,
            flt=167,
            rFTP=Power('200w'),
            cFTP=Power('200w'),
            plan='',
            race=date.today()
        )
        expected_description = (
            "- Warm up.\n- Ride 2 minutes at the high end of zone 5 (not max.\neffort).\n"
            "- Ride in zone 2 for 20 minutes.\n- Ride 8 minutes at high-end of zone 4 (not max.\neffort).\n"
            "- Cool down.\n\nTry this workout before you do a "
            "proper fitness signature test.\nThe goal is to do an effort that's almost as long as the test effort, but "
            "short enough so that you're not exhausted by the end.\nAfter you've done this workout, you'll have a much "
            "better starting point for the fitness signature test workouts.. FTP 200, TSS 96, NP 195, IF 0.98. "
            "ECOs: 468.0"
        )

        description: str | None = workout._generate_description()

        self.assertEqual(description, expected_description)

    def test_swimming_workout(self) -> None:
        workout = Workout(
            config={},
            target=[],
            vVO2=Pace('5:00'),
            fmin=60,
            fmax=200,
            flt=185,
            rFTP=Power('400w'),
            cFTP=Power('200w'),
            plan='',
            race=date.today()
        )
        workout.mileage = 1.5
        expected_description = '. Plan: . ECOs: 0'

        description: str | None = workout._generate_description()

        self.assertEqual(description, expected_description)

    def test_cardio_workout(self) -> None:
        workout = Workout(
            config={},
            target=[],
            vVO2=Pace('5:00'),
            fmin=60,
            fmax=200,
            flt=185,
            rFTP=Power('400w'),
            cFTP=Power('200w'),
            plan='',
            race=date.today()
        )
        workout.ratio = 0.75
        workout.tss = 50
        expected_description = '. Plan: . ECOs: 0'

        description: str | None = workout._generate_description()

        self.assertEqual(description, expected_description)


class TestZones(unittest.TestCase):
    def setUp(self) -> None:
        self.workout = Workout(
            config={},
            target=[],
            vVO2=Pace('3:30'),
            fmin=account.fmin,
            fmax=account.fmax,
            flt=account.flt,
            rFTP=Power('200'),
            cFTP=Power('200'),
            plan='',
            race=date.today()
        )

    def test_zones(self) -> None:
        expected_zones: list[float] = [0.46, 0.6, 0.7, 0.8,
                                       (account.flt - account.fmin) / (account.fmax-account.fmin),
                                       1.0, 1.1]
        expected_hr_zones: list[int] = [int(account.fmin + zone * (account.fmax-account.fmin))
                                        for zone in expected_zones]
        expected_data: list = [{
            "changeState": "CHANGED",
            "trainingMethod": "HR_RESERVE",
            "lactateThresholdHeartRateUsed": account.flt,
            "maxHeartRateUsed": account.fmax,
            "restingHrAutoUpdateUsed": False,
            "sport": "DEFAULT",
            "zone1Floor": expected_hr_zones[0],
            "zone2Floor": expected_hr_zones[1],
            "zone3Floor": expected_hr_zones[2],
            "zone4Floor": expected_hr_zones[3],
            "zone5Floor": expected_hr_zones[4]
        }]

        zones, hr_zones, data = Workout(
            [],
            [],
            account.vV02,
            account.fmin,
            account.fmax,
            account.flt,
            account.rFTP,
            account.cFTP,
            str(''),
            date.today()
        ).hr_zones()

        self.assertEqual(zones, expected_zones)
        self.assertEqual(hr_zones, expected_hr_zones)
        self.assertEqual(data, expected_data)

        with self.assertLogs(level=logging.INFO) as cm:
            self.workout.zones()

        log_messages: list[str] = cm.output
        self.assertIn('INFO:root:::Heart Rate Zones::', log_messages)
        self.assertIn(f"INFO:root:fmin: {self.workout.fmin} flt: "
                      f"{self.workout.flt} fmax: {self.workout.fmax}", log_messages)
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
        self.workout = Workout(
            config={},
            target=[],
            vVO2=Pace('3:30'),
            fmin=account.fmin,
            fmax=account.fmax,
            flt=account.flt,
            rFTP=Power('200'),
            cFTP=Power('200'),
            plan='',
            race=date.today()
        )

    def test_target_type(self) -> None:
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
        target: dict = configreader.read_config(r'target.yaml')
        workout = Workout(
            config=[],
            target=target,
            vVO2=Pace('3:30'),
            fmin=44,
            fmax=183,
            flt=167,
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
        target: dict = configreader.read_config(r'target.yaml')
        workout = Workout(
            config=[],
            target=target,
            vVO2=Pace('3:30'),
            fmin=44,
            fmax=183,
            flt=167,
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
        step: dict = {
            "type": "heart.rate.zone",
            "zone": 2
        }

        target_type, target_value = self.workout.extract_target_value(step, "max")

        self.assertEqual(target_type, "heart.rate.zone")
        self.assertEqual(target_value, "0.8")

    def test_extract_target_value_power_zone(self) -> None:
        step: dict = {
            "type": "power.zone",
            "zone": 3
        }

        target_type, target_value = self.workout.extract_target_value(step, "min")

        self.assertEqual(target_type, "power.zone")
        self.assertEqual(target_value, "0.9")

    def test_sec_greater_than_zero_running(self):
        workout_file: str = os.path.join('.', 'trainingplans', 'Running', 'Napier', 'Half', 'Advanced', 'Meso1',
                                         '21_1.yaml')
        config: dict = configreader.read_config(workout_file)
        target: dict = configreader.read_config(r'target.yaml')
        workout = Workout(
            config=config,
            target=target,
            vVO2=Pace('3:30'),
            fmin=44,
            fmax=183,
            flt=167,
            rFTP=Power('200w'),
            cFTP=Power('200w'),
            plan='',
            race=date.today()
        )

        expected_duration: dict = {
            'estimatedDurationInSecs': 3000,
            'estimatedDistanceInMeters': 8870.0,
            'avgTrainingSpeed': 2.9566666666666666}

        self.assertEqual(workout.get_estimated_duration(), expected_duration)


class TestLoadMetrics(unittest.TestCase):
    def test_load_metrics(self) -> None:
        # Create mock workouts
        target: dict = configreader.read_config(r'target.yaml')

        workout_file: str = os.path.join('.', 'trainingplans', 'Running', 'Napier', 'Half', 'Advanced', 'Meso1',
                                         '21_1.yaml')
        config: dict = configreader.read_config(workout_file)
        workout1 = Workout(
            config=config,
            target=target,
            vVO2=Pace('3:30'),
            fmin=44,
            fmax=183,
            flt=167,
            rFTP=Power('200w'),
            cFTP=Power('200w'),
            plan='',
            race=date(2024, 1, 1)
        )

        workout_file: str = os.path.join('.', 'trainingplans', 'Running', 'Napier', 'Half', 'Advanced', 'Meso1',
                                         '21_2.yaml')
        config: dict = configreader.read_config(workout_file)
        workout2 = Workout(
            config=config,
            target=target,
            vVO2=Pace('3:30'),
            fmin=44,
            fmax=183,
            flt=167,
            rFTP=Power('200w'),
            cFTP=Power('200w'),
            plan='',
            race=date(2024, 1, 1)
        )

        workout_file: str = os.path.join('.', 'trainingplans', 'Running', 'Napier', 'Half', 'Advanced', 'Meso2',
                                         '20_2.yaml')
        config: dict = configreader.read_config(workout_file)
        workout3 = Workout(
            config=config,
            target=target,
            vVO2=Pace('3:30'),
            fmin=44,
            fmax=183,
            flt=167,
            rFTP=Power('200w'),
            cFTP=Power('200w'),
            plan='',
            race=date(2024, 1, 1)
        )

        workouts = [workout2, workout1, workout3]

        # Call load_metrics
        mileage, duration, tss, ECOs, Rdist, Rdists, day_min, day_max = Workout.load_metrics(workouts)

        # Assert the results
        self.assertEqual(mileage[21], 12.87)
        self.assertEqual(duration[21], timedelta(seconds=4631))
        self.assertEqual(tss[21], 115572.0)
        self.assertEqual(ECOs[21], 127.0)
        self.assertEqual(Rdist, [3670, 3000, 0, 0, 0, 0, 0, 0])
        self.assertEqual(Rdists[21], [1631, 3000, 0, 0, 0, 0, 0, 0])
        self.assertEqual(day_min, date(2023, 8, 1))
        self.assertEqual(day_max, date(2023, 8, 9))

        with self.assertLogs(level=logging.INFO) as cm:
            Workout.load_metrics(workouts)

        log_messages = cm.output
        self.assertEqual(['INFO:root:From 2023-08-01 to 2023-08-09',
                          'INFO:root:Week 21: 12.87 km - Duration: 1:17:11 - ECOs: 127.0',
                          'INFO:root:Week 20: 5.0 km - Duration: 0:33:59 - ECOs: 34.0'], log_messages)


class TestIntensityFactor(unittest.TestCase):
    def setUp(self):
        self.workout = Workout(
            config={},
            target=[],
            vVO2=Pace('5:00'),
            fmin=60,
            fmax=200,
            flt=185,
            rFTP=Power('400w'),
            cFTP=Power('200w'),
            plan='',
            race=date.today()
            )

    def test_intensity_factor_below_0_5(self):
        v = 0.4
        duration_secs = 100
        Rdist = [0] * 8
        c, Rdist = self.workout.intensity_factor(v, duration_secs, Rdist)
        self.assertEqual(c, 0.0)
        self.assertEqual(Rdist, [0, 0, 0, 0, 0, 0, 0, 0])

    def test_intensity_factor_R0(self):
        v = 0.6
        duration_secs = 100
        Rdist = [0] * 8
        c, Rdist = self.workout.intensity_factor(v, duration_secs, Rdist)
        self.assertEqual(c, 1.0)
        self.assertEqual(Rdist, [100, 0, 0, 0, 0, 0, 0, 0])

    def test_intensity_factor_R1(self):
        v = 0.7
        duration_secs = 100
        Rdist = [0] * 8
        c, Rdist = self.workout.intensity_factor(v, duration_secs, Rdist)
        self.assertEqual(c, 2.0)
        self.assertEqual(Rdist, [0, 100, 0, 0, 0, 0, 0, 0])

    def test_intensity_factor_R2(self):
        v = 0.8
        duration_secs = 100
        Rdist = [0] * 8
        c, Rdist = self.workout.intensity_factor(v, duration_secs, Rdist)
        self.assertEqual(c, 3.0)
        self.assertEqual(Rdist, [0, 0, 100, 0, 0, 0, 0, 0])

    def test_intensity_factor_R3(self):
        v = 0.9
        duration_secs = 100
        Rdist = [0] * 8
        c, Rdist = self.workout.intensity_factor(v, duration_secs, Rdist)
        self.assertEqual(c, 5.0)
        self.assertEqual(Rdist, [0, 0, 0, 100, 0, 0, 0, 0])

    def test_intensity_factor_R3_plus(self):
        v = 1.0
        duration_secs = 100
        Rdist = [0] * 8
        c, Rdist = self.workout.intensity_factor(v, duration_secs, Rdist)
        self.assertEqual(c, 9.0)
        self.assertEqual(Rdist, [0, 0, 0, 0, 100, 0, 0, 0])

    def test_intensity_factor_R4(self):
        v = 1.1
        duration_secs = 100
        Rdist = [0] * 8
        c, Rdist = self.workout.intensity_factor(v, duration_secs, Rdist)
        self.assertEqual(c, 15.0)
        self.assertEqual(Rdist, [0, 0, 0, 0, 0, 100, 0, 0])

    def test_intensity_factor_R5(self):
        v = 1.3
        duration_secs = 100
        Rdist = [0] * 8
        c, Rdist = self.workout.intensity_factor(v, duration_secs, Rdist)
        self.assertEqual(c, 40.0)
        self.assertEqual(Rdist, [0, 0, 0, 0, 0, 0, 100, 0])

    def test_intensity_factor_R6(self):
        v = 1.6
        duration_secs = 100
        Rdist = [0] * 8
        c, Rdist = self.workout.intensity_factor(v, duration_secs, Rdist)
        self.assertEqual(c, 50.0)
        self.assertEqual(Rdist, [0, 0, 0, 0, 0, 0, 0, 100])

    def test_standard_density_standard_density_too_high_R3(self):
        with self.assertRaises(ValueError):
            self.workout.standard_density(120, 10, 0, 0, 0, 0, 0)

    def test_standard_density_standard_density_too_high_R3_plus(self):
        with self.assertRaises(ValueError):
            self.workout.standard_density(100, 10, 10, 50, 50, 50, 8.0)

    def test_standard_density_standard_density_too_high_R4(self):
        with self.assertRaises(ValueError):
            self.workout.standard_density(100, 10, 10, 50, 50, 50, 14.0)

    def test_standard_density_standard_density_too_high_R5_R6(self):
        with self.assertRaises(ValueError):
            self.workout.standard_density(100, 10, 10, 50, 50, 50, 16.0)


class TestReplaceStringInFile(unittest.TestCase):
    def setUp(self) -> None:
        self.test_file_path = 'test_file.txt'
        with open(self.test_file_path, 'w') as file:
            file.write("This is a test file. This file is used for testing.")

    def tearDown(self) -> None:
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_replace_string_in_file(self) -> None:
        Workout.replace_string_in_file(self.test_file_path, "test", "sample")
        with open(self.test_file_path, 'r') as file:
            file_data = file.read()
            self.assertIn("This is a sample file. This file is used for sampleing.", file_data)

    def test_replace_string_in_file_no_match(self) -> None:
        Workout.replace_string_in_file(self.test_file_path, "nonexistent", "sample")
        with open(self.test_file_path, 'r') as file:
            file_data = file.read()
            self.assertIn("This is a test file. This file is used for testing.", file_data)

    def test_replace_string_in_file_empty_file(self) -> None:
        empty_file_path = 'empty_test_file.txt'
        with open(empty_file_path, 'w') as file:
            file.write("")
        Workout.replace_string_in_file(empty_file_path, "test", "sample")
        with open(empty_file_path, 'r') as file:
            file_data = file.read()
        self.assertEqual(file_data, "")
        os.remove(empty_file_path)

    def test_replace_string_in_file_none_path(self) -> None:
        result = Workout.replace_string_in_file(None, "test", "sample")  # type: ignore
        self.assertIsNone(result)


class TestCalculateECOs(unittest.TestCase):
    def setUp(self) -> None:
        self.workout = Workout(
            config={},
            target=[],
            vVO2=Pace('5:00'),
            fmin=60,
            fmax=200,
            flt=185,
            rFTP=Power('400w'),
            cFTP=Power('200w'),
            plan='',
            race=date.today()
            )

    def test_calculate_ECOs_with_intensity_factors(self) -> None:
        ECOs = 100
        intensity_factor_list = [0.5, 1.0]
        expected_ECOs = 120.0
        result = self.workout.calculate_ECOs(ECOs, intensity_factor_list)
        self.assertEqual(result, expected_ECOs)

    def test_calculate_ECOs_with_single_intensity_factor(self) -> None:
        ECOs = 100
        intensity_factor_list = [1.0]
        expected_ECOs = 100
        result = self.workout.calculate_ECOs(ECOs, intensity_factor_list)
        self.assertEqual(result, expected_ECOs)

    def test_calculate_ECOs_with_empty_intensity_factor_list(self) -> None:
        ECOs = 100
        intensity_factor_list = []
        expected_ECOs = 100
        result = self.workout.calculate_ECOs(ECOs, intensity_factor_list)
        self.assertEqual(result, expected_ECOs)

    def test_calculate_ECOs_with_zero_intensity_factor(self) -> None:
        ECOs = 100
        intensity_factor_list = [1.0, 0.0]
        expected_ECOs = 100
        result = self.workout.calculate_ECOs(ECOs, intensity_factor_list)
        self.assertEqual(result, expected_ECOs)
