# MolSysMT Developer Guide

`devguide/` contains the maintained engineering and scientific-development
contract for MolSysMT. It is not a session log and it is not a claim that every
described capability is implemented.

## How to interpret this directory

Documents have one of four roles:

1. **Normative** documents define current invariants, interfaces, or policies.
2. **Operational** documents describe maintained development and validation
   workflows.
3. **Pending** documents record unresolved bugs or proposals. They are not part
   of the implemented contract.
4. **Archived** documents preserve dated assessments and release planning. They
   provide historical context only.

When documents disagree, use this order of authority:

1. repository-wide and local `AGENTS.md` instructions;
2. current code plus executable tests;
3. normative documents listed below;
4. operational documents;
5. pending and archived material.

An implementation-status statement is trustworthy only when it points to code,
tests, or reproducible validation evidence. Dated benchmark numbers are
observations from a particular environment, not timeless performance guarantees.

See [DOCUMENT_POLICY.md](DOCUMENT_POLICY.md) for maintenance and status rules.

## Start here

Read these documents in order when first working on MolSysMT:

1. [Core specification](CORE_SPECIFICATION.md) — native model, hierarchy, and
   package boundaries.
2. [Public API surface](api_surface.md) — stability classification and public
   contract.
3. [Interfaces](INTERFACES.md) — form-agnostic behavior and I/O boundaries.
4. [Forms and conversions](forms_and_conversions.md) — adapter and conversion
   semantics.
5. [Testing strategy](testing_strategy.md) — evidence required for a supported
   claim.
6. [Scientific validation](scientific_validation.md) — independent evidence,
   conventions, and tolerance governance.
7. [Diagnostics](DIAGNOSTICS.md) and [error policy](error_policy.md) — failure
   and observability behavior.
8. [Performance and JIT](performance_and_jit.md) and
   [scalability](SCALABILITY.md) — trusted kernels and heavy trajectories.

## Maintained normative documents

### Architecture and data model

- [CORE_SPECIFICATION.md](CORE_SPECIFICATION.md)
- [ALGORITHMS.md](ALGORITHMS.md)
- [INTERFACES.md](INTERFACES.md)
- [api_surface.md](api_surface.md)
- [BUILDER_API.md](BUILDER_API.md)
- [BUILD_ECOSYSTEM.md](BUILD_ECOSYSTEM.md)
- [declarative_serialization_forms.md](declarative_serialization_forms.md)
- [h5msm_format.md](h5msm_format.md)
- [forms_and_conversions.md](forms_and_conversions.md)
- [form_adapter_implementation.md](form_adapter_implementation.md)

### Scientific construction and analysis

- [scientific_validation.md](scientific_validation.md)
- [scientific_evidence_matrix.md](scientific_evidence_matrix.md) — generated
  status view backed by the executable Scientific Truth evidence registry.
- [structure_preparation_pipeline.md](structure_preparation_pipeline.md)
- [performance_and_jit.md](performance_and_jit.md)
- [rust_kernel_optimization_guide.md](rust_kernel_optimization_guide.md) — the
  measured method for optimising the Rust kernels, including what was tried and
  did not work, and why the wheel stays a portable baseline build.
- [SCALABILITY.md](SCALABILITY.md)
- [gpu_acceleration.md](gpu_acceleration.md) — design and capability map; each
  backend claim must still be confirmed by its tests.

### Reliability and governance

- [testing_strategy.md](testing_strategy.md)
- [testing_form_adapters.md](testing_form_adapters.md)
- [devtools_and_ci.md](devtools_and_ci.md)
- [DIAGNOSTICS.md](DIAGNOSTICS.md)
- [error_policy.md](error_policy.md)
- [deprecation_policy.md](deprecation_policy.md)
- [digestion_and_dependencies.md](digestion_and_dependencies.md)
- [support_tier_protocol.md](support_tier_protocol.md)
- [support_tiers.ipynb](support_tiers.ipynb) — executable report, not a second
  tier registry.

### Documentation, education, and visualization

- [documentation_sync.md](documentation_sync.md)
- [notebook_compilation_and_visualization.md](notebook_compilation_and_visualization.md) — normative specification for notebook pre-execution, timestamp tracking, and MolSysViewer integration.
- [course_structure.md](course_structure.md)
- [viewers_and_visualization.md](viewers_and_visualization.md)
- [molsysviewer_addon.md](molsysviewer_addon.md)

### Strategy and measurements

- [competitive_landscape_and_vision.md](competitive_landscape_and_vision.md)
- [roadmap.md](roadmap.md)
- [benchmarking/README.md](benchmarking/README.md)

### Release operations

- [release_1_0_status.md](release_1_0_status.md) — live phase/stage status and
  evidence ledger for the remaining 1.0 work.
- [release_gate.md](release_gate.md) — exact-commit checklist required before
  tagging.
- [release_1_0_execution_plan.md](pending_proposals/release_1_0_execution_plan.md)
  — accepted ordering, weights, exit gates, and stop conditions.

Strategic documents describe direction. They do not override the API, testing,
dependency, or scientific contracts above.

## Work queues

- [Pending bugs](pending_bugs/README.md) contain reproduced or suspected defects.
- [Pending proposals](pending_proposals/README.md) contain ideas awaiting a
  decision or implementation.
- [Archived material](archive/README.md) contains dated audits, assessments, and
  release checkpoints.

Moving a document into a pending or archived directory changes its documentary
status; it does not close a bug, accept a proposal, or certify an implementation.

## Essential external guides

The repository root contains required integration guidance that complements this
directory:

- [`SMONITOR_GUIDE.md`](../SMONITOR_GUIDE.md)
- [`ARGDIGEST_GUIDE.md`](../ARGDIGEST_GUIDE.md)
- [`PYUNITWIZARD_GUIDE.md`](../PYUNITWIZARD_GUIDE.md)
- [`DEPDIGEST_GUIDE.md`](../DEPDIGEST_GUIDE.md)

## Maintenance check

Run the developer-guide validator after changing this directory:

```bash
python devtools/scripts/validate_devguide.py
```

The validator checks local Markdown targets, forbidden machine-specific links,
and references to retired document names. It does not prove that scientific or
implementation claims are true; those require tests and reproducible evidence.
