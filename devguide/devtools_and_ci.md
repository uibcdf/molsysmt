"""
MolSysMT Developer Guide — Devtools and CI
"""

# Devtools and CI

## Devtools
Developer utilities live under `devtools/` and `scripts/`. Use these for
validation, build tasks, and maintenance workflows.

## CI Expectations
- Tests run with `pytest`.
- Documentation builds must not introduce warnings.
- Optional dependencies must be guarded and skipped when unavailable.

## Validation Scripts
- `scripts/validate_dependencies.py` must pass before release.
