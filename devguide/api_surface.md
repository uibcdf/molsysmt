# Public API Surface and Stability

This document defines how the public surface is identified and how stability
claims are made. The normative classification is the machine-readable registry
in `devtools/data/public_api_stability.json`; its generated human-readable view
is `api_stability_registry.md`.

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

## Normative stability contract

Every export in the root lazy registry and the release-contract namespaces is
classified as `stable`, `experimental`, or `outside-contract`. The registry is
validated against source code with the Python AST, without importing MolSysMT
or optional dependencies. CI fails when an export is added without a decision,
when a registered export disappears, or when the generated table is stale.

The exact member inventories currently tracked are `molsysmt`, `basic`,
`structure`, `build`, `pbc`, `physchem`, `topology`, `hbonds`, and
`molecular_mechanics`. Other root namespaces have an explicit subtree policy:
their members inherit the namespace's Experimental or Outside-contract status
until that namespace is promoted into exact member tracking.

`pre-1.0` in the introduction field means that the symbol was already present
during pre-release development and that no trustworthy finer-grained public
release provenance exists. It is not an inferred maturity claim.

Presence in an `__init__.py`, a docstring `versionadded` directive, form tier,
or test suite still does not establish stability on its own. Only the registry
does. A previous registry can be passed to the validator as a baseline; Stable
symbols cannot be demoted or removed and deprecated lifecycle state cannot be
silently reverted.

## Root compatibility points

Numerical kernels are already compiled in the installed Rust extension. The
pre-1.0 JIT warm-up helpers were removed with the JIT runtime; ordinary Python
imports remain the explicit mechanism for applications that want eager module
loading.

Exceptions re-exported at the root are Stable user-side handling points. Their
catalog prose may improve, but their import paths and intended exception roles
belong to the `1.x` compatibility contract.

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
