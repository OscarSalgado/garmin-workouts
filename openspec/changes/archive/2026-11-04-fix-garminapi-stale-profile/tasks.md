## 1. Implementation

- [x] 1.1 Replace the constructor copies of `full_name`, `display_name`, `unit_system` in `garminworkouts/garmin/garminapi.py` with read-through properties
- [x] 1.2 Extract `_refresh_version()` and call it from `__init__` (if authenticated) and after a successful `login()`
- [x] 1.3 Log "Logged in as ..." at the end of a successful `login()`; remove it from `__init__`

## 2. Tests

- [x] 2.1 Update `tests/platform/test_garminapi.py` for properties and post-login version/identity
- [x] 2.2 Add tests: profile populated after login, identity logged once after login and not at construction, version fallback on failure
- [x] 2.3 Run the full test suite and confirm no regressions
