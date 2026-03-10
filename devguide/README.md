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
- the full test suite passes with `pytest -q tests -x`;
- the earlier sequential validation batches also passed independently for
  `tests/basic`, `tests/build`, `tests/form`, `tests/structure`,
  `tests/thirds`, `tests/topology`, `tests/native`, `tests/cross_repo`,
  `tests/hbonds`, `tests/molecular_mechanics`, `tests/pbc`,
  `tests/physchem`, and `tests/supported`;
- for broad validation work from this checkpoint onward, the default execution
  mode on the reference workstation is distributed `pytest-xdist`
  (`-n 12 --dist loadfile`) rather than fully sequential execution;
- the low-priority cleanup identified during the validation pass was closed:
  `show_contacts` no longer emits undigested-argument warnings for `style` and
  `show`, and `.codecov.yml` now tracks core `form`, `_private`, and `lib`
  modules again.

Current post-validation focus:
- decide what belongs to the explicit `1.0.0` support contract and what should
  remain outside that contract because it is still immature or peripheral;
- translate the green test state into a clear release checkpoint and support
  tier decision.

## Release checkpoint meaning: `0.15.0`

`0.15.0` is the first post-`0.14.0` stabilization checkpoint defined by a
green full-suite test state instead of partial confidence or local subsystem
confidence.

For development, this means:
- `0.15.0` starts from `pytest -q tests -x` passing cleanly in the reference
  environment;
- new work after `0.15.0` should be treated as regression-sensitive by
  default;
- any support-tier or API-contract reduction must be explicit and documented,
  not accidental fallout from refactors;
- future stabilization tags should be interpreted against this new baseline:
  a tag is not considered equivalent in quality unless it starts from a green
  suite or documents precisely why it does not.

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
