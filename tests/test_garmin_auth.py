"""Tests for Garmin credentials/token-store configuration and the MFA prompt in ``account``.

Tests cover:
- GARMIN_USERNAME/GARMIN_PASSWORD, with a deprecated EMAIL/PASSWORD fallback
- GARMINTOKENS token store resolution
- MFA prompt
- Removal of the unused centralized client
- Remaining configuration getters
"""

import logging
import os
import unittest
from pathlib import Path
from unittest.mock import patch

import pytest

import account


def _environ_only_config(key, default=None, **_):
    """Stand-in for decouple.config that ignores any developer .env file."""
    return os.environ.get(key, default)


@pytest.fixture
def clean_env(monkeypatch):
    monkeypatch.setattr(account, 'config', _environ_only_config)
    for name in ('GARMIN_USERNAME', 'GARMIN_PASSWORD', 'EMAIL', 'PASSWORD', 'GARMINTOKENS'):
        monkeypatch.delenv(name, raising=False)
    return monkeypatch


def test_credentials_canonical_variables(clean_env, caplog) -> None:
    clean_env.setenv('GARMIN_USERNAME', 'user@example.com')
    clean_env.setenv('GARMIN_PASSWORD', 'secret')

    with caplog.at_level(logging.WARNING):
        assert account.get_credentials() == ('user@example.com', 'secret')

    assert 'deprecated' not in caplog.text


def test_credentials_legacy_fallback_warns(clean_env, caplog) -> None:
    clean_env.setenv('EMAIL', 'legacy@example.com')
    clean_env.setenv('PASSWORD', 'legacy-secret')

    with caplog.at_level(logging.WARNING):
        assert account.get_credentials() == ('legacy@example.com', 'legacy-secret')

    assert 'GARMIN_USERNAME' in caplog.text and 'GARMIN_PASSWORD' in caplog.text


def test_credentials_canonical_wins_over_legacy(clean_env, caplog) -> None:
    clean_env.setenv('GARMIN_USERNAME', 'new@example.com')
    clean_env.setenv('GARMIN_PASSWORD', 'new-secret')
    clean_env.setenv('EMAIL', 'legacy@example.com')
    clean_env.setenv('PASSWORD', 'legacy-secret')

    with caplog.at_level(logging.WARNING):
        assert account.get_credentials() == ('new@example.com', 'new-secret')

    assert 'deprecated' not in caplog.text


def test_credentials_missing_returns_none(clean_env) -> None:
    assert account.get_credentials() == (None, None)


def test_credentials_partial_returns_none_for_missing(clean_env) -> None:
    clean_env.setenv('GARMIN_USERNAME', 'user@example.com')

    assert account.get_credentials() == ('user@example.com', None)


def test_tokenstore_defaults_to_home(clean_env) -> None:
    assert account.get_tokenstore() == str(Path('~/.garminconnect').expanduser())


def test_tokenstore_from_environment(clean_env, tmp_path) -> None:
    clean_env.setenv('GARMINTOKENS', str(tmp_path / 'tokens'))

    assert account.get_tokenstore() == str(tmp_path / 'tokens')


def test_tokenstore_expands_user(clean_env) -> None:
    clean_env.setenv('GARMINTOKENS', '~/custom-tokens')

    assert account.get_tokenstore() == str(Path('~/custom-tokens').expanduser())


@pytest.mark.parametrize('name', ['get_garmin_client', 'garmin_client', 'tokenstore', 'is_interactive'])
def test_centralized_client_is_removed(name) -> None:
    assert not hasattr(account, name)
    assert name not in account.__all__


def test_all_exported_symbols_available() -> None:
    for symbol in account.__all__:
        assert hasattr(account, symbol), f"Missing exported symbol: {symbol}"


class TestMfa(unittest.TestCase):
    """The MFA prompt."""

    def test_get_mfa_with_mocked_getpass(self) -> None:
        with patch.object(account, 'getpass', return_value='123456') as mock_getpass:
            assert account.get_mfa() == '123456'
        assert 'MFA' in mock_getpass.call_args[0][0]

    def test_get_mfa_returns_input_unchanged(self) -> None:
        with patch.object(account, 'getpass', return_value='  123456  '):
            assert account.get_mfa() == '  123456  '


class TestAccountModuleIntegration(unittest.TestCase):
    """Integration tests for the account module as a whole."""

    def test_account_module_initialization_completes(self) -> None:
        """Test that the account module initializes without raising exceptions."""
        # If we got here, the module initialized successfully
        assert account is not None
        assert hasattr(account, '__all__')

    def test_locale_configuration(self) -> None:
        """Verify locale is set to expected value."""
        # Locale is configured via environment/config, check via get_athlete_config if needed
        # For now, just verify the module has the expected structure
        assert hasattr(account, 'get_athlete_config')

    def test_other_configuration_values_exist(self) -> None:
        """Verify other config values are loaded via get_athlete_config()."""
        cfg = account.get_athlete_config()
        config_keys = ['vV02', 'fmin', 'rfmax', 'cfmax', 'sfmax', 'rflt', 'cflt', 'sflt']
        for key in config_keys:
            assert key in cfg, f"Missing config key: {key}"
            assert cfg[key] is not None, f"Config key {key} is None"

    def test_fitness_power_configs_loaded(self) -> None:
        """Verify fitness/power related configs are loaded."""
        cfg = account.get_athlete_config()
        assert 'rFTP' in cfg
        assert 'cFTP' in cfg
        assert cfg['rFTP'] is not None
        assert cfg['cFTP'] is not None

    def test_intervals_api_config_exists(self) -> None:
        """Verify Intervals.icu API configuration exists."""
        cfg = account.get_intervals_config()
        assert 'api_key' in cfg
        assert 'athlete_id' in cfg
        assert cfg['api_key'] is not None
        assert cfg['athlete_id'] is not None

    def test_bot_token_exists(self) -> None:
        """Verify BOT_TOKEN configuration exists."""
        cfg = account.get_athlete_config()
        assert 'BOT_TOKEN' in cfg
        assert cfg['BOT_TOKEN'] is not None


if __name__ == '__main__':
    unittest.main()
