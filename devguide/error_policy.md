"""
MolSysMT Developer Guide — Error and Warning Policy
"""

# Error and Warning Policy

## Single Source of Truth
All diagnostics must emit through SMonitor catalogs. Do not hardcode warning
or error messages in code paths.

## Argument Errors
Use specific subclasses for argument validation issues to provide richer feedback:

- `ArgumentChoiceError`: When a value is not in the allowed set of choices.
- `ArgumentLengthError`: When list/array lengths do not match expected dimensions.
- `ArgumentConflictError`: When mutually exclusive arguments are provided.

Example:
```python
raise ArgumentChoiceError(
    argument="element",
    value=element,
    choices=["atom", "group"],
    caller="my_func"
)
```

## Exceptions
All custom exceptions must inherit from `smonitor.integrations.CatalogException` (or a local wrapper). 
They should define a `catalog_key` that matches an entry in `molsysmt/_private/smonitor/catalog.py`.

Example:
```python
class ArgumentError(MolSysMTCatalogException):
    catalog_key = "ArgumentError"
```

## Warning Categories
Warnings should inherit from `smonitor.integrations.CatalogWarning`. Use the `warn` or `warn_once` helpers from `molsysmt._private.smonitor` to emit them.

## Probing Policy (Form/Type Detection)
Exploratory checks such as `is_form`, `is_item`, `is_quantity`, and `is_unit`
must behave as predicates:

- A non-matching candidate is an expected outcome and must return `False`.
- Expected probe misses must not surface as `ERROR` in user-facing profiles.
- Probe misses may be emitted as `DEBUG` for developer telemetry.
- `WARNING` and `ERROR` are reserved for actionable anomalies and real failures.

This policy applies across the MolSysSuite stack (`molsysmt`, `pyunitwizard`,
`argdigest`, `depdigest`, and `smonitor`) to avoid noisy diagnostics during
normal detection paths.

## Required Extras
Follow `SIGNALS` contracts in `molsysmt/_private/smonitor/catalog.py`.
