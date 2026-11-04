"""IntervalsTarget and IntervalsWorkout with fake workouts and a stubbed HTTP layer."""
import logging
from datetime import date, timedelta
from unittest import mock

import pytest

from intervalsicu.intervals import workout as workout_module
from intervalsicu.intervals.workout import IntervalsWorkout


class FakeWorkout:
    def __init__(self, day, sport="running", mileage=10.0, duration=timedelta(hours=1), name="w", steps=None):
        self.day = day
        self.config = {"sport": sport, "steps": steps or [], "sub_type": None}
        self.mileage = mileage
        self.duration = duration
        self.sec = int(duration.total_seconds()) if duration else 0
        self.name = name

    def get_workout_date(self):
        return self.day, 0, 0

    def get_workout_name(self):
        return self.name

    def _steps(self, steps):
        return steps


def _monday_in_future(weeks=2) -> date:
    today = date.today()
    return today - timedelta(days=today.weekday()) + timedelta(weeks=weeks)


@pytest.fixture
def api() -> IntervalsWorkout:
    return IntervalsWorkout("ath", "key")


# ---- target ------------------------------------------------------------------------------------------------

def test_sport_target_metrics_sums_per_week(api) -> None:
    monday = _monday_in_future()
    workouts = [
        FakeWorkout(monday, mileage=10, duration=timedelta(hours=1)),
        FakeWorkout(monday + timedelta(days=2), mileage=5, duration=timedelta(minutes=30)),
        FakeWorkout(monday + timedelta(days=2), sport="cycling", mileage=50),
        FakeWorkout(monday + timedelta(days=20), mileage=99),            # outside the range
        FakeWorkout(monday, mileage=None, duration=None),                # nothing to add
    ]
    mondays, mileage, duration = api.get_sport_target_metrics(workouts, monday, monday + timedelta(days=13), "Run")
    assert mondays == [monday, monday + timedelta(days=7)]
    assert mileage == [15, 0]
    assert duration == [5400, 0]
    _, ride_mileage, ride_duration = api.get_sport_target_metrics(
        workouts, monday, monday + timedelta(days=13), "Ride")
    assert ride_mileage == [0, 0] and ride_duration == [3600, 0]


def test_set_targets_uploads_future_targets(api) -> None:
    monday = _monday_in_future()
    with mock.patch.object(api, "upload_events") as upload:
        api.set_targets([FakeWorkout(monday)], monday, monday + timedelta(days=6))
    data = upload.call_args.args[0]
    assert data[0]["category"] == "TARGET" and data[0]["type"] == "Run"
    assert data[0]["distance_target"] == 10000.0 and data[0]["time_target"] == 3600


def test_set_targets_warns_when_nothing_to_upload(api, caplog) -> None:
    monday = _monday_in_future()
    with mock.patch.object(api, "upload_events") as upload, caplog.at_level(logging.WARNING):
        api.set_targets([], monday, monday + timedelta(days=6))
    upload.assert_not_called()
    assert "No targets to upload" in caplog.text


def test_set_targets_skips_past_weeks_and_empty_weeks(api) -> None:
    past_monday = date.today() - timedelta(days=date.today().weekday()) - timedelta(weeks=3)
    future_monday = _monday_in_future()
    data: list = []
    api.set_targets_(data, "Run", [past_monday, future_monday], [5, 0], [100, 0])
    assert data == []


# ---- steps -------------------------------------------------------------------------------------------------

def _step(**kw):
    step = {"stepType": {"stepTypeKey": "interval"}, "endCondition": {"conditionTypeKey": "time"},
            "endConditionValue": 60, "targetType": {"workoutTargetTypeKey": "no.target"}}
    step.update(kw)
    return step


def test_step_format_end_conditions(api) -> None:
    assert api.step_format(190, 4.0, 250, _step())["duration"] == 60
    dist = api.step_format(190, 4.0, 250, _step(endCondition={"conditionTypeKey": "distance"},
                                                  endConditionValue=1000))
    assert dist["distance"] == 1000
    lap = api.step_format(190, 4.0, 250, _step(endCondition={"conditionTypeKey": "lap.button"}))
    assert lap["until_lap_press"] is True and lap["text"] == "Press lap" and "description" not in lap


@pytest.mark.parametrize("target, key, units, fmt", [
    ("heart.rate.zone", "hr", "%hr", "% HR"),
    ("pace.zone", "pace", "%pace", "% Pace"),
    ("power.zone", "power", "%ftp", "% intensity"),
    ("power.3s", "power", "%ftp", "power=3s"),
])
def test_step_format_targets(api, target, key, units, fmt) -> None:
    step = _step(targetType={"workoutTargetTypeKey": target}, targetValueOne=100, targetValueTwo=200,
                 description="warm")
    result = api.step_format(200, 4.0, 100, step)
    assert result[key] == {"units": units, "start": "50" if key == "hr" else mock.ANY, "end": mock.ANY}
    assert fmt in result["description"] and result["text"] == result["description"]
    assert "targetType" not in result and "stepType" not in result


@pytest.mark.parametrize("target, key", [
    ("heart.rate.zone", "hr"), ("pace.zone", "pace"), ("power.zone", "power"), ("power.3s", "power")])
def test_step_format_missing_thresholds_give_zero(api, target, key) -> None:
    result = api.step_format(None, None, None, _step(targetType={"workoutTargetTypeKey": target},
                                                      targetValueOne=100, targetValueTwo=200))
    assert result[key]["start"] == "0" and result[key]["end"] == "0"


def test_step_format_no_target_and_none_description(api) -> None:
    result = api.step_format(190, 4.0, 250, _step(description=None))
    assert result["description"].endswith("workout - No target")


def test_expand_repeats(api) -> None:
    steps = [
        _step(),
        {"stepType": {"stepTypeKey": "repeat"}, "numberOfIterations": 3, "workoutSteps": [
            _step(), _step(endCondition={"conditionTypeKey": "distance"}, endConditionValue=500)]},
        {"stepType": {"stepTypeKey": "repeat"}, "workoutSteps": []},
        {"stepType": {"stepTypeKey": "mystery"}, "description": "x"},
    ]
    out = api.expand_repeats(190, 4.0, 250, steps)
    assert out[0]["duration"] == 60
    assert out[1]["reps"] == "3" and out[1]["duration"] == 60 and out[1]["distance"] == 500
    assert out[2]["reps"] == "1" and "duration" not in out[2] and "distance" not in out[2]
    assert out[3]["description"] == ""


def test_duration_string_branches() -> None:
    lines: list = []
    IntervalsWorkout.duration_string(lines, {"duration": 3725, "description": "easy"})
    IntervalsWorkout.duration_string(lines, {"duration": 30, "text": "Press lap", "description": "rest it"})
    IntervalsWorkout.duration_string(lines, {"duration": 30, "text": "Press lap"})
    IntervalsWorkout.duration_string(lines, {"distance": 1500, "description": "fast"})
    IntervalsWorkout.duration_string(lines, {"reps": "2", "steps": [
        {"duration": 60, "description": "a"}, {"distance": 400, "description": "b"}, {"other": 1}]})
    IntervalsWorkout.duration_string(lines, {"description": "free text"})
    assert lines == [
        "- 1h2m5s in easy",
        "- Press lap 30s in rest it",
        "- Press lap 30s in rest",
        "- 1.5km in fast",
        "\n2x", "  - 1m in a", "  - 0.4km in b",
        "- free text",
    ]


# ---- training data -----------------------------------------------------------------------------------------

def test_format_training_data(api) -> None:
    day = date(2026, 3, 10)
    steps = [_step(description="a")]
    workouts = {"trainings": [
        FakeWorkout(day, steps=list(steps), name="in range"),
        FakeWorkout(day + timedelta(days=100), steps=list(steps), name="too late"),
        FakeWorkout(day, sport="unknown sport", steps=[_step(), {"stepType": {"stepTypeKey": "repeat"},
                                                                  "numberOfIterations": 2,
                                                                  "workoutSteps": [_step()]}], name="other"),
    ]}

    def settings(sport):
        return {} if sport == "Other" else {"threshold_pace": 4.0, "max_hr": 190, "ftp": 250}

    with mock.patch.object(api, "get_sport_settings", side_effect=lambda sport: settings(sport)):
        out = api.format_training_data(workouts, plan_folder={"id": 7, "start_date_local": "2026-03-01T00:00:00"},
                                       day_a=day, day_b=day + timedelta(days=1))
        no_folder = api.format_training_data(workouts, day_a=day, day_b=day + timedelta(days=1))
    assert [w["name"] for w in out] == ["in range", "other"]
    assert out[0]["folder_id"] == 7 and out[0]["day"] == 9 and out[0]["type"] == "Run"
    assert out[1]["type"] == "Other"
    assert no_folder[0]["folder_id"] is None
    assert "2x" in out[1]["description"]


def test_format_training_data_without_sport_settings_entry(api) -> None:
    day = date(2026, 3, 10)
    with mock.patch.object(api, "get_sport_settings", return_value={}), \
            mock.patch.object(IntervalsWorkout, "format_sport", return_value="Unlisted"):
        out = api.format_training_data({"trainings": [FakeWorkout(day, steps=[_step()])]},
                                       day_a=day, day_b=day)
    assert len(out) == 1


# ---- athlete data ------------------------------------------------------------------------------------------

def test_update_athlete_data(api) -> None:
    class VAM:
        @staticmethod
        def to_pace():
            return 2.0

    class FTP:
        power = "250w"

    athlete = {"fmin": 45, "rfmax": 185, "rflt": 168, "cfmax": 166, "cflt": 148, "sfmax": 185, "sflt": 167,
               "vV02": VAM(), "cFTP": FTP()}

    def settings(sport):
        return {"id": f"id-{sport}"} if sport != "Walk" else {}

    with mock.patch.object(workout_module.configreader, "read_config", return_value={"R2": {"min": "0.5"}}), \
            mock.patch.object(workout_module.account, "get_athlete_config", return_value=athlete), \
            mock.patch.object(api, "get_sport_settings", side_effect=settings), \
            mock.patch.object(api, "update_resting_hr") as rhr, \
            mock.patch.object(api, "update_threshold_pace") as pace, \
            mock.patch.object(api, "update_max_hr") as max_hr, \
            mock.patch.object(api, "update_lthr") as lthr, \
            mock.patch.object(api, "update_hrrc_min_percent") as hrrc, \
            mock.patch.object(api, "update_ftp") as ftp:
        api.update_athlete_data()
    rhr.assert_called_once_with(resting_hr=45)
    pace.assert_called_once_with(threshold_pace=1.0, id="id-Run")
    assert [c.kwargs["id"] for c in max_hr.call_args_list] == ["id-Run", "id-Swim", "id-Ride"]
    assert lthr.call_count == 3 and hrrc.call_count == 3
    ftp.assert_called_once_with(ftp=250, indoor_ftp=250, id="id-Ride")


# ---- folders -----------------------------------------------------------------------------------------------

def test_list_folders_and_plans(api) -> None:
    folders = [{"name": "A", "type": "FOLDER"}, {"name": "P", "type": "PLAN"}, {"name": "X"}]
    with mock.patch.object(api, "list_folders", return_value=folders):
        assert list(api.list_workout_folders()) == ["A"]
        assert list(api.list_plans()) == ["P"]

