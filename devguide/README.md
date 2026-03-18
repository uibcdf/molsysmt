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
- structural and PBC hot paths now use explicit kernel-facing preparation where
  needed, without changing the user-facing unit policy of the public API;
- a first `MolSysBuilder` slice is implemented and validated for creation from
  scratch, `MolSys -> MolSysBuilder`, and `MolSysBuilder -> MolSys`;
- `molsysmt.build.editable(...)` now provides the ergonomic entrypoint for
  editing an existing molecular system through the builder.
- declared-state form coverage now exists for `MolSysBuilder` through `get`,
  `set`, `info`, and `select`.
- the first declarative serializer slice is now implemented:
  `molsysmt.MolSysDict`, `molsysmt.TopologyDict`, `file:molsys_yaml`, and `file:topology_yaml` are available, with focused
  round-trip tests and supported-form coverage.
- the structure hot-path audit clarified that `molsysmt.lib.structure` kernels
  are unit-agnostic and should receive prepared numeric arrays without forcing
  a canonical unit such as `nm`;
- local helpers under `molsysmt.lib.structure._kernel_inputs` now centralize
  coordinate rank normalization and paired-input alignment for hot structure
  wrappers;
- this work now sits cleanly on top of PyUnitWizard's expanded extraction API
  (`value_type`, `dtype`) instead of overloading generic public digestion.
- a first lightweight benchmark harness now exists in `benchmarks/` and the
  initial `XYZ` baseline confirms that `_kernel_inputs` is not the dominant
  cost in hot structure wrappers.
- comprehensive test suites are now in place for the two primary topology
  interoperability forms:
  - `mdtraj.Topology`: 384 tests against the standard reference molecular system
    (builder fixture) + 15 PDB oracle tests against `1l2y.pdb` (Trp-cage);
  - `openmm.Topology`: 393 builder tests + 15 PDB oracle tests using the same
    oracle and reference system;
  - this work required fixing multiple latent bugs in both adapters — the full
    bug inventory is recorded in `testing_form_adapters.md`;
- all missing `get_total_n_*` scalar-returning aggregation functions were added
  to the `openmm.Topology` adapter (~97 functions);
- the `devtools/tests/Makefile` `coverage-top` target was updated to always
  print depth=0 (whole-package total) before the user-requested depth.
- `string:pdb_id` and `string:alphafold_id` promoted to Tier 1; identity-converter
  import bugs fixed in their `to_openmm_Topology`, `to_openmm_PDBFile`, and
  `to_mdtraj_Topology` converters;
- `file:bcif` and `file:bcif.gz` topological getter stubs filled (342 functions
  each), enabling `select()`, `get()`, and `Iterator()` on these forms;
- `file:dcd` now implements `get_n_atoms_from_system` by reading the binary header,
  allowing `is_a_molecular_system()` to correctly detect incompatible pairing;
- `Topology.extract()` now correctly reindexes `groups['component_index']` when
  that column is present, fixing `infer_molecule_types_from_topology` after `remove()`;
- pytest mark system introduced: `tier1 / tier2 / tier3 / network / redundant /
  peptide_parity`; tier marks auto-applied from `FORM_TIERS` via `conftest.py` hook;
  `MSM_RUN_EXTENDED_PEPTIDE_PARITY` env var replaced by `@pytest.mark.peptide_parity`;
- `devtools/tests/Makefile` now includes `DOCTEST_DIR` so `molsysmt/basic/` doctests
  are always part of `make test` and `make coverage`, and excludes `peptide_parity`
  by default;

Validation status at this checkpoint:
- the full test suite passes with `pytest -q tests -x`;
- the earlier sequential validation batches also passed independently for
  `tests/basic`, `tests/build`, `tests/form`, `tests/structure`,
  `tests/thirds`, `tests/topology`, `tests/native`, `tests/cross_repo`,
  `tests/hbonds`, `tests/molecular_mechanics`, `tests/pbc`,
  `tests/physchem`, and `tests/supported`;
- `tests/form/mdtraj_Topology` (399 tests) and `tests/form/openmm_Topology`
  (408 tests) now pass cleanly as part of the `tests/form` batch;
- for broad validation work from this checkpoint onward, the default execution
  mode on the reference workstation is distributed `pytest-xdist`
  (`-n 12 --dist loadfile`) rather than fully sequential execution;
- the low-priority cleanup identified during the validation pass was closed:
  `show_contacts` no longer emits undigested-argument warnings for `style` and
  `show`, and `.codecov.yml` now tracks core `form`, `_private`, and `lib`
  modules again.
- `molsysmt.molecular_dynamics` remains in the repository but is explicitly outside the `1.0.0` support contract;
- local and Codecov coverage baselines intentionally exclude `molsysmt/molecular_dynamics/**` until that area is promoted into a supported post-1.0 line.
- overall test coverage is approximately 62% at this checkpoint (target: 70-80%
  on the Tier 1 surface before `1.0.0`).

Current post-validation focus:
- continue hardening Tier 1 form adapter test coverage;
  the next target form adapter should be selected based on coverage hotspots
  in `tests/form` (run `make coverage-hotspots SUBPACKAGE=molsysmt.form` from
  `devtools/tests`);
- decide what belongs to the explicit `1.0.0` support contract and what should
  remain outside that contract because it is still immature or peripheral;
- translate the green test state into a clear release checkpoint and support
  tier decision;
- treat the current split between public `get()` and
  `molsysmt.lib.structure._kernel_inputs` as sufficient for `1.0.0`, while
  keeping a lighter internal retrieval path as a post-`1.0.0` optimization only
  if real workflows justify it;
- avoid future drift by centralizing shared kernel-input normalization rules if
  multiple domains begin to duplicate them after `1.0.0`.

## Release checkpoint meaning: `0.15.0`, `0.16.0`, and `0.17.0`

`0.15.0` is the first post-`0.14.0` stabilization checkpoint defined by a
green full-suite test state instead of partial confidence or local subsystem
confidence.

`0.16.0` is the first post-`0.15.0` feature checkpoint that keeps that green
full-suite baseline while adding a new native editable form (`MolSysBuilder`)
and the first deterministic builder-based converter fixtures.

`0.17.0` should capture the first declarative-serialization checkpoint built on
top of that builder work:
- `MolSysDict`, `TopologyDict`, and `StructuresDict`;
- YAML-backed declarative file forms discovered by content;
- direct `MolSysBuilder <-> MolSysDict` declared-state conversion;
- removal of the legacy public topology-editing helpers in `molsysmt.build`.

For development, this means:
- `0.15.0` starts from `pytest -q tests -x` passing cleanly in the reference
  environment;
- `0.16.0` keeps that full-suite-green baseline while extending the core data
  model with `MolSysBuilder`;
- `0.17.0` keeps that same baseline while adding the first declarative forms
  and consolidating explicit topology editing on `MolSysBuilder`;
- new work after `0.15.0` should be treated as regression-sensitive by
  default;
- any support-tier or API-contract reduction must be explicit and documented,
  not accidental fallout from refactors;
- future stabilization tags should be interpreted against this new baseline:
  a tag is not considered equivalent in quality unless it starts from a green
  suite or documents precisely why it does not.

## Recommended Reading Order
1) `competitive_landscape_and_vision.md` (Strategic vision: strengths, gaps, and targets vs mdtraj/MDAnalysis)
2) `1.0.0_maturity_audit.md` (Technical depth audit)
3) `1.0.0_road_to_excellence.md` (Strategic weaknesses and path to 1.0)
4) `next_steps_toward_1_0.md` (Ordered remaining work toward 1.0.0)
6) `support_tiers.ipynb` (Form classification — notebook has live tier query from `form_tier.py`)
7) `digestion_and_dependencies.md` (Lazy Loading & ArgDigest policies)
8) `forms_and_conversions.md` (Graph conversion rules)
9) `viewers_and_visualization.md` (Visual backend policy)
10) `architecture.md`
11) `element_and_native_rebuild.md`
12) `molsys_builder.md`
13) `declarative_serialization_forms.md`
14) `api_surface.md`
15) `testing_strategy.md`
16) `testing_form_adapters.md`
17) `devtools_and_ci.md` (Local test/coverage toolbox and planned CI)
18) `scalability_and_heavy_trajectories_v2.md` (Pre-1.0.0 heavy trajectory design)
19) `smonitor_feedback_proposals.md` (Temporary diagnostic improvements under evaluation)

## Scope
These documents define how MolSysMT should be implemented and maintained:
API boundaries, data conventions, forms, dependency rules, diagnostics, and
performance strategy. User-facing documentation lives under `docs/`, but must
follow this guidance.
