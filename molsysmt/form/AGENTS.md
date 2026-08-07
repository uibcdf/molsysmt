# Form Converters Agents Guide

This guide is for agents and contributors working on form adapters under `molsysmt/form`.
It refines the global rules in the repository root `AGENTS.md` for this subtree.

## Language and style

- Keep all comments and docstrings in English.
- Follow NumPy-style docstrings and the conventions in `coding/coding_guide.md`.
- The first line of a docstring should be a short gerund summary (for example, “Converting MolSys to ViewerJSON.”).
- Document units explicitly for physical quantities.

## Form module structure

- Every form package (for example, `file_pdb`, `molsysmt_MolSys`, `molsysmt_ViewerJSON`) must expose at least:
  - `form_name`
  - `form_type`
  - `form_info`
  - `piped_topological_attribute`
  - `piped_structural_attribute`
  - `piped_any_attribute`
  - `bonds_are_explicit`
  - `bonds_can_be_computed`
  - `is_form`, `attributes`, `has_attribute`
  - Public API functions such as `get`, `set`, `extract`, `copy`, `add`, `merge`, `append_structures`, iterators, and converter functions, as appropriate for the form.
- Each `__init__.py` must define a `_convert_to` dictionary mapping target form names (strings) to callable converters, plus any `_conversion_opt_kwargs` when optional kwargs are supported.
- Keep imports and `__all__` aligned with the existing pattern in neighboring form modules.
- The piping metadata is part of the form contract and must be reviewed for every new or modified form:
  - `piped_topological_attribute`: preferred target form when several topological attributes will be extracted from this form.
  - `piped_structural_attribute`: preferred target form when several structural attributes will be extracted from this form.
  - `piped_any_attribute`: preferred target form when mixed topological and structural extraction is expected and one shared conversion is cheaper than two separate conversions.
- Set a pipe to `None` only when repeated direct getters are already the cheapest and most stable path.
- Pipe targets must be valid form names accepted by `molsysmt.convert`. Do not use non-existent forms or singular/plural typos.
- Do not overwrite piping metadata later in the same `__init__.py`. Legacy duplicate assignments silently disable the optimization path.
- When a form rebuilds topology or structures internally for individual `get_*` helpers, it is a strong signal that piping should be configured.
- When choosing between a specific pipe and `piped_any_attribute`, prefer the most reduced stable target:
  - use a topology form for topological-only bulk extraction,
  - use a structures form for structural-only bulk extraction,
  - use a full `molsysmt.MolSys` pipe only when mixed extraction really benefits from it.
- If a form exposes both individual getters and an efficient conversion path, keep both:
  - the getters remain part of the public adapter surface,
  - high-level bulk consumers such as `molsysmt.get`, `molsysmt.compare`, and `molsysmt.info` rely on the piping metadata to avoid repeated expensive reconstructions.
- In practice, piping matters most for high-level APIs that request many attributes in one call:
  - direct consumers: `molsysmt.get` and `molsysmt.compare`,
  - indirect consumers through `molsysmt.get`: `molsysmt.info`, `molsysmt.get_label`, `molsysmt.contains`, `molsysmt.is_composed_of`, and selection backends that build expressions from repeated attribute queries.
- `molsysmt.select` itself usually does not need special piping support because its direct form-level accesses are typically single-attribute lookups (`n_*`, `*_index`, `inner_bond_index`). Optimize the form metadata for bulk attribute extraction first; do not add select-specific complexity unless profiling proves a real bottleneck.

## Converters and validation

- Public conversion, get, extract, set and iterator functions should use the `@arg_digest` decorator from `molsysmt._private.argdigest` for argument validation.
- Private helpers (including functions in modules named `_private` or clearly internal utilities) must **not** be decorated with `@arg_digest`.
- Prefer composing converters instead of duplicating logic:
  - For example, conversions from `molsysmt.MolSys` to JSON forms should be built by combining the topology and structures converters rather than re-implementing them.
  - When a path already exists (A → B and B → C), prefer using those converters rather than implementing A → C from scratch unless there is a strong reason.

## Attributes, shapes, and units

- Use standard attribute names and shapes:
  - Coordinates: arrays with shape `(n_structures, n_atoms, 3)` (or `(n_frames, n_atoms, 3)` in iterators); units: nanometers.
  - Box: arrays with shape `(n_structures, 3, 3)`; lengths in nanometers, angles handled in radians when derived.
  - Time: arrays in picoseconds.
  - Charges: expressed in units of the elementary charge.
- Respect default behaviors for `selection` and `structure_indices` as described in `dev_guide.md` and `coding/coding_guide.md`.
- When introducing or modifying JSON-like forms (for example, `molsysmt.ViewerJSON`), keep their schema consistent with the corresponding native classes and clearly document units in their docstrings.

## Tests

- When adding or changing converters, update or add tests under `tests/form` in the mirrored path (for example, changes in `molsysmt/form/molsysmt_ViewerJSON` should be accompanied by tests under `tests/form/molsysmt_ViewerJSON`).
- Keep tests deterministic and reasonably fast; prefer bundled systems from `molsysmt.systems` and small synthetic examples where appropriate.
- Tests for converters should check:
  - Types of returned objects.
  - Shapes and units of key attributes (coordinates, box, time).
  - Integrity of topology (numbers of atoms, bonds, groups, etc.).

## Safety and evolution

- Do not change existing `form_name` strings or public keys in schemas without carefully evaluating downstream impact and tests.
- When extending forms, prefer additive changes and maintain backward-compatible behavior unless the change is explicitly intended as a breaking change and is coordinated with tests and documentation.
- Keep the conversion graph coherent: avoid introducing cycles or ambiguous paths that bypass established, tested converters without necessity.
