# Data Model

## Coordinates
- NumPy arrays with shape `(n_structures, n_atoms, 3)` or `(n_frames, n_atoms, 3)`
  for iterators.
- Units: **nanometers (nm)**.

## Box
- NumPy arrays with shape `(n_structures, 3, 3)`.
- Lengths in **nanometers**.
- Angles in **radians** when derived.

## Time
- Arrays of time in **picoseconds (ps)**.

## Charges
- Units of **elementary charge**.

## Get / Iterator / Form / Native Invariants
- `n_atoms` is always an integer, even if no topology is present.
- `n_structures` is `None` when the form has no structural info; otherwise
  always an integer (0 if empty).
- If structural attributes (time, box, etc.) are missing, return a list of
  `None` values matching the requested structure indices.

## Element IDs
In native MolSysMT objects (`molsysmt.Topology`, `molsysmt.MolSys`), element
IDs (`atom_id`, `group_id`, `component_id`, `molecule_id`, `chain_id`,
`entity_id`) are stored as **strings**. Normalize any numeric IDs to strings.
