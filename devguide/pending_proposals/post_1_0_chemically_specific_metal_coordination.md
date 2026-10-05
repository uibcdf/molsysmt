---
summary: Post-1.0 chemically specific metal coordination
issue: uibcdf/molsysmt#337
status: open
opened: 2026-10-05
closed:
verification: inspected
area: [api, structure]
guard:
normative:
blocked_by: []
supersedes: []
---

# Post-1.0 chemically specific metal coordination

## What

Study chemically specific metal-coordination criteria beyond the current `metal_ligand_distance` proximity profile after 1.0.

## How

Establish primary scientific definitions and independent controls for supported metal/ligand classes. Evaluate metal-dependent distances, oxidation-state evidence, coordination numbers and geometry without treating proximity as proof. Reuse public physchem site interpretation, topology connectivity and structure/pbc geometry. Produce sparse observations with explicit methods, units, participants, scope and original evidence.

## Why

The implemented broad experimental profile preserves its reference sites and inclusive cutoff; its docstring explicitly excludes oxidation state, bond formation, coordination geometry, affinity and energy. The interaction plan leaves metal-specific rules as future work. Preserve that ambition without turning it into a requirement for the delivered family/result namespace.

## What is inspected and what is assumed

The implemented method and exclusions are inspected in `molsysmt/interactions/metal_coordination/get_metal_coordination.py`. No new literature search, chemical benchmark or accuracy claim is made by filing this study.

## What was refuted

A single universal distance threshold is not a metal-specific physical model. Stored dative/covalent assignments and inferred interaction observations have different authority.

## Scope and exclusions

Post-1.0 under the [scope freeze](../release_1_0_scope.md). A method and backend remain undecided. Formal-charge recognition expansion is separately #262; chemical assignment storage stays in ChemicalStates.

## Acceptance criteria

- Record scientific use cases and attributable definitions, supported element/chemical-state coverage and explicit unassessed cases.
- Compare analytical/curated positive and negative geometries, including periodic images and competing ligands.
- Define participant roles and geometric evidence for multi-ligand observations.
- Choose or reject implementation based on scientific evidence and workload cost; update public documentation and independent guards if accepted.

