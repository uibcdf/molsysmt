# Architecture

## Purpose
MolSysMT is a modular Python library for describing, transforming, and
analyzing molecular systems. It provides a uniform API across multiple
external engines and file formats while enforcing consistent data models.

## High-Level Layout
```
molsysmt/
  basic/           # High-level public API (get, set, convert, select, view)
  form/            # Adapters for external forms and files (lazy discovery)
  element/         # Element-level operations (atom/group/component/etc.)
  structure/       # Geometry and structural tools
  lib/             # Performance kernels (Numba, math, pbc, structure)
  native/          # Native objects and default units
  pbc/             # Periodic boundary condition tools
  build/           # Topology construction and fixes
  hbonds/          # Hydrogen-bond analysis
  thirds/          # Optional integrations and third-party bridges
  systems/         # Bundled reference systems for tests/docs
  _private/        # Internal helpers (not public API)
```

## Public vs Private
- Public API is what is imported from `molsysmt/__init__.py`.
- Anything under `molsysmt/_private` is internal and must not be re-exported.
- Public functions must use `@arg_digest` for argument validation.

## Data Flow
Typical execution pipeline:
1) Public API entrypoint (e.g., `molsysmt.basic.get`).
2) Argument digestion and validation (`arg_digest`).
3) Form conversion or attribute extraction.
4) Core computation (element/structure/lib).
5) Consistent output format (lists, shapes, units).

## Element vs Native Rebuild

MolSysMT distinguishes between two related but different concerns:

- `molsysmt.element`: public, form-agnostic query helpers.
- `molsysmt.native`: native reconstruction and inference over `Topology` and `MolSys`.

Public element helpers may use dispatch, `get()`, `select()`, and conversion
machinery. Native rebuild workflows must not. Native rebuild code must operate
directly on native topology tables and native helpers in
`molsysmt/native/_hierarchy.py`.

See `element_and_native_rebuild.md`.

## Performance Layer
`molsysmt/lib` contains performance-critical kernels. These kernels use
Numba and are compiled lazily to keep `import molsysmt` fast. See
`performance_and_jit.md`.

## Diagnostics
All warnings and errors must be emitted through SMonitor catalogs. See
`smonitor_integration.md`.
