from unittest.mock import MagicMock

import pytest
from garminconnect import Garmin

from garminworkouts.garmin.garminclient import GarminClient
import account


@pytest.fixture
def authed_gclient() -> GarminClient:
    """GarminClient backed by a mocked Garmin client: tests never touch the network."""
    email, password = account.get_credentials()
    fake = MagicMock(spec=Garmin)
    fake.display_name = "tester"
    fake.full_name = "Test User"
    fake.unit_system = "metric"
    fake.client = MagicMock()
    fake.client.is_authenticated = False
    return GarminClient(email, password, client=fake)


_PROTECTED_SOURCES = (
    "garminworkouts/models/strength.py",
    "garminworkouts/models/types.py",
    "garminworkouts/garmin/garminapi.py",
)


@pytest.fixture(autouse=True)
def protect_source_files(tmp_path, monkeypatch):
    """GarminTypes rewrites source files from API payloads; never let tests do that to the real ones."""
    import builtins
    import os
    import shutil

    real_open = builtins.open

    def guarded_open(file, mode="r", *args, **kwargs):
        if isinstance(file, (str, os.PathLike)) and any(c in mode for c in "wa+"):
            norm = os.path.abspath(os.fspath(file)).replace("\\", "/")
            if any(norm.endswith(p) for p in _PROTECTED_SOURCES):
                copy = tmp_path / os.path.basename(norm)
                if not copy.exists():
                    shutil.copyfile(norm, copy)
                file = copy
        return real_open(file, mode, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", guarded_open)
