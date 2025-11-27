# MolSysMT Repository Agents Guide

This document defines global rules for automated agents and human contributors working on the MolSysMT repository.
More specific `AGENTS.md` files in subdirectories refine or override these rules within their scope.

## Scope

- This file applies to every file in the repository unless a more specific `AGENTS.md` in a subdirectory states otherwise.
- When rules conflict, the more local `AGENTS.md` wins; this root file remains the global baseline.

## Language and documentation

- All repository-facing text must be written in English: code comments, docstrings, error/warning messages, READMEs, guides, developer notes, notebooks, and all `AGENTS.md` files.
- User-facing conversations (issues, PR reviews, interactive assistant replies) may follow the user’s preferred language, but anything committed to the repo stays in English.
- Follow the documentation conventions in `dev_guide.md`, `coding/coding_guide.md`, and the documentation-specific AGENTS under `docs/` and `docs/dev/`.
- For web documentation (User Guide, Showcase, Cookbook, developer docs), use MyST and cross-linking patterns described in `docs/content/developer/documentation/web/` (notably `references.md`).

## Public vs private API

- Public functions and methods (imported in package `__init__` modules or intended for users) should use the `@digest` decorator from `molsysmt._private.digestion` for argument validation.
- Private helpers, especially anything under `molsysmt/_private`, must **not** use `@digest`. Keep them small, focused, and internal.
- Do not expose `_private` modules in public APIs.
- When adding new public functions, ensure they follow existing naming, argument, and return-value conventions in adjacent modules.

## Docstrings and style

- Use NumPy-style docstrings as illustrated in `coding/coding_guide.md`.
- First line: short gerund summary (for example, “Getting box lengths and angles.”).
- Always document units for physical quantities (coordinates in nm, time in ps, angles in radians, charges in elementary charge units).
- Prefer doctest-friendly examples where appropriate, but keep them short and focused.
- Keep comments and docstrings meaningful; avoid restating information that is obvious from the code.

## Data conventions

- Coordinates: NumPy arrays with shape `(n_structures, n_atoms, 3)` (or `(n_frames, n_atoms, 3)` for iterators); units: nanometers.
- Box: NumPy arrays with shape `(n_structures, 3, 3)`; lengths in nanometers, angles handled in radians when derived.
- Time: arrays in picoseconds.
- Charges: expressed in units of the elementary charge.
- Respect the invariants described in `dev_guide.md` for `Get`, `Iterator`, `Form`, and `Native` behavior.

## Forms and conversions

- Form adapters live under `molsysmt/form`; see `molsysmt/form/AGENTS.md` for detailed guidance.
- Each form module should declare `form_name`, `form_type`, `form_info`, and populate `_convert_to` with callables instead of hard-coding conversion graphs.
- Prefer composing existing converters (for example, combining topology and structures converters) rather than re-implementing duplicate logic.
- Keep attribute names and array shapes consistent across forms (coordinates, box, time, topology attributes, etc.).

## Testing and validation

- Use `pytest` for tests; follow the structure and conventions documented in `tests/AGENTS.md`.
- Place tests in the mirrored path under `tests/` corresponding to the package area you change.
- Keep tests deterministic and reasonably fast; rely on bundled systems in `molsysmt.systems` and small fixtures when possible.
- When changing behavior, update or add tests to capture the intended semantics instead of weakening existing expectations.

## Safety and tooling

- Prefer minimal, focused changes that respect the existing architecture and style.
- Do not run or document destructive git commands (such as `git reset --hard` or `git push --force`) in automated workflows.
- Avoid adding new external dependencies without considering their impact; reuse existing libraries and utilities already in the project when possible.
- Automated agents must respect sandboxing and should avoid network access unless explicitly required and permitted by the execution environment.

For more specialized guidance, consult the AGENTS files in `ai_assistant/`, `docs/`, `docs/dev/`, `coding/`, `molsysmt/form/`, and `tests/`.
