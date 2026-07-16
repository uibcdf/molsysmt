# Public API Surface and Stability

This document defines how the public surface is identified and how stability
claims are made. The dated, manually curated pre-1.0 classification is archived
under `archive/assessments/` because it cannot be kept authoritative without an
executable registry.

## What is public

The root public surface is the lazy registry `molsysmt._LAZY_ATTRIBUTES`, exposed
through `molsysmt.__getattr__()`. It currently includes namespaces, native
classes, core functions, warm-up helpers, and selected diagnostics.

Public namespace surfaces are defined by the non-private symbols intentionally
exported from their package `__init__.py` files. A symbol need not be copied into
the root registry to be public as `molsysmt.structure.<name>` or another public
namespace.

Modules under `molsysmt/_private` are internal. `molsysmt.third_party` is a
bridge implementation namespace and is not a stable user contract unless an
individual symbol is documented otherwise.

## Current stability evidence

The repository does not yet contain a machine-readable, release-approved
stability registry for every public symbol. Therefore:

- presence in an `__init__.py` establishes discoverability, not a promise of
  stability throughout the `1.x` line;
- a docstring `versionadded` directive records introduction, not maturity;
- form tiers classify adapter support, not function stability;
- tests demonstrate covered behavior, not an irrevocable compatibility policy.

Until the registry proposed in
`pending_proposals/machine_readable_api_stability_registry.md` exists, stability
must be stated narrowly in release notes or an explicitly approved public API
document. Do not label the entire current surface Stable by inference.

## Root compatibility points

The root registry currently exposes both `molsysmt.warmup()` and the deprecated
compatibility alias `molsysmt.warmup_numba()`. New documentation and code should
use `warmup()`.

Exceptions re-exported at the root are intended for user-side handling, but
their constructor details and catalog payloads still require compatibility
tests before stronger guarantees are made.

## Evolution rules

For a new or changed public function:

1. define the intended stability level and lifecycle impact;
2. follow adjacent naming, arguments, and return conventions;
3. use `@arg_digest` where public argument validation is appropriate;
4. do not decorate private helpers;
5. add behavioral and failure-path tests;
6. update docstrings, User Guide, Cookbook where relevant, and the Four Paths
   course as required by the repository lifecycle policy;
7. add deprecation before removing or breaking an established stable contract.

Not every public callable has the same decorator needs. Classes, predicates,
compatibility wrappers, and thin namespace helpers must follow their local
contract rather than a blanket “every public symbol is decorated” rule.

## Unsupported behavior

A public signature must not imply silent partial support. Unsupported engines,
forms, output types, or argument combinations should raise a catalog-backed,
typed exception with actionable context. Bare `NotImplementedError` remains
technical debt and should not be copied into new public paths.
