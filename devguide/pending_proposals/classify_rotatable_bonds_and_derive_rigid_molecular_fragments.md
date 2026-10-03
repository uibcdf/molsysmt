---
summary: Classify rotatable bonds and derive rigid molecular fragments
issue: uibcdf/molsysmt#224
status: partial
opened: 2026-09-22
closed:
verification: reproduced
area: [structure, build]
guard:
normative:
blocked_by: []
supersedes: []
---

# Classify rotatable bonds and derive rigid molecular fragments

**Reported:** 2026-09-22, from the MolSysMT–DockingMT Vina preparation and conversion review.
**Status:** Partial. Explicit chosen-bond fragment partitioning was brought
forward for PDBQT validation; chemical rotatable-bond classification remains
post-1.0.

## What

Expose reusable torsion candidates and the rigid fragments induced by chosen active bonds.

## How

Classify eligible bonds from chemical graph information, explain exclusions such as rings and amides, then derive connected rigid fragments while preserving source atom and bond IDs.

## Why

Existing covalent-block and dihedral operations do not provide a general small-molecule torsion model needed by a flexible PDBQT ligand writer.

## What is measured and what is assumed

**Inspected:** Inspected topology/get_covalent_blocks.py and structure/get_dihedral_quartets.py; Meeko documents configurable rotatable-bond rules.
**Assumed:** The proposed contract is useful for the stated consumer; quantitative impact and complete chemical coverage need representative validation.

## What was refuted

Making ROOT/BRANCH records the general torsion representation was rejected because those records are PDBQT-specific.

## Scope and exclusions

Chemical classification and fragment graph; rooted PDBQT serialization belongs to uibcdf/molsysmt#214, protocol selection to DockingMT.

## Acceptance criteria

- Tests distinguish acyclic single bonds, ring bonds, amides, and incomplete bond-order inputs.
- Selected active bonds produce deterministic rigid fragments and atom/bond correspondence; unsupported cases fail explicitly.

## Dependencies and risks

Related tracked work: uibcdf/molsysmt#214
Cross-component implementation links: uibcdf/dockingmt#6.
New functionality requires tests of scientific semantics and documentation appropriate to its public surface.



## Explicit-cut tool checkpoint — 2026-10-03

`molsysmt.topology.get_rigid_fragments` is a documented experimental general
connectivity tool. It resolves a complete state-specific graph from supported
forms before returning packed int64 fragment memberships, source atom/bond
indices, an atom-to-fragment map and aligned branch endpoint/fragment pairs.
Cuts are explicit source bond indices, deduplicated and range checked. Dative
cuts and original-graph non-bridges fail, including simultaneous ring cuts that
would otherwise disconnect the ring. Isolated atoms and disconnected components
remain represented. Empty arrays have defined shapes. Coordinates and source
chemistry remain unchanged. Standalone ChemicalStates and its typed dictionary
are supported without requiring native Topology or structures.

The implementation uses the existing chemical graph resolver and NetworkX
connectivity/bridge primitives. It has no chemistry perception, PDBQT ROOT
representation, atom typing or implicit chemical storage. The PDBQT writer
reuses this public tool to check supplied trees against complete native graphs.
Contract and form-agnostic tests live in
`tests/topology/test_get_rigid_fragments.py`; its doctest and User Guide/course
explain source indices, completeness and rigidity by explicit graph cuts.

**Remaining:** chemical torsion eligibility, ring/amide and bond-order criteria,
selection policy and explanatory exclusions on representative chemistry. No
heavy-workload measurement or Rust optimization claim is made in this stage.
