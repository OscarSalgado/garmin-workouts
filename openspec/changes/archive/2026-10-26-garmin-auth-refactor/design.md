## Context

Currently, Garmin authentication is split:
- Credentials (email/password) are loaded in `account.py` from environment variables
- Client initialization and token management happens in `garminapi.py`
- Token caching uses a `./garminconnect` directory that's managed implicitly

This makes it difficult to mock authentication in tests, reason about the auth flow, and ensure tokens persist correctly across application instances.

## Goals / Non-Goals

**Goals:**
- Centralize Garmin client creation in `account.py` as a module-level singleton
- Provide a clean `garmin_client` import point for the rest of the application
- Maintain token persistence using python-garminconnect's built-in caching
- Preserve MFA support for interactive authentication
- Ensure backward compatibility with existing code that uses `GarminApi`

**Non-Goals:**
- Change the MFA implementation (stays interactive via `input()`)
- Add OAuth or alternative auth methods
- Migrate existing production tokens
- Integrate with Intervals.icu's auth system

## Decisions

**1. Module-level singleton in account.py**
- Create `garmin_client` as a module-level variable initialized on import
- Rationale: Simplest pattern for Python, avoids circular imports, single point of truth
- Alternative considered: Lazy initialization function (adds complexity without benefit for this use case)

**2. Token storage location**
- Use `./.garminworkouts-cache/garmin` as the token store directory
- Rationale: Isolates Garmin tokens from other caches, avoids cluttering root directory, explicit naming
- Alternative: `./garminconnect` (current) - less explicit, could conflict with other tools

**3. GarminApi refactoring approach**
- Keep `GarminApi` class but make it use `garmin_client` internally
- Rationale: Minimizes changes to calling code, easier gradual migration
- Alternative: Deprecate `GarminApi` entirely (too aggressive for one change)

**4. Error handling**
- If authentication fails during module import, log error but don't crash
- Rationale: Allows tests/CLI commands to run without requiring interactive login
- Precedent: Current code already does this in `garminapi.py`

## Risks / Trade-offs

- **[Risk] Circular imports** → Design account.py imports to be minimal; GarminApi will depend on account.py's `garmin_client`
- **[Risk] Test isolation** → Tests that import account.py will try to authenticate unless we mock credentials early
  → Mitigation: Use pytest fixtures that patch `decouple.config` before account.py is imported
- **[Risk] Token persistence across app restarts** → If tokenstore path changes, old tokens are lost
  → Mitigation: Document the path in .env.example and warn in changelog
- **[Trade-off] Module-level side effects** → Importing account.py triggers authentication attempt
  → Accepted because: Current code already does this, and non-interactive environments skip login
