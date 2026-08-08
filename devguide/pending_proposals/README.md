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

## Triage map

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
- `declared_selection_syntaxes_without_implementation.md` — seven syntaxes are
  declared and four of fourteen `(syntax, direction)` cells work; `MDAnalysis`
  is documented as available but reachable only from PDB files and MDAnalysis
  objects. Raised from MolSysViewer, which re-promises the same list.

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
- `private_api_in_the_published_reference.md` — whether the published API
  reference should carry its hidden `Developer` branch into `molsysmt._private`.
  Undecided rather than broken; today the branch is four files documenting one
  exception, and the only page a reader can reach describes a module that was
  removed seven months ago.
- `presentation_and_citation_surface.md` — partially resolved on 2026-08-07. The
  authorship question is decided and the misattributed ORCID is gone with it, and
  the duplicate landing page is deleted. Two items remain: the stale, malformed DOI
  and version in `CITATION.cff`, and the timing of the installation instructions
  against the Conda delivery track.

### Education

- `course_review/` — unresolved retrospective course improvements.

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
