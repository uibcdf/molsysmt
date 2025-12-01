# Coding Agents Guide

This guide is for agents and contributors editing Python code, forms, or
infrastructure scripts in this repository. It refines the global rules from
the root `AGENTS.md` for coding-related work.

## Language and documentation

- Comments, docstrings, and user-facing strings stored in the repository must be written in English.
- Follow the conventions described in `dev_guide.md` and `coding/coding_guide.md`.
- Docstrings should follow NumPy-style with a gerund one-line summary (for example, “Getting box lengths and angles.”).
- Always include units for physical quantities (nm, ps, radians, elementary charge) where applicable and keep only a single `Returns` block.

## Public vs private code and `@digest`

- Public functions (part of the user-facing API, imported in `__init__.py` modules, or clearly referenced in docs) should be decorated with `@digest` from `molsysmt._private.digestion` for argument validation.
- Private helpers, especially those under `molsysmt/_private` or in modules explicitly marked as internal, must **not** use `@digest`.
- Do not expose `_private` modules in public APIs.

## Data shapes and units

- Respect the standard shapes and conventions:
  - Coordinates: `numpy.ndarray` with shape `(n_structures, n_atoms, 3)` (or `(n_frames, n_atoms, 3)` for iterators); units: nanometers.
  - Box: `numpy.ndarray` with shape `(n_structures, 3, 3)`; lengths in nanometers, angles handled in radians when derived.
  - Time: arrays in picoseconds.
  - Charges: expressed in units of the elementary charge.
- Honor defaults for `selection` and `structure_indices` as described in `coding/coding_guide.md` and `dev_guide.md`.

## Forms and conversions

- When working with form adapters (`molsysmt/form`), follow the additional guidance in `molsysmt/form/AGENTS.md`.
- Prefer using the centralized form registry and existing converters instead of duplicating conversion paths.
- Reuse existing helpers for selections, units, PBC utilities, and topology operations whenever possible.

## Testing and maintenance

- Use `pytest` for tests; place them under `tests/` mirroring the package structure.
- When behavior changes, add or adjust tests accordingly, keeping runtime modest and relying on bundled systems from `molsysmt.systems` or small fixtures.
- Reuse shared fixtures defined in `tests/conftest.py` instead of creating one-off molecular systems inside tests; add new reusable systems there unless a test intentionally exercises online conversion or detection flows.
- Prefer incremental, focused changes; avoid large refactors unless explicitly requested and well-justified.
- In native MolSysMT objects (`molsysmt.Topology`, `molsysmt.MolSys`), element IDs (`atom_id`, `group_id`, `component_id`, `molecule_id`, `chain_id`, `entity_id`) must be stored as strings. Normalize any incoming numeric IDs in converters and rebuilders and keep tests aligned with this invariant.
- Getter-style functions (including `molsysmt.basic.get` and element-specific getters) must return Python lists for collections (lists of lists when nested), not NumPy arrays, to keep outputs consistent across forms and examples.

## Safety and dependencies

- Avoid introducing new external dependencies or modifying packaging/CI configuration (for example, `pyproject.toml`, `setup.cfg`, GitHub Actions workflows) unless explicitly requested.
- Do not add or document destructive git commands in code or tooling.
- Respect any execution and sandboxing constraints when suggesting or running scripts.
