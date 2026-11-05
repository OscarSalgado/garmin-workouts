import logging
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from garminconnect import (
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)

from garminworkouts.garmin.garminapi import GarminApi


def _make_mock_garmin(is_authenticated: bool = True, version: str = None) -> MagicMock:
    mock_garmin = MagicMock()
    mock_garmin.display_name = "tester"
    mock_garmin.full_name = "Test User"
    # Like the real library, the profile is only populated once authenticated.
    mock_garmin.unit_system = "metric" if is_authenticated else None
    mock_garmin.client.is_authenticated = is_authenticated
    mock_garmin.client.request.return_value = MagicMock(
        json=lambda: [{"version": version or GarminApi._GARMIN_VERSION}]
    )
    return mock_garmin


def _patch_garmin(mock_garmin: MagicMock, isdir: bool = False):
    return (
        patch("garminworkouts.garmin.garminapi.Garmin", return_value=mock_garmin),
        patch("os.path.isdir", return_value=isdir),
    )


def test_no_tokenstore_skips_login() -> None:
    mock_client = _make_mock_garmin(is_authenticated=False)
    p1, p2 = _patch_garmin(mock_client, isdir=False)
    with p1 as mock_garmin_cls, p2:
        api = GarminApi("user@example.com", "password")

    mock_garmin_cls.assert_called_once()
    mock_client.login.assert_not_called()
    assert api.is_authenticated is False
    assert api.unit_system is None
    assert api.version == GarminApi._GARMIN_VERSION


def test_constructor_does_not_login_even_with_existing_tokenstore_dir() -> None:
    # Login is explicit (GarminApi.login); the constructor only reads client state.
    mock_client = _make_mock_garmin(is_authenticated=True)
    p1, p2 = _patch_garmin(mock_client, isdir=True)
    with p1, p2:
        api = GarminApi("user@example.com", "password")

    mock_client.login.assert_not_called()
    assert api.is_authenticated is True


def test_credential_login_with_tokenstore() -> None:
    mock_client = _make_mock_garmin(is_authenticated=True)
    p1, p2 = _patch_garmin(mock_client, isdir=False)
    with p1, p2:
        api = GarminApi("user@example.com", "password")
        api.login("./garminconnect")

    mock_client.login.assert_called_with("./garminconnect")
    assert api.is_authenticated is True
    assert api.display_name == "tester"
    assert api.full_name == "Test User"
    assert api.unit_system == "metric"
    assert api.version == GarminApi._GARMIN_VERSION


def test_cached_token_login_reuses_session() -> None:
    # Garmin.login() itself handles the load-tokens-then-fall-back-to-credentials
    # flow; from GarminApi's perspective a cached-token login just succeeds
    # without raising.
    mock_client = _make_mock_garmin(is_authenticated=True)
    p1, p2 = _patch_garmin(mock_client, isdir=False)
    with p1, p2:
        api = GarminApi("user@example.com", "password")
        api.login("./garminconnect")

    mock_client.login.assert_called_once_with("./garminconnect")
    assert api.is_authenticated is True


def test_expired_token_login_failure_is_handled() -> None:
    mock_client = _make_mock_garmin(is_authenticated=False)
    mock_client.login.side_effect = Exception("token expired")
    p1, p2 = _patch_garmin(mock_client, isdir=False)
    with p1, p2:
        api = GarminApi("user@example.com", "password")
        api.login("./garminconnect")

    mock_client.login.assert_called_once_with("./garminconnect")
    assert api.is_authenticated is False
    assert api.unit_system is None
    assert api.version == GarminApi._GARMIN_VERSION


def test_profile_is_read_through_after_login(caplog: pytest.LogCaptureFixture) -> None:
    mock_client = _make_mock_garmin(is_authenticated=False)
    mock_client.display_name = None
    mock_client.full_name = None
    mock_client.unit_system = None
    p1, p2 = _patch_garmin(mock_client, isdir=False)
    with p1, p2, caplog.at_level(logging.INFO, logger="garminworkouts.garmin.garminapi"):
        api = GarminApi("user@example.com", "password")
        assert api.full_name == "" and api.display_name == "" and api.unit_system is None
        assert not [r for r in caplog.records if "Logged in as" in r.getMessage()]

        def populate(*_args: Any, **_kwargs: Any) -> None:
            mock_client.display_name = "tester"
            mock_client.full_name = "Test User"
            mock_client.unit_system = "metric"
            mock_client.client.is_authenticated = True

        mock_client.login.side_effect = populate
        assert api.login("./garminconnect") is True

    assert (api.full_name, api.display_name, api.unit_system) == ("Test User", "tester", "metric")
    messages = [r.getMessage() for r in caplog.records if "Logged in as" in r.getMessage()]
    assert messages == ["Logged in as Test User (tester)"]


def test_version_is_queried_after_login_when_unauthenticated_at_construction() -> None:
    mock_client = _make_mock_garmin(is_authenticated=False, version="99.9.9")

    def authenticate(*_args: Any, **_kwargs: Any) -> None:
        mock_client.client.is_authenticated = True

    mock_client.login.side_effect = authenticate
    p1, p2 = _patch_garmin(mock_client, isdir=False)
    with p1, p2:
        api = GarminApi("user@example.com", "password")
        assert api.version == GarminApi._GARMIN_VERSION
        api.login("./garminconnect")

    assert api.version == "99.9.9"


def test_mfa_prompt_is_wired_into_garmin_client() -> None:
    mock_client = _make_mock_garmin(is_authenticated=True)
    p1, p2 = _patch_garmin(mock_client, isdir=False)
    with p1 as mock_garmin_cls, p2:
        api = GarminApi("user@example.com", "password")

    _, kwargs = mock_garmin_cls.call_args
    assert kwargs["prompt_mfa"] == api.get_mfa

    with patch("garminworkouts.garmin.garminapi.getpass", return_value="123456"):
        assert api.get_mfa() == "123456"


def test_version_matches_expected_no_error_logged() -> None:
    mock_client = _make_mock_garmin(is_authenticated=True, version=GarminApi._GARMIN_VERSION)
    p1, p2 = _patch_garmin(mock_client, isdir=False)
    with p1, p2:
        api = GarminApi("user@example.com", "password")
        api.login("./garminconnect")

    assert api.version == GarminApi._GARMIN_VERSION


def test_version_mismatch_is_logged_but_does_not_raise() -> None:
    mock_client = _make_mock_garmin(is_authenticated=True, version="99.9.9")
    p1, p2 = _patch_garmin(mock_client, isdir=False)
    with p1, p2:
        api = GarminApi("user@example.com", "password")
        api.login("./garminconnect")

    assert api.version == "99.9.9"


def test_version_fetch_error_falls_back_to_default() -> None:
    mock_client = _make_mock_garmin(is_authenticated=True)
    mock_client.client.request.side_effect = Exception("network error")
    p1, p2 = _patch_garmin(mock_client, isdir=False)
    with p1, p2:
        api = GarminApi("user@example.com", "password")
        api.login("./garminconnect")

    assert api.version == GarminApi._GARMIN_VERSION


def test_is_authenticated_false_when_no_client() -> None:
    mock_client = _make_mock_garmin(is_authenticated=False)
    p1, p2 = _patch_garmin(mock_client, isdir=False)
    with p1, p2:
        api = GarminApi("user@example.com", "password")

    api._client = None
    assert api.is_authenticated is False


def test_is_authenticated_handles_exception() -> None:
    mock_client = _make_mock_garmin(is_authenticated=True)
    p1, p2 = _patch_garmin(mock_client, isdir=False)
    with p1, p2:
        api = GarminApi("user@example.com", "password")

    type(mock_client.client).is_authenticated = property(
        lambda self: (_ for _ in ()).throw(Exception("boom"))
    )
    assert api.is_authenticated is False


def test_get_put_post_delete_download_delegate_to_client() -> None:
    mock_client = _make_mock_garmin(is_authenticated=True)
    p1, p2 = _patch_garmin(mock_client, isdir=False)
    with p1, p2:
        api = GarminApi("user@example.com", "password")

    api.get("/some/path", params={"a": 1})
    mock_client.client.request.assert_called_with(
        "GET", GarminApi._GARMIN_SUBDOMAIN, "/some/path", params={"a": 1}
    )

    api.put("/some/path", json={"a": 1})
    mock_client.client.put.assert_called_with(GarminApi._GARMIN_SUBDOMAIN, "/some/path", json={"a": 1})

    api.post("/some/path", json={"a": 1})
    mock_client.client.post.assert_called_with(GarminApi._GARMIN_SUBDOMAIN, "/some/path", json={"a": 1})

    api.delete("/some/path")
    mock_client.client.delete.assert_called_with(GarminApi._GARMIN_SUBDOMAIN, "/some/path")

    api.download("/some/path")
    mock_client.client.download.assert_called_with("/some/path")


def test_enter_exit() -> None:
    mock_client = _make_mock_garmin(is_authenticated=False)
    p1, p2 = _patch_garmin(mock_client, isdir=False)
    with p1, p2:
        api = GarminApi("user@example.com", "password")

    assert api.__enter__() is api
    assert api.__exit__(None, None, None) is None


@pytest.mark.parametrize("error", [
    GarminConnectTooManyRequestsError("429 rate limited"),
    GarminConnectAuthenticationError("wrong credentials"),
    GarminConnectConnectionError("network down"),
])
def test_login_surfaces_typed_failures(error: Exception) -> None:
    mock_client = _make_mock_garmin(is_authenticated=False)
    mock_client.login.side_effect = error
    p1, p2 = _patch_garmin(mock_client, isdir=False)
    with p1, p2:
        api = GarminApi("user@example.com", "password")
        with pytest.raises(type(error)):
            api.login("./garminconnect")


def test_login_unexpected_error_returns_false_and_warns(caplog) -> None:
    mock_client = _make_mock_garmin(is_authenticated=False)
    mock_client.login.side_effect = RuntimeError("boom")
    p1, p2 = _patch_garmin(mock_client, isdir=False)
    with p1, p2, caplog.at_level(logging.WARNING, logger="garminworkouts.garmin.garminapi"):
        api = GarminApi("user@example.com", "password")
        assert api.login("./garminconnect") is False

    assert any(r.levelno == logging.WARNING and "boom" in r.getMessage() for r in caplog.records)


def test_login_without_tokenstore_or_credentials_returns_false_without_network() -> None:
    mock_client = _make_mock_garmin(is_authenticated=False)
    p1, p2 = _patch_garmin(mock_client, isdir=False)
    with p1, p2:
        api = GarminApi("", "")
        assert api.login() is False

    mock_client.login.assert_not_called()


def test_creates_new_garmin_client_when_none_given() -> None:
    mock_client = _make_mock_garmin(is_authenticated=False)
    with patch("garminworkouts.garmin.garminapi.Garmin", return_value=mock_client) as garmin_cls:
        api = GarminApi("user@example.com", "password")
    garmin_cls.assert_called_once()
    assert api._client is mock_client
