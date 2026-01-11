## 2026-01-10 — Dependency injection of HTTP session

**Decision**  
Inject a pre-configured `requests.Session` into the OpenWeather client functions,
rather than creating the session inside the client.

**Context**  
The extraction logic makes HTTP requests to external APIs. The code needs to:
- remain simple for local execution
- avoid hidden dependencies on global state
- be testable without making real HTTP calls
- support future enhancements (retries, backoff, headers, adapters)

**Decision rationale**  
Creating the HTTP session outside the client and passing it in explicitly:

- Keeps the client functions free of environment and configuration concerns
- Makes dependencies explicit at the call site
- Allows headers, adapters, and retry behaviour to be configured once
- Enables straightforward unit testing by injecting a mocked or fake session

This follows the principle that functions should depend on *what they need*,
not *where it comes from*.

**Alternatives considered**  
- Creating a `requests.Session` inside the client  
  Rejected because it hides dependencies, makes testing harder, and couples
  the client to specific configuration choices.

- Using `requests.get(...)` directly  
  Rejected because it prevents reuse of connections and makes future retry
  and transport-level concerns harder to introduce cleanly.

**Consequences**  
- Slightly more wiring in `main.py`
- Clear separation between orchestration and client logic
- A natural place to introduce retries, backoff, logging, or adapters later
  without changing the client interface

## 2026-01-11 — Configuration via Pydantic Settings

**Decision**  
Use Pydantic Settings to load and validate environment-based configuration
(API key, base URL, timeout).

**Why**  
- Avoid hard-coding secrets
- Fail fast on misconfiguration
- Keep client code free of environment concerns

**Alternatives considered**  
- Direct `os.environ` access (simpler, but less robust)
- Hard-coded constants (rejected)

**Consequences**  
- Adds a dependency on Pydantic
- Makes future Airflow / CI integration easier

## 2026-01-11 — Freeze scope at MVP and shift focus to testing

**Decision**  
Freeze the current implementation as a minimum viable product (MVP) and
pause further architectural expansion in order to focus on testing and
consolidation.

**Context**  
The initial design brief for this project was to create **simple Python
extraction logic** for fetching weather data from an external API. During
development, it became clear that the project could naturally expand into:

- multi-location and multi-date ingestion
- partitioned storage layouts
- retries with exponential backoff
- orchestration via Airflow
- external job specifications

While these directions are valid, pursuing them immediately risked
overcomplicating the code before the core extraction logic was proven and
understood.

**Decision rationale**  
Freezing the project at the current MVP stage:

- Keeps the implementation aligned with the original design brief
- Avoids premature abstraction and overengineering
- Establishes a stable baseline that can be reasoned about and tested
- Allows design decisions made so far to be validated through testing
- Creates a clear checkpoint before introducing additional complexity

At this stage, correctness, clarity, and confidence in behaviour are more
valuable than additional features.

**Next focus: testing**  
With a working MVP in place, the next priority is to introduce targeted tests,
including:

- Validation of configuration loading and failure modes
- Behaviour of the HTTP client under success and error conditions
- Verification that dependencies (e.g. injected session) are used correctly

This testing phase will help confirm that the current design choices are sound
before extending the system further.

**Alternatives considered**  
- Continuing immediately with retries, parameter builders, and partitioned
  storage  
  Rejected to avoid diluting focus and obscuring the learning goals of the
  exercise.

**Consequences**  
- Planned enhancements are explicitly deferred and tracked via GitHub Issues
- The codebase remains small, readable, and easy to reason about
- Future extensions can be made incrementally on top of a tested foundation