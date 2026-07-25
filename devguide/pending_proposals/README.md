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

- `trajectory_projection_onto_principal_components.md` — explicit per-frame
  projection onto a fitted PCA basis without confusing scores with eigenvectors.
- `chemical_metadata_preservation_sdf_mol2.md`
- `proposal_protor_atom_typing_and_radii.md`
- `topomt_requested_spatial_helpers_and_sasa.md` — Part 1 (configurable
  `probe_radius` / `n_sphere_points`) done; Part 2 (grid helpers) pending.
- `sasa_methodologies_and_acceleration_post_1_0.md` — cell-list acceleration and
  alternative SASA methodologies (LCPO, Lee–Richards).
- `neighbor_list_consumer_migration.md` — migrate `get_neighbors` (threshold mode)
  and h-bond candidate generation onto the shared cell-list neighbour-list primitive.
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
- `rust_numba_coexistence_and_cut_plan.md` — the migration plan now that all 97 CPU kernels
  are ported: a `configure.kernel` global + uniform `kernel=` override (reusing the existing
  parallel=/num_threads= pattern, not per-function args), the packaging gate (CI wheels; hard
  dependency vs graceful `'auto'`), the announced tolerance-level numerical change, the 1.0
  deprecation of Numba, and where redesign levers A/B (now) and C/D/E (post-cut) fit.
- `rusterization_pilot_conclusions_and_adoption.md` — hands-on pilot results and a
  recommended incremental adoption path (start migrating kernels behind an opt-in seam
  now; keep shipping Rust wheels a post-1.0 infrastructure decision).
- `linear_algebra_backend_for_rust_kernels.md` — whether the Rust kernels should link
  LAPACK/MKL. Measured answer: 10 of the 11 blocked kernels only diagonalise 3x3 and 4x4
  matrices, and PCA spends 76-93% of its time building the covariance rather than
  diagonalising it, so the useful property is fast BLAS, not a fast eigensolver.
  Recommends pure Rust (`nalgebra`, `faer`) over a BLAS system dependency.
- `triclinic_cell_list_completeness.md` — **RESOLVED**. The Rust cell list and cell-list
  SASA are now correct on triclinic (and small) boxes: perpendicular-thickness grid sizing,
  lattice fractional binning (`inv^T·p`), reduced-cell minimum image, and a unique-cell
  stencil for n<3. Validated against an all-pairs ±2 ground truth and the brute-force SASA.
- `rust_gpu_backend_options.md` — whether the Rust layer should also target the GPU.
  Recommendation: no, near-term — GPU stays on the existing Numba-CUDA/Taichi backends,
  orthogonal to the CPU numba/rust choice. If ever pursued, `wgpu` is the portable
  (default-wheel-compatible) option and CUDA (`cudarc`) belongs only in an optional wheel
  variant. Separate, optional, post-cut; must not block the CPU cut.
- `rust_kernel_redesign_beyond_faithful_ports.md` — where a redesign beats the faithful
  ports. Measured: the obvious in-kernel micro-opts are already in the Numba original, and
  real-workload time is dominated by `get_contacts` going through the dense distance matrix
  and by GC pressure from per-op temporaries — neither an in-kernel problem. Ranks the real
  levers (PCA covariance, cell-list routing, fused passes, SoA layout, Niggli cell).
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
