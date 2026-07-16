# Error and Warning Policy

Maintained public paths should use the catalog-backed classes and helpers in
`molsysmt._private.smonitor`. Legacy deviations do not establish precedent.

## Choosing a failure

- Use a specific argument exception for invalid choices, lengths, conflicts,
  shapes, units, or types.
- Use capability/conversion exceptions for unsupported forms, engines,
  syntaxes, methods, or routes.
- Use structural or algorithm errors when accepted molecular data violate an
  invariant or computation cannot produce a scientifically valid result.
- Preserve the original exception with chaining when translating an external
  dependency failure.

Example:

```python
raise ArgumentChoiceError(
    argument="element",
    value=element,
    choices=["atom", "group"],
    caller="molsysmt.example",
)
```

Do not introduce new bare `Exception`, `NotImplementedError`, `ValueError`, or
hardcoded warning strings on public paths when a domain exception exists.

## Predicates and probes

`is_form`, `is_item`, `is_quantity`, and similar probes return `False` for a
normal non-match. They may report that outcome at debug level. Malformed data
after a positive identification, dependency failures, and internal defects must
not be swallowed as `False`.

## Recoverable behavior

A warning is appropriate only when the operation can still return a valid,
well-defined result. The warning must state the fallback, scientific impact, or
user action. If validity or alignment is uncertain, fail instead.

## Structured context

Follow the catalog signal contract. Prefer stable context fields such as
`caller`, `operation`, `form`, `engine`, `backend`, `argument`, and original
cause. Avoid embedding all context only in prose.

## Migration rule

When touching a legacy path with `print`, bare exceptions, or silent fallback,
migrate the affected branch and add a regression test when this can be done
without expanding the requested change materially. Broader migration belongs in
an explicit proposal and should be prioritized by public/scientific risk.
