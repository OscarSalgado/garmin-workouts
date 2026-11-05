"""IntervalsAPI against a real local HTTP server: timeouts and retries."""
import time

import pytest
import requests
from werkzeug.wrappers import Response

from intervalsicu.intervals.api import IntervalsAPI


@pytest.fixture
def api() -> IntervalsAPI:
    client = IntervalsAPI("ath", "key", timeout=(1, 0.5))
    # keep the backoff negligible so retry tests stay fast
    for adapter in client.session.adapters.values():
        adapter.max_retries.backoff_factor = 0
    return client


def test_read_timeout_raises_within_the_bound(httpserver, api) -> None:
    def slow(_request):
        time.sleep(2)
        return Response("late")

    httpserver.expect_request("/slow").respond_with_handler(slow)
    start = time.monotonic()
    with pytest.raises(requests.Timeout):
        api.get(httpserver.url_for("/slow"))
    assert time.monotonic() - start < 1.9


def test_rate_limited_once_then_succeeds(httpserver, api) -> None:
    httpserver.expect_ordered_request("/r").respond_with_data("", status=429, headers={"Retry-After": "0"})
    httpserver.expect_ordered_request("/r").respond_with_json({"ok": True})
    response = api.get(httpserver.url_for("/r"))
    assert response.status_code == 200 and response.json() == {"ok": True}


def test_persistent_server_error_fails_after_last_retry(httpserver, api) -> None:
    httpserver.expect_request("/e").respond_with_data("", status=503)
    response = api.get(httpserver.url_for("/e"))
    assert response.status_code == 503
    assert len(httpserver.log) == 4  # first attempt + 3 retries
    with pytest.raises(requests.HTTPError):
        response.raise_for_status()


def test_post_is_not_replayed(httpserver, api) -> None:
    httpserver.expect_request("/p", method="POST").respond_with_data("", status=503)
    assert api.post(httpserver.url_for("/p"), json={}).status_code == 503
    assert len(httpserver.log) == 1
