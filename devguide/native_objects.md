"""
MolSysMT Developer Guide — Native Objects
"""

# Native Objects

## Scope
This document defines invariants and expected behavior for native MolSysMT
objects such as `MolSys`, `Topology`, and `Trajectory`.

## Core Objects
- `molsysmt.MolSys`
- `molsysmt.Topology`
- `molsysmt.Trajectory`

## Invariants
- Element IDs are stored as **strings** (`atom_id`, `group_id`, `component_id`,
  `molecule_id`, `chain_id`, `entity_id`).
- Structural attributes (coordinates, box, time) follow the shapes and units
  defined in `data_model.md`.

## Get / Iterator / Form / Native Behavior
- If time/box/etc. are missing, output lists of `None` with correct length.
- For iterators, coordinates and box always include the frame dimension.

## Converters
Converters must normalize IDs to strings and preserve shapes/units.
