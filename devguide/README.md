# MolSysMT Developer Guide

This folder is the single source of truth for developer-facing conventions,
invariants, and internal policies in MolSysMT. Other files (for example,
`docs/content/developer/*`, `README.md`, and tutorials) must
align with these rules. If conflicts exist, **`devguide/` takes precedence**.

## Recommended Reading Order
1) `architecture.md`
2) `api_surface.md`
3) `data_model.md`
4) `forms_and_conversions.md`
5) `digestion_and_dependencies.md`
6) `smonitor_integration.md`
7) `performance_and_jit.md`
8) `testing_strategy.md`
9) `documentation_sync.md`
10) `implementation_plan.md`
11) `roadmap.md`

## Scope
These documents define how MolSysMT should be implemented and maintained:
API boundaries, data conventions, forms, dependency rules, diagnostics, and
performance strategy. User-facing documentation lives under `docs/`, but must
follow this guidance.

## Canonical Inputs
The following files are authoritative inputs that this devguide consolidates:
- `AGENTS.md`
- `coding/coding_guide.md`
- `SPEC_DEPENDENCIES.md`
- `SMONITOR_GUIDE.md`
- `ROADMAP.md`
- `molsysmt/_argdigest.py` and `molsysmt/_depdigest.py`
- `docs/content/developer/*` (curated user-facing versions)
