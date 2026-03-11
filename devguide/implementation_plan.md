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
- upstream ArgDigest caller helpers were introduced for caller-sensitive digester
  logic (`argdigest.core.caller.*`) so downstream digesters can stop open-coding
  `caller.endswith(...)` guards;
- `float64` normalization at structural and PBC JIT boundaries;
- adapter fixes for `MDAnalysis.AtomGroup`, `StructuresDict`, `GRO`, `PDB`,
  AlphaFold/mmCIF, and OpenMM context conversion;
- a first `MolSysBuilder` slice now exists and is validated for
  `MolSysBuilder()` from scratch, `MolSys -> MolSysBuilder`, and
  `MolSysBuilder -> MolSys`;
- declared-state form coverage now includes `get`, `set`, `info`, and `select`
  for `molsysmt.MolSysBuilder`;
- deterministic builder-originated fixture coverage now backs PDB and H5MSM
  native converter tests, so those round-trips no longer need to discover truth
  from the serialized format itself;
- explicit topology editing is now intended to converge on
  `MolSysBuilder` / `molsysmt.build.editable(...)`, with `add_bonds`,
  `remove_bonds`, and `define_new_chain` entering the deprecation path for the
  `1.0` line.

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
- `tests/supported` ✅
- `pytest -q tests -x` ✅

## Next sessions

Immediate next steps:
1. define the explicit `1.0.0` support contract now that the suite is green;
2. classify peripheral or immature functionality that should remain outside the
   release contract even if tests exist;
3. prepare the next release checkpoint/tag from a contract-based perspective
   instead of a firefighting perspective.

Follow-up after the next validation checkpoint:
- review whether remaining warnings from third-party libraries should be
  documented, filtered, or simply tolerated;
- reassess coverage targets now that `.codecov.yml` includes core internal
  modules again; the current honest full-suite baseline is 51% with distributed
  coverage execution;
- keep the first builder slice narrow and stable before adding broader form
  adapters or serialization helpers;
- treat builder digestion as a first-class public-API requirement; the current
  builder slice now uses caller-sensitive digestion with small helper support
  added upstream in ArgDigest instead of bypassing `@arg_digest`;
- continue only with polish or contract-scope decisions, not broad
  stabilization rewrites.

## Tag semantics from `0.15.0` onward

`0.15.0` marks a change in how stabilization tags are interpreted in this
repository.

From this checkpoint onward:
- a stabilization tag should begin from a green full-suite state;
- support-contract discussions should happen after the suite is green, not as
  a substitute for getting it green;
- refactors that weaken support for peripheral or immature functionality must
  be evaluated explicitly against the intended `1.0.0` contract;
- the default assumption is now "regression until proven otherwise" for any
  post-`0.15.0` change touching core forms, native objects, diagnostics, or
  public element semantics.
