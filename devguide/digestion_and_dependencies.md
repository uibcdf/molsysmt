# Digestion and Dependencies

## Argument Digestion (`arg_digest`)
- All public functions must validate inputs with `@arg_digest`.
- The ArgDigest configuration lives in `molsysmt/_argdigest.py`.
- Place `@dep_digest` **below** `@arg_digest` so it works on normalized args.
- For quantity strings, digesters must parse with `puw.parse.parse(...)`
  (not `puw.parse(...)`), following the current PyUnitWizard API layout.

Key configuration fields:
- `DIGESTION_SOURCE`
- `DIGESTION_STYLE`
- `STANDARDIZER`
- `STRICTNESS`
- `SKIP_PARAM`

## Dependency Policy
MolSysMT distinguishes **hard** vs **soft** dependencies:
- Hard: required for core functionality.
- Soft: optional features; must be lazily imported.

Rules:
- Never import soft dependencies at module top-level.
- Use `@dep_digest(library)` to guard optional functionality.
- Validate architecture with `scripts/validate_dependencies.py`.

## Single Source of Truth
Dependency status and form mapping live in `molsysmt/_depdigest.py`.

Key configuration fields:
- `LIBRARIES` (hard vs soft)
- `MAPPING` (form directory → library)
- `SHOW_ALL_CAPABILITIES`
- `EXCEPTION_CLASS`

## Maintenance
When moving a dependency from hard → soft:
1) Move imports inside functions.
2) Add `@dep_digest`.
3) Update `_depdigest.py`.
4) Ensure form mapping exists.
