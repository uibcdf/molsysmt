"""
MolSysMT Developer Guide — Devtools and CI
"""

# Devtools and CI

## Devtools
Developer utilities live under `devtools/` and `scripts/`. Use these for
validation, build tasks, and maintenance workflows.

## CI Expectations
- Tests run with `pytest`.
- Push/PR gating runs on Ubuntu with Python 3.13 (fast tier).
- Full test matrix runs weekly (scheduled) and on manual dispatch:
  Ubuntu + macOS, Python 3.10 through 3.13.
- Documentation builds must not introduce warnings.
- Optional dependencies must be guarded and skipped when unavailable.
- The repository keeps two skip mechanisms:
  - `paths-ignore` for docs-only changes.
  - explicit `[skip ci]` in commit/PR metadata for exceptional cases.

## Validation Scripts
- `scripts/validate_dependencies.py` must pass before release.
- `scripts/validate_resources.py` must pass before release.
