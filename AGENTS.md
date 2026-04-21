# MolSysMT Repository Agents Guide

This document defines global rules for automated agents and human contributors working on the MolSysMT repository.
More specific `AGENTS.md` files in subdirectories refine or override these rules within their scope.

## Scope

- This file applies to every file in the repository unless a more specific `AGENTS.md` in a subdirectory states otherwise.
- When rules conflict, the more local `AGENTS.md` wins; this root file remains the global baseline.

## Language and documentation

- All repository-facing text must be written in English: code comments, docstrings, error/warning messages, READMEs, guides, developer notes, notebooks, and all `AGENTS.md` files.
- User-facing conversations (issues, PR reviews, interactive assistant replies) may follow the user’s preferred language, but anything committed to the repo stays in English.
- Follow the documentation conventions in `devguide/`, `coding/coding_guide.md`, and the documentation-specific AGENTS under `docs/`.
- For web documentation (User Guide, Showcase, Cookbook, developer docs), use MyST and cross-linking patterns described in `docs/content/developer/documentation/web/` (notably `references.md`).
- **Lifecycle Integrity:** Any change or addition to the public API is considered incomplete until: (1) Docstrings are updated and pass doctests, (2) the **User Guide** (Foundations, Toolbox, and Cookbook) reflects the new behavior, and (3) the corresponding modules of **'The Four Paths of the MolSysMT's Master'** course are verified and updated. Documentation is treated as code; it must be accurate and functional.

## Public vs private API

- Public functions and methods (imported in package `__init__` modules or intended for users) should use the `@digest` decorator from `molsysmt._private.digestion` for argument validation.
- Private helpers, especially anything under `molsysmt/_private`, must **not** use `@digest`. Keep them small, focused, and internal.
- Do not expose `_private` modules in public APIs.
- When adding new public functions, ensure they follow existing naming, argument, and return-value conventions in adjacent modules.

## Docstrings and style

- Use NumPy-style docstrings (see `coding/coding_guide.md` and `docs/content/developer/documentation/api/docstrings.md`) with a gerund one-line summary.
- Standard order: summary; optional extended description; Parameters; Returns (single section); Raises; Notes; See Also; Examples (doctest `>>>`); tutorial admonition; `.. versionadded::`.
- Types in lowercase; defaults in the description; reuse standard wording for `molecular_system`, `selection`, `structure_indices`, `syntax`, `skip_digestion`, `to_form`; document units (nm, ps, radians, elementary charge) where applicable.
- Examples must be minimal and deterministic, using bundled systems; avoid duplicating heavy test logic.
- Keep comments/docstrings meaningful; avoid restating obvious code behavior.

## Data conventions

- Coordinates: NumPy arrays with shape `(n_structures, n_atoms, 3)` (or `(n_frames, n_atoms, 3)` for iterators); units: nanometers.
- Box: NumPy arrays with shape `(n_structures, 3, 3)`; lengths in nanometers, angles handled in radians when derived.
- Time: arrays in picoseconds.
- Charges: expressed in units of the elementary charge.
- Respect the invariants described in `dev_guide.md` for `Get`, `Iterator`, `Form`, and `Native` behavior.

## Dependency Management

## Dependency Management
- **Hard vs Soft Dependencies:** MolSysMT distinguishes between essential libraries (Hard) and optional feature-enabling ones (Soft). This status is centrally managed in `molsysmt/_depdigest.py`.
- **Lazy Imports:** Never import a soft dependency (e.g., `mdtraj`, `openmm`, `MDAnalysis`, `parmed`, `pytraj`, `nglview`, `pdbfixer`, `biopython`, `plotly`) at the module's top level. Always perform imports inside functions or methods.
- **Enforcement:** Use the `@dep_digest(library, when=None)` decorator from the `depdigest` package (configured by `molsysmt/_depdigest.py`) to enforce dependency availability and provide metadata for introspection.
- **Validation:** Run `devtools/scripts/validate_dependencies.py` to ensure no top-level imports of soft dependencies leak into the codebase. Exempt zones (tests, dev tools) are defined in the script and documented in `SPEC_DEPENDENCIES.md`.

## Forms and conversions

- Form adapters live under `molsysmt/form`; see `molsysmt/form/AGENTS.md` for detailed guidance.
- Discovery and registration are lazy and dynamic. They rely on the central mapping in `molsysmt/_depdigest.py` (specifically `MAPPING`). Do not add dependency-related variables to the form's local `__init__.py`.
- Each form module should declare `form_name`, `form_type`, `form_info`, and populate `_convert_to` with callables.
- Respect `msm.config.show_all_capabilities` which allows users to filter available forms based on their installed environment.


## Performance Architecture

- **Normalization Passports**: Use `ValidatedPayload` from `argdigest` for internal high-frequency calls to bypass redundant unit and shape validation.
- **Fast-Track Units**: Register canonical units (nm, ps, Da, K) in `puw.fast_track` within `molsysmt/_pyunitwizard.py` to enable instant unit bypass.
- **Chunked Execution**: Large trajectories must be processed via the `ChunkedExecutor` (see `devguide/scalability_and_heavy_trajectories_v2.md`).

## Testing and validation

- Use `pytest` for tests; follow the structure and conventions documented in `tests/AGENTS.md`.
- Place tests in the mirrored path under `tests/` corresponding to the package area you change.
- Keep tests deterministic and reasonably fast; rely on bundled systems in `molsysmt.systems` and small fixtures when possible.
- When changing behavior, update or add tests to capture the intended semantics instead of weakening existing expectations.

## Git commits

- Never add a `Co-Authored-By` trailer to commit messages. Commit messages must contain only the subject line and, when necessary, a body — no attribution footers of any kind.
- Always include `[skip ci]` in the commit message unless explicitly instructed otherwise.

## Safety and tooling

- Prefer minimal, focused changes that respect the existing architecture and style.
- Do not run or document destructive git commands (such as `git reset --hard` or `git push --force`) in automated workflows.
- Avoid adding new external dependencies without considering their impact; reuse existing libraries and utilities already in the project when possible.
- Automated agents must respect sandboxing and should avoid network access unless explicitly required and permitted by the execution environment.
- In native MolSysMT objects (for example, `molsysmt.Topology` and `molsysmt.MolSys`), element IDs (`*_id` fields) are stored as strings; normalize incoming numeric IDs to strings and keep this invariant in converters, rebuilders, and tests.

For more specialized guidance, consult the AGENTS files in `ai_assistant/`, `docs/`, `coding/`, `molsysmt/form/`, and `tests/`.

## External Tooling Guides (Required for Development)

These guides are required reading for anyone developing this library. They describe how external tools must be used here.

- `SMONITOR_GUIDE.md` — Required guide for SMonitor integration and diagnostics.
- `ARGDIGEST_GUIDE.md` — Required guide for argument validation and the ValidatedPayload (Passport) protocol.
- `PYUNITWIZARD_GUIDE.md` — Required guide for unit management and Fast-Track conversion registration.
- `DEPDIGEST_GUIDE.md` — Required guide for dependency management and lazy loading.
