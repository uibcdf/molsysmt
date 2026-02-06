# Digestion and Dependencies

## Argument Digestion (`arg_digest`)
- All public functions must validate inputs with `@arg_digest`.
- Place `@dep_digest` **below** `@arg_digest` so it works on normalized args.

## Dependency Policy
MolSysMT distinguishes **hard** vs **soft** dependencies:
- Hard: required for core functionality.
- Soft: optional features; must be lazily imported.

Rules:
- Never import soft dependencies at module top-level.
- Use `@dep_digest(library)` to guard optional functionality.
- Validate architecture with `scripts/validate_dependencies.py`.

## Single Source of Truth
Dependency status and form mapping live in `molsysmt/config/dependencies.py`.

## Maintenance
When moving a dependency from hard → soft:
1) Move imports inside functions.
2) Add `@dep_digest`.
3) Update `dependencies.py`.
4) Ensure form mapping exists.
