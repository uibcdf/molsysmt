# API Surface

## Public API Definition
The public API is defined by symbols imported in `molsysmt/__init__.py`.
Anything not imported there is considered internal.
Modules under `molsysmt/_private` are internal implementation details and must
not be re-exported.

## Required Decorators
- Public functions and methods **must** use `@arg_digest`.
- Internal helpers, especially under `molsysmt/_private`, **must not** use
  `@arg_digest`.

## Return Conventions
- Getter-style functions return **Python lists** (or lists of lists), not
  NumPy arrays, when returning collections.
- Single numeric values should be scalars (`int`, `float`, `str`) as
  appropriate.

## Naming and Signatures
Follow existing naming conventions in adjacent modules. When adding public
functions, keep argument names aligned with standard terms:
`molecular_system`, `selection`, `structure_indices`, `syntax`,
`skip_digestion`, `to_form`.

## Stability and Backward Compatibility
Public APIs are expected to remain stable across minor releases. Any breaking
changes must be documented in `devguide/roadmap.md` and announced in the
release notes.

## Not Implemented Policy (1.0-RC)
Public APIs must not silently expose partial behavior.

- If a parameter combination is not implemented, raise a typed exception
  (`NotImplementedMethodError`) with `caller` and an actionable message.
- Do not document unimplemented behavior as available.
- If backward-compatible aliases are supported (for example, old argument
  names), normalize them explicitly and document which name is canonical.
- For 1.0-RC triage:
  - `must-fix`: gaps that break advertised behavior in public API docs.
  - `documented-not-supported`: behavior that is intentionally deferred and
    explicitly documented as not implemented.
