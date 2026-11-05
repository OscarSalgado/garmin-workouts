# Tasks

## 1. Session with timeout and retries

- [x] 1.1 Create a `requests.Session` in `IntervalsApi.__init__` with the auth headers and a mounted `HTTPAdapter`
  using `urllib3.util.Retry(total=3, backoff_factor=1, status_forcelist=(429, 500, 502, 503, 504),
  respect_retry_after_header=True)`. Verify: unit test inspects the mounted adapter's retry settings.
- [x] 1.2 Route `get/post/put/delete/patch` through the session with `kwargs.setdefault("timeout", self.timeout)`
  (default `(5, 30)`). Verify: test with a mocked session asserts `timeout=(5, 30)` is passed and can be overridden.
- [x] 1.3 Close the session in `__exit__`. Verify: test asserts `session.close()` is called when used as a context
  manager.

## 2. Consistent error handling

- [x] 2.1 Use a checked helper (raise on non-2xx) in methods that call `.json()` without checking the status.
  Verify: test with a 500 response raises `requests.HTTPError` instead of a JSON decode error.
- [x] 2.2 Replace f-string log calls in `api.py` with `%s` arguments. Verify: `ruff check --select G004
  intervalsicu` is clean.

## 3. Guardrail

- [x] 3.1 Remove `S113` from the global ruff ignore list and fix or justify any remaining findings.
  Verify: `ruff check --select S113 .` reports nothing.
- [x] 3.2 Integration test with `pytest-httpserver`: a server that sleeps longer than the read timeout makes the
  call raise `requests.Timeout` within the timeout; a server answering 429 then 200 succeeds after one retry.
