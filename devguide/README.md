# MolSysMT Developer Guide

This folder is the single source of truth for developer-facing conventions,
invariants, and internal policies in MolSysMT. Other files (for example,
`docs/content/developer/*`, `README.md`, and tutorials) must
align with these rules. If conflicts exist, **`devguide/` takes precedence**.

## Current checkpoint (March 2026)

The current stabilization pass is focused on finishing the path to `1.0.0`
with broad sequential validation and targeted fixes instead of architectural
rewrites.

Recent completed work:
- native rebuild and public `molsysmt.element` semantics were separated and documented;
- H5MSM now preserves `b_factor` and the bundled `181l.h5msm` artifact was regenerated;
- `nglview` round-trips and color-by-value tests were made deterministic offline;
- `smonitor` and MolSysMT diagnostics were hardened for developer and QA workflows;
- structural and PBC JIT call sites were normalized to `float64` at the public boundary.

Validation status at this checkpoint:
- broad sequential test batches already pass for `tests/basic`, `tests/build`,
  `tests/form`, `tests/structure`, `tests/thirds`, `tests/topology`,
  `tests/native`, `tests/cross_repo`, `tests/hbonds`,
  `tests/molecular_mechanics`, `tests/pbc`, and `tests/physchem`;
- the next validation slice to resume is `tests/supported`;
- low-priority cleanup still pending includes a few `argdigest` warnings
  (for example in `show_contacts`) and the pending `.codecov.yml` adjustment.

## Recommended Reading Order
1) `1.0.0_maturity_audit.md` (Current state and roadmap)
2) `support_tiers.md` (Form classification)
3) `digestion_and_dependencies.md` (Lazy Loading & ArgDigest policies)
4) `forms_and_conversions.md` (Graph conversion rules)
5) `viewers_and_visualization.md` (Visual backend policy)
6) `architecture.md`
7) `element_and_native_rebuild.md`
8) `api_surface.md`
9) `testing_strategy.md`
10) `smonitor_feedback_proposals.md` (Temporary diagnostic improvements under evaluation)

## Scope
These documents define how MolSysMT should be implemented and maintained:
API boundaries, data conventions, forms, dependency rules, diagnostics, and
performance strategy. User-facing documentation lives under `docs/`, but must
follow this guidance.
