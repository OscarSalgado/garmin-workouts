import ipaddress
import os
import socket
from unittest.mock import MagicMock

import pytest
from garminconnect import Garmin

from garminworkouts.garmin.garminclient import GarminClient

# Fixed dummy account/athlete values: the default test run needs no .env and no real secrets.
DUMMY_EMAIL = "tester@example.com"
DUMMY_PASSWORD = "dummy-password"
DUMMY_ENV = {
    "GARMIN_USERNAME": DUMMY_EMAIL,
    "GARMIN_PASSWORD": DUMMY_PASSWORD,
    "vV02": "5:00",
    "fmin": "45",
    "rfmax": "185",
    "rflt": "168",
    "cfmax": "166",
    "cflt": "148",
    "sfmax": "185",
    "sflt": "167",
    "rFTP": "358w",
    "cFTP": "270w",
    "BOT_TOKEN": "dummy-token",
    "intervals_api_key": "dummy-intervals-key",
    "intervals_athlete_id": "i0",
}


def _is_live_run(config) -> bool:
    expr = (config.getoption("markexpr", default="") or "").replace(" ", "")
    return "live" in expr and "notlive" not in expr


def pytest_configure(config) -> None:
    """Outside `-m live`, force dummy credentials (even over a developer's .env) before any test is collected."""
    config._live_run = _is_live_run(config)
    if not config._live_run:
        os.environ.update(DUMMY_ENV)


class SocketBlockedError(RuntimeError):
    """Raised when a default-run test tries to reach a non-local host."""


def _is_local(host) -> bool:
    if host in (None, "", "localhost"):
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


@pytest.fixture(autouse=True)
def block_external_sockets(request, monkeypatch):
    """Fail any test that opens a connection to a non-local host (localhost stays open for pytest-httpserver)."""
    if request.config._live_run or request.node.get_closest_marker("live"):
        return
    real_connect = socket.socket.connect
    real_connect_ex = socket.socket.connect_ex
    real_getaddrinfo = socket.getaddrinfo

    def _check(address) -> None:
        host = address[0] if isinstance(address, tuple) else address
        if isinstance(address, tuple) and not _is_local(host):
            raise SocketBlockedError(f"socket blocked: default test run may not connect to {host!r}")

    def guarded_connect(self, address):
        _check(address)
        return real_connect(self, address)

    def guarded_connect_ex(self, address):
        _check(address)
        return real_connect_ex(self, address)

    def guarded_getaddrinfo(host, *args, **kwargs):
        if not _is_local(host):
            raise SocketBlockedError(f"socket blocked: default test run may not resolve {host!r}")
        return real_getaddrinfo(host, *args, **kwargs)

    monkeypatch.setattr(socket.socket, "connect", guarded_connect)
    monkeypatch.setattr(socket.socket, "connect_ex", guarded_connect_ex)
    monkeypatch.setattr(socket, "getaddrinfo", guarded_getaddrinfo)


@pytest.fixture
def authed_gclient() -> GarminClient:
    """GarminClient backed by a mocked Garmin client: tests never touch the network."""
    fake = MagicMock(spec=Garmin)
    fake.display_name = "tester"
    fake.full_name = "Test User"
    fake.unit_system = "metric"
    fake.client = MagicMock()
    fake.client.is_authenticated = False
    return GarminClient(DUMMY_EMAIL, DUMMY_PASSWORD, client=fake)


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
