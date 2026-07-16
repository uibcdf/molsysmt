# Pending Proposals

This directory contains work that has not been accepted as part of the current
MolSysMT contract. A proposal may be technically detailed without being approved,
implemented, benchmarked, or scientifically validated.

Before implementation, check the proposal against current code and dependency
versions: proposals are intentionally allowed to age. Record a decision, define
acceptance criteria, and migrate durable rules into normative documents when the
work is completed.

Large architectural proposals should begin with a small evidence-gathering phase
and must not weaken dependency policy, lifecycle integrity, diagnostics, or the
scientific-validation requirements.

## Triage map

### Reliability and contract work

- `technical_and_scientific_quality_improvement_program.md` — umbrella quality
  program; split accepted work into smaller changes.
- `explicit_form_support_registry.md` — removing implicit Tier 1 classification.
- `machine_readable_api_stability_registry.md` — explicit symbol stability.
- `documentation_lifecycle_manifest.md` — API-to-doc/course traceability.
- `catalog_diagnostics_migration.md` — risk-ranked diagnostics cleanup.
- `benchmark_regression_gate_reliability.md` — statistically credible gates.
- `conversion_fidelity_and_molsysdict_v1.md` — executable Tier 1 conversion
  fidelity and a versioned path beyond the MolSysDict 0.1 boundary.
- `chemical_graph_and_conversion_execution_checkpoint.md` — current re-entry
  point: approve and validate the native chemical-graph contract before Rust,
  interactions, reactive states, or broad adapter fan-out.
- `chemical_state_adapter_fidelity_audit.md` — source-by-source audit of native
  bond-storage coupling, chemical metadata preservation, explicit conversion
  losses, and the ordered adapter migration.

### Scientific and ecosystem requests

- `chemical_metadata_preservation_sdf_mol2.md`
- `physchem_electronegativity_per_element.md`
- `physchem_support_dummy_atoms.md`
- `proposal_protor_atom_typing_and_radii.md`
- `topomt_requested_spatial_helpers_and_sasa.md`
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
- `rusterization_heavy_computations.md`
- `rusterization_hybrid_columnar_ecs_arrow_graph_engine.md`
- `rusterization_parallel_trajectory_io.md`
- `rusterization_topology_and_selections.md`
- `pyunitwizard_global_standards_conflict.md`
- `smonitor_feedback.md`
- `conda_numba_preheating.md`
- `git_history_bloat_cleanup.md`

### Education

- `course_review/` — unresolved retrospective course improvements.

This index is organizational only. Priority comes from evidence, scientific
risk, effort, and an explicit maintainer decision. Proposals marked exploratory
or partially superseded must be re-scoped before implementation.
