# Implementation Plan

This document summarizes current implementation priorities and phased work.
It consolidates and refines `ROADMAP.md` for developer execution.

## Phase 1 — Core Stability (1.0 Candidate)
- API stability for public functions.
- Documentation coverage for public API.
- Tests ≥ 75% coverage with stable expectations.

## Phase 2 — Ecosystem Integration
- Viewer ecosystem alignment (MolSysViewer/NGLView).
- Dependency metadata integration into API docs.

## Phase 3 — Performance and Diagnostics
- Maintain lightweight import strategy.
- Improve JIT warmup ergonomics and reporting.
- Expand SMonitor catalog coverage.

## Current stabilization checkpoint (March 2026)

The current implementation pass is centered on broad validation and targeted
hardening. The architecture-level refactors planned for the `1.0.0` path are
already in place; the remaining work is now dominated by validation-driven bug
fixes and small contract clarifications.

Completed in the current pass:
- native/public separation for rebuild and element query semantics;
- H5MSM support for `b_factor`, including regeneration of `181l.h5msm`;
- deterministic offline coverage for `nglview` color-by-value workflows;
- structured diagnostics adoption with `smonitor.integrations.context_extra(...)`;
- `float64` normalization at structural and PBC JIT boundaries;
- adapter fixes for `MDAnalysis.AtomGroup`, `StructuresDict`, `GRO`, `PDB`,
  AlphaFold/mmCIF, and OpenMM context conversion.

Sequential validation status:
- `tests/basic` ✅
- `tests/build` ✅
- `tests/form` ✅
- `tests/structure` ✅
- `tests/thirds` ✅
- `tests/topology` ✅
- `tests/native` ✅
- `tests/cross_repo` ✅
- `tests/hbonds` ✅
- `tests/molecular_mechanics` ✅
- `tests/pbc` ✅
- `tests/physchem` ✅

## Next sessions

Immediate next steps:
1. run `tests/supported`;
2. if that passes, make a new broad status checkpoint and reassess the actual
   remaining failing surface;
3. return to the pending low-priority cleanup:
   - `argdigest` warnings still emitted by `show_contacts`;
   - `.codecov.yml` cleanup so core modules are no longer excluded from
     coverage accounting.

Follow-up after the next validation checkpoint:
- run another targeted audit of any remaining failing top-level test groups;
- decide whether additional offline fixture hardening is needed;
- only then continue with secondary polish work.
