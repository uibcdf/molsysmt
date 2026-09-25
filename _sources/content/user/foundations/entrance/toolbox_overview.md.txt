(user-foundations-entrance-toolbox-overview)=
# Overview of Tools

As a Multi-Toolkit, MolSysMT organizes its functional API into specialized tool compartments (namespaces). Each compartment is dedicated to a specific domain of molecular operations — from system preparation and coordinate geometry to topological connectivity, periodic boundary conditions, physical-chemical properties, and third-party interoperability.

This modular architecture provides clean, purpose-built function names without cluttering your global scope, maintaining a uniform vocabulary across all **89 supported forms**.

---

## Basic
The **{doc}`Basic <../../tools/basic/index>`** module (`molsysmt.basic`) provides core, form-agnostic operations used across almost every workflow.
- **Key Operations**: `get`, `set`, `select`, `convert`, `build`, `view`, `compare`, `add`, `contains`, `copy`, `remove`, `append_structures`.
- **Philosophy**: Universal interaction layer operating identically on any molecular representation — whether a disk file (PDB, mmCIF, GRO), an in-memory object (OpenMM `Topology`, MDAnalysis `Universe`), or a native `MolSys`.

---

## Form
The **{doc}`Form <../../tools/form/index>`** module (`molsysmt.form`) manages form discovery, support tier inspection, form-specific conversions, and attribute capability reporting.
- **Key Operations**: `get_form`, `is_form`, `show_forms`, `get_attributes`.
- **Philosophy**: Dynamic introspection layer that determines how attributes and structural features are extracted or converted across supported data forms.

---

## Element
The **{doc}`Element <../../tools/element/index>`** module (`molsysmt.element`) provides targeted access and manipulation across biological structural tiers.
- **Sub-namespaces**: `atom`, `group` (amino acids, nucleotides, ions), `component`, `molecule`, `entity`, `chain`.
- **Philosophy**: Hierarchical queries allowing operations tailored to specific structural scales (e.g., querying alpha-carbon atoms of a chain or retrieving residue sequences for specific protein entities).

---

## Build
The **{doc}`Build <../../tools/build/index>`** module (`molsysmt.build`) provides native structure preparation, capping, hydrogen placement, solvation, and molecular repair capabilities.
- **Key Operations**: `get_missing_heavy_atoms`, `add_missing_heavy_atoms`, `get_missing_terminal_cappings`, `add_missing_terminal_cappings`, `add_missing_hydrogens`, `solvate`, `add_counterions`, `mutate`.
- **Philosophy**: Complete, simulation-ready system preparation executed natively in Python without requiring external software installations like PDBFixer or OpenMM.

---

## Structure
The **{doc}`Structure <../../tools/structure/index>`** module (`molsysmt.structure`) handles coordinate geometry, spatial measurements, structural analysis, and 3D transformations.
- **Key Operations**: `get_distances`, `get_contacts`, `get_sasa`, `get_rmsd`, `get_rmsf`, `fit`, `align`, `get_radius_of_gyration`, `get_principal_axes`, `get_dihedral_angles`, `center`, `translate`, `rotate`.
- **Philosophy**: High-performance analytical operations executed on precompiled Rust kernels. Coordinates follow strict geometric contracts: nanometer units, NumPy array shape `(n_structures, n_atoms, 3)`, right-handed 3×3 rotation matrices, and deterministic fitting requiring at least three non-collinear atoms.

---

## Topology
The **{doc}`Topology <../../tools/topology/index>`** module (`molsysmt.topology`) governs chemical connectivity, bond matrices, sequence extraction, and secondary structure assignment.
- **Key Operations**: `get_bond_graph`, `get_covalent_blocks`, `get_covalent_chains`, `get_covalent_paths`, `get_sequence`, `get_secondary_structure`.
- **Philosophy**: Fast topological inventory management preserving stable element identifiers rather than renumbering them, maintaining chemical integrity across form conversions.

---

## PBC
The **{doc}`PBC <../../tools/pbc/index>`** module (`molsysmt.pbc`) manages periodic boundary conditions, unit cell box vectors, and boundary unwrapping.
- **Key Operations**: `get_box`, `set_box`, `unwrap`, `wrap`, `get_box_volume`, `get_box_angles`.
- **Philosophy**: Automatic handling of periodic boundary conditions across simulations, ensuring correct distance and contact calculations under minimum image conventions.

---

## Physchem
The **{doc}`Physchem <../../tools/physchem/index>`** module (`molsysmt.physchem`) computes physical and chemical properties of molecular systems.
- **Key Operations**: `get_charge`, `get_mass`, `get_degrees_of_freedom`, `get_molecular_weight`.
- **Philosophy**: Automated calculation of physical-chemical descriptors carrying explicit physical units (`pyunitwizard`).

---

## Molecular Mechanics
The **{doc}`Molecular Mechanics <../../tools/molecular_mechanics/index>`** module (`molsysmt.molecular_mechanics`) handles forcefield definitions, atom types, and mechanics parameters.
- **Key Operations**: `get_forcefield`, `get_atom_type`, `get_partial_charge`.
- **Philosophy**: Inspection and management of molecular mechanics forcefield assignments and parameter sets.

---

## Hbonds
The **{doc}`Hbonds <../../tools/hbonds/index>`** module (`molsysmt.hbonds`) detects and analyzes hydrogen-bonding networks across structures and trajectories.
- **Key Operations**: `get_hbonds`, `get_hbond_acceptors`, `get_hbond_donors`.
- **Philosophy**: Geometric and distance-angle based detection of hydrogen bonds for structural stability analysis.

---

## Third Party
The **{doc}`Third Party <../../tools/third_party/index>`** module (`molsysmt.third_party`) hosts specialized bridges to external software packages in the computational biology ecosystem.
- **Supported Integrations**: OpenMM, MDAnalysis, MDTraj, ParmEd, PyTraj, RDKit, Biopython, NGLView, MolSysViewer.
- **Philosophy**: Zero-friction handshakes allowing MolSysMT to delegate specialized computation or visualization to external engines without writing custom file conversion scripts.

---

:::{admonition} How to Explore the Tools
:class: note
- **Step-by-Step Tutorials**: To learn how to use each tool with interactive code examples, explore the **{doc}`Tools User Guide <../../tools/index>`**.
- **Technical Specifications**: To consult exact function signatures, argument types, docstrings, and developer API details, visit the **{doc}`Technical API Documentation <../../../../api/index>`**.
:::
