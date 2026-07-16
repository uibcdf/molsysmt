# Diagnostics Contract

SMonitor is the preferred structured diagnostics layer for MolSysMT. The
catalog, exception classes, warning classes, and emitters live under
`molsysmt/_private/smonitor`, with package configuration in
`molsysmt/_smonitor.py`.

This is a target contract, not a claim that all legacy paths have migrated.
Direct `print`, standard warnings, bare exceptions, and swallowed emission
failures still exist and must be treated as technical debt.

## Severity

- `DEBUG`: expected probes, internal decision context, and development detail;
- `INFO`: relevant successful execution decisions or progress;
- `WARNING`: recoverable behavior that may affect cost, fidelity, or outcome;
- `ERROR`: a failure that prevents the requested result.

An expected form/type probe miss returns `False` and must not appear as a
user-facing error. A caught scientific failure is not a probe miss.

## Catalog use

- Reuse a suitable catalog entry before adding a new one.
- Keep code, message template, severity, hints, and required `extra` fields
  coherent.
- Use catalog-backed exception and warning classes on maintained public paths.
- Include `caller`, operation, form/backend, and scientifically relevant context
  when the signal contract supports them.
- Never let telemetry failure replace or hide the original scientific error.

`warn()` and `warn_once()` centralize emission. Python's `warnings.warn()` is
acceptable when emitting a catalog-backed warning instance if that is the local
tested pattern; hardcoded strings and `print("Warning...")` are not equivalent.

## Failure integrity

- Do not use `except Exception: pass` around diagnostics, import warm-up, or
  scientific execution without a narrowly justified fallback.
- Do not downgrade arbitrary reducer or converter exceptions into corrupt-input
  warnings.
- Fallback must preserve the original cause and make any fidelity change
  observable.
- Success signals must be emitted only after the operation has produced a valid
  result.

## Validation

Tests should assert exception/warning category, code or catalog key, actionable
message, and required structured context. Catalog validation does not prove
that every code path uses the catalog; migration requires source checks and
behavioral tests.

See `error_policy.md`, `SMONITOR_GUIDE.md`, and the confirmed diagnostic defects
under `pending_bugs/`.
