(user-foundations-native-world-molsys)=
# molsysmt.MolSys

`molsysmt.MolSys` is MolSysMT's primary native in-memory class. It represents a complete, self-contained molecular system by encapsulating three dedicated sub-objects that decouple topological, structural, and physical mechanics data.

---

## Internal Architecture

A `molsysmt.MolSys` object encapsulates three internal attributes:

- **`molsys.topology`**: An instance of `molsysmt.Topology` managing the molecular graph, element hierarchies (`atom`, `group`, `component`, `chain`, `molecule`, `entity`), covalent bonds, and chemical identity metadata.
- **`molsys.structures`**: An instance of `molsysmt.Structures` storing 3D atomic coordinates, periodic boundary box vectors, time series, and trajectory frame metadata.
- **`molsys.molecular_mechanics`**: An instance of `molsysmt.MolecularMechanics` managing force field definitions, partial charges, atomic masses, non-bonded parameters, and energy contracts.

Any of these three components can be populated or empty depending on the information available in the system.

---

## Design Invariants

The `molsysmt.MolSys` class enforces fundamental data invariants across MolSysMT:

- **Unit Conventions**: Spatial coordinates are stored in nanometers (`nm`), time in picoseconds (`ps`), and charges in elementary charge units (`e`).
- **String Identifiers**: Element IDs (`atom_id`, `group_id`, `chain_id`, etc.) are normalized as strings.
- **Frame Coordinates**: Coordinate arrays maintain shape `(n_structures, n_atoms, 3)`.
