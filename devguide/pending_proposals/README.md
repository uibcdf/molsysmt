# Pending Proposals

This directory contains work that has not been accepted as part of the current
MolSysMT contract. A proposal may be technically detailed without being approved,
implemented, benchmarked, or scientifically validated.

Before implementation, check the proposal against current code and dependency
versions: proposals are intentionally allowed to age. Record a decision, define
acceptance criteria, and migrate durable rules into normative documents when the
work is completed.

`native_dcd_reader_rust_study_and_plan.md` is the concrete engineering study for a
MolSysMT-owned DCD reader and writer, written on 2026-08-03 at the maintainer's
request. It carries no approval to start: the go/no-go criteria remain those of
`rusterization_parallel_trajectory_io.md` and `native_format_parsers_post_1_0.md`.

Reading MDAnalysis's independent implementation alongside the VMD-derived one used by
MDTraj and Biotite turned up two disagreements that affect MolSysMT **today**: only
MDAnalysis interprets the newer CHARMM box-matrix unit cell, and the two libraries
produce time axes differing by the AKMA-to-picosecond factor from the same file.

The governing idea is section 7.0: the goal is not another DCD parser but a backend
shaped like the `file:dcd` adapter's own surface. Every getter of that form currently
decodes the whole trajectory, so counting frames costs as much as reading them and
asking for one structure costs twice as much as asking for all of them. Phase 0 should
therefore be run on its own merit — it separates adapter cost from parser cost and may
find a defect in the current adapter, whether or not any Rust is ever written.

Large architectural proposals should begin with a small evidence-gathering phase
and must not weaken dependency policy, lifecycle integrity, diagnostics, or the
scientific-validation requirements.

## Generated index

Entries carrying front matter under
[reporting_protocol.md](../reporting_protocol.md) are listed here automatically.

<!-- generated: devguide_index -->

### Open (8)

- [`add_an_explicit_source_form_hint_to_convert.md`](add_an_explicit_source_form_hint_to_convert.md) — [#151](https://github.com/uibcdf/molsysmt/issues/151) — Add an explicit source-form hint to convert. *(inspected)*
- [`adopt_pyunitwizard_fast_paths_at_quantity_boundaries.md`](adopt_pyunitwizard_fast_paths_at_quantity_boundaries.md) — [#155](https://github.com/uibcdf/molsysmt/issues/155) — Audit PyUnitWizard fast-path adoption at quantity boundaries. *(inspected)*
- [`convert_np_int64_scalar_integers_to_native_python_ints_in_returned_lists_and_set.md`](convert_np_int64_scalar_integers_to_native_python_ints_in_returned_lists_and_set.md) — [#165](https://github.com/uibcdf/molsysmt/issues/165) — convert np.int64 scalar integers to native python ints in returned lists and sets *(asserted)*
- [`evaluate_deprecation_or_removal_of_define_new_chain_in_favor_of_msm_build_editab.md`](evaluate_deprecation_or_removal_of_define_new_chain_in_favor_of_msm_build_editab.md) — [#167](https://github.com/uibcdf/molsysmt/issues/167) — evaluate deprecation or removal of define_new_chain in favor of msm.build.editable *(asserted)*
- [`evaluate_if_msm_topology_add_bonds_is_redundant_given_msm_build_editable.md`](evaluate_if_msm_topology_add_bonds_is_redundant_given_msm_build_editable.md) — [#166](https://github.com/uibcdf/molsysmt/issues/166) — evaluate if msm.topology.add_bonds is redundant given msm.build.editable *(asserted)*
- [`evaluate_single_assessment_delegation_for_public_molecular_system_predicates.md`](evaluate_single_assessment_delegation_for_public_molecular_system_predicates.md) — [#154](https://github.com/uibcdf/molsysmt/issues/154) — Evaluate single-assessment delegation for public molecular-system predicates *(measured)*
- [`extend_the_catalog_warning_round_trip_guard_to_every_warning_class.md`](extend_the_catalog_warning_round_trip_guard_to_every_warning_class.md) — [#161](https://github.com/uibcdf/molsysmt/issues/161) — Extend the catalog-warning round-trip guard to every warning class *(reproduced)*
- [`shared_reporting_vocabulary_across_molsyssuite.md`](shared_reporting_vocabulary_across_molsyssuite.md) — [#156](https://github.com/uibcdf/molsysmt/issues/156) — A reporting vocabulary every MolSysSuite tool can adopt unchanged. *(measured)*

<!-- /generated -->

## Triage map

**Hand-written, and temporary.** These entries predate the reporting protocol and are
recorded in `devtools/data/devguide_migration_baseline.json` as awaiting front matter
and an issue. As each is migrated it moves into the generated index above and its line
here is removed. Until that is finished this map is the only complete list, which is
exactly the duplication the protocol removes -- it is tolerated only while the
migration is in flight.


### Reliability and contract work

- `release_1_0_execution_plan.md` — authoritative ordering guide for restoring
  conversion fidelity, productizing the Rust extension, removing Numba before
  1.0, completing documentation lifecycle work, and running the release gates.
- `technical_and_scientific_quality_improvement_program.md` — umbrella quality
  plan for the codebase, dependencies, documentation, and scientific validation.
- `docs/README.md` — index and triage of pending documentation proposals.
- `documentation_lifecycle_manifest.md` — API-to-doc/course traceability.
- `catalog_diagnostics_migration.md` — risk-ranked diagnostics cleanup.
- `benchmark_regression_gate_reliability.md` — statistically credible gates.
- `conversion_fidelity_and_molsysdict_v1.md` — executable Tier 1 conversion
  fidelity and a versioned path beyond the MolSysDict 0.1 boundary; the gate is
  operational and remaining non-exhaustive routes are explicit baseline debt.

### Scientific and ecosystem requests

- `trajectory_projection_onto_principal_components.md` — explicit per-frame
  projection onto a fitted PCA basis without confusing scores with eigenvectors.
- `chemical_metadata_preservation_sdf_mol2.md`
- `proposal_protor_atom_typing_and_radii.md`
- `topomt_requested_spatial_helpers_and_sasa.md` — Part 1 (configurable
  `probe_radius` / `n_sphere_points`) done; Part 2 (grid helpers) pending.
- `sasa_methodologies_and_acceleration_post_1_0.md` — cell-list acceleration and
  alternative SASA methodologies (LCPO, Lee–Richards).
- `molsysviewer_molsysmt_nonblocking_heavy_operations.md`

### Exploratory architecture and operations

- `attribute_centric_molecular_system_model.md` — proposed attribute-
  centric extension of the native model for a rigorous bond contract, optional
  interaction datasets, and future reactive chemical states.
- `topology_selection_indexing_and_pyarrow.md` — immediate selection
  optimization and a separate Arrow-dtype feasibility study.
- `optional_native_columns_memory_model.md` — post-1.0 evaluation of
  schema-aware optional physical columns so topology memory scales with the
  information an instance actually contains.
- `rust_gpu_backend_options.md` — whether the Rust layer should also target the GPU.
  The landscape survey is still live post-1.0 work. Its near-term framing is
  settled: the default Rust wheel is CPU-only and Numba-CUDA has been removed, so
  any future GPU surface must pass its own scientific and failure-contract audit.
- `rusterization_hybrid_columnar_ecs_arrow_graph_engine.md`
- `rusterization_parallel_trajectory_io.md`
- `rusterization_topology_and_selections.md`
- `pyunitwizard_global_standards_conflict.md`
- `smonitor_feedback.md`
- `git_history_bloat_cleanup.md`

### Presentation, documentation, and citation

- `readme_positioning_and_1_0_refresh.md` — how MolSysMT presents itself. Accepted
  and largely applied: the README and documentation landing pages described a
  converter and a removed Numba/CUDA architecture, understated the supported
  surface, and carried code examples that did not execute.
- `migration_off_the_in_house_publication_actions.md` — two independent decisions:
  publishing the documentation through GitHub's native Pages deployment instead of a
  `gh-pages` branch of 1907 site snapshots, and building the conda packages on a runner
  per platform instead of relabelling one Linux build. The second is blocking for 1.0;
  the first is not, and removes `contents: write` from a workflow.
- `presentation_and_citation_surface.md` — partially resolved on 2026-08-07. The
  authorship question is decided and the misattributed ORCID is gone with it, and
  the duplicate landing page is deleted. Two items remain: the stale, malformed DOI
  and version in `CITATION.cff`, and the timing of the installation instructions
  against the Conda delivery track.

### Education

- `course_review/` — unresolved retrospective course improvements. This one is not a
  queue: it is outside the reporting protocol by design, and its documents carry no front
  matter and no issue. See
  [reporting_protocol.md](../reporting_protocol.md) for why, and split anything accepted
  out of it into ordinary entries here.

This index is organizational only. Priority comes from evidence, scientific
risk, effort, and an explicit maintainer decision. Proposals marked exploratory
or partially superseded must be re-scoped before implementation.

## Closed and moved out of this directory

Archived on 2026-08-07 under `../archive/resolved_proposals/`:

- `atom_axis_add_semantic_audit.md` and its evidence
  `atom_axis_add_phase1_findings.md` — **completed** through all four phases. The
  audit found the scope narrower than assumed, two of its own premises wrong, and a
  defect it had not anticipated; its seven decisions are implemented and its contract
  now lives in [`native_structures_contract.md`](../native_structures_contract.md).
  All ten acceptance criteria are walked in the archived document. One finding left
  the audit and stayed open on its own:
  [`archive/resolved_bugs/public_functions_silently_ignore_unknown_keywords.md`](../archive/resolved_bugs/public_functions_silently_ignore_unknown_keywords.md).

Archived on 2026-07-28 under `../archive/resolved_proposals/`, with a resolution
note on each:

- `rust_numba_coexistence_and_cut_plan.md` — **completed.** The cut is done; there
  is no coexistence left to manage.
- `rusterization_pilot_conclusions_and_adoption.md` — **historical pilot evidence.**
  Its measurements explain the decision; its recommendations are contradicted by
  shipped work.
- `conda_numba_preheating.md` — **withdrawn.** It preheated a JIT that no longer
  exists, through a `warmup()` API that has been removed.
- `triclinic_cell_list_completeness.md` — **resolved**, implemented and validated in
  `rust/src/neighbors.rs` and `rust/src/sasa.rs`.

Archived on 2026-07-29 after F2 closure and F3 lifecycle reconciliation:

- `explicit_form_support_registry.md` — **completed.** Every discovered form is
  explicitly classified and the release validator rejects implicit support.
- `course_module_renumbering_scheme.md` — **completed.** F1 implemented the
  20-module Core, Paths 21–54, stable labels, manifest, and validator.
- `rust_packaging_backend_design.md` — **completed.** The accepted
  setuptools-rust private-extension design passed C1–C7.
- `linear_algebra_backend_for_rust_kernels.md` — **completed.** The Rust-only
  runtime uses `nalgebra` and `faer` and passed its scientific and packaging
  gates.
- `chemical_graph_and_conversion_execution_checkpoint.md` — **completed.** The
  fixed pre-1.0 chemical-graph consolidation block is implemented.
- `chemical_state_v1_executable_contract.md` — **completed.** The accepted
  reference-state and normalized chemical-state contract is implemented for
  the 1.0 scope.
- `chemical_state_adapter_fidelity_audit.md` — **completed.** Priority inbound,
  outbound, strict-loss, and persistence adapter seams are implemented; broader
  lower-tier expansion remains deferred.
- `neighbor_list_consumer_migration.md` — **completed.** Common threshold and
  h-bond consumer paths use the shared primitive; residual modes remain on the
  matrix path by explicit design.
- `rusterization_heavy_computations.md` — **completed and superseded.** The
  exploration led to the Rust-only runtime and no longer defines future work.
- `rust_migration_documentation_and_test_residue.md` — **completed.** The
  dihedral broadcast contract is tested on both paths, archived records resolve,
  and Rust source documentation describes the production Rust-only runtime.

A proposal is archived, never deleted. If one of these questions returns it will
return with a different premise and deserves a fresh document rather than a
revived one.
