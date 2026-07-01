# Proposal: Post-1.0 SDF/MOL2 chemical metadata expansion

**Status:** post-1.0 proposal
**Requester:** MolSysViewer
**Owner:** MolSysMT

## Context

The pre-1.0 baseline is intentionally small: MolSysMT should preserve basic
chemical metadata already represented by native forms and needed by viewers:
`bond_order`, `bond_type`/aromatic markers, and atom formal charge through
`MolecularMechanics`.

The remaining SDF/MOL2 work is useful, but it requires broader schema and API
decisions. It should not block MolSysMT 1.0.

## Deferred Scope

- Add first-class `file:sdf` support, including multi-molecule SDF files.
- Decide the canonical representation for SDF property blocks such as docking
  scores, supplier IDs, names, and custom fields.
- Preserve molecule/component boundaries and per-molecule property blocks for
  multi-ligand files.
- Revisit `file:mol2 -> MolSys` backend selection so cheminformatics-oriented
  parsing can be preferred when metadata fidelity matters, while preserving a
  stable fallback for geometry/topology loading.
- Normalize aromaticity semantics across RDKit, OpenFF, SDF, and MOL2 beyond the
  minimal pre-1.0 `bond_type="aromatic"` contract.
- Decide whether partial charges and other atom-level chemical annotations are
  always part of `ViewerJSON` or exposed through a more general annotations
  block.

## Non-goals Before 1.0

- Do not add ad-hoc chemistry perception in MolSysViewer.
- Do not put force-field/mechanical columns such as `formal_charge` or
  `partial_charge` into `topology.atoms`.
- Do not rush a multi-molecule SDF schema without documenting selection,
  indexing, and metadata ownership.

## Acceptance Criteria For Post-1.0 Completion

- Representative SDF ligands with custom property blocks round-trip through
  MolSysMT without losing molecule-level metadata.
- Multi-molecule SDF files preserve molecule boundaries and property blocks.
- MOL2 loading can preserve chemically meaningful bond order/type and charges
  through a documented backend path.
- `molsysmt.ViewerJSON` exposes the selected metadata in a transport-friendly
  schema for MolSysViewer and other visual consumers.
- Tests cover direct chemical forms, converted native forms, and ViewerJSON
  output.
