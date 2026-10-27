import pytest
from garminworkouts.garmin.garminclient import GarminClient
import account


@pytest.fixture
def authed_gclient() -> GarminClient:
    email, password = account.get_credentials()
    return GarminClient(email, password)
