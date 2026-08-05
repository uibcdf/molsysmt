(user-foundations-entrance-toolbox-overview)=
# Toolbox Overview

MolSysMT organizes its functional API into purpose-built **"boxes"** (namespaces). Each box is defined around a specific domain of operations — such as structural preparation, coordinate geometry, topological inventory, or third-party interoperability.

This modular organization allows you to work with clean, specialized function names without cluttering your global scope, while maintaining a consistent vocabulary across all **89 supported forms**.

---

## Basic Box
The **{doc}`Basic <../../tools/basic/index>`** box (`molsysmt.basic`) contains the core, form-agnostic operations used in almost every MolSysMT script.
- **Key Operations**: `get`, `set`, `select`, `convert`, `build`, `view`, `compare`, `add`, `contains`, `copy`, `remove`, `append_structures`.
- **Philosophy**: Uniform interaction layer operating on any molecular representation — whether it is a disk file (PDB, mmCIF, GRO), an in-memory object (OpenMM `Topology`, MDAnalysis `Universe`), or a native `MolSys`.

---

## Build Box
The **{doc}`Build <../../tools/build/index>`** box (`molsysmt.build`) provides native structure preparation and molecular repair capabilities.
- **Key Operations**: `get_missing_heavy_atoms`, `add_missing_heavy_atoms`, `get_missing_terminal_cappings`, `add_missing_terminal_cappings`, `add_missing_hydrogens`, `solvate`, `add_counterions`, `mutate`.
- **Philosophy**: Complete, simulation-ready system preparation executed natively in Python without requiring external software installations like PDBFixer or OpenMM.

---

## Structure Box
The **{doc}`Structure <../../tools/structure/index>`** box (`molsysmt.structure`) handles coordinate geometry, spatial measurements, structural analysis, and 3D transformations.
- **Key Operations**: `get_distances`, `get_contacts`, `get_sasa`, `get_rmsd`, `get_rmsf`, `fit`, `align`, `get_radius_of_gyration`, `get_principal_axes`, `get_dihedral_angles`, `center`, `translate`, `rotate`.
- **Philosophy**: High-performance analytical operations executed on precompiled Rust kernels. Coordinates follow strict geometric contracts: nanometer units, NumPy array shape `(n_structures, n_atoms, 3)`, right-handed 3×3 rotation matrices, and deterministic fitting requiring at least three non-collinear atoms.

---

## Topology Box
The **{doc}`Topology <../../tools/topology/index>`** box (`molsysmt.topology`) governs chemical connectivity, bond matrices, sequence extraction, and secondary structure assignment.
- **Key Operations**: `get_bond_graph`, `get_covalent_blocks`, `get_covalent_chains`, `get_covalent_paths`, `get_sequence`, `get_secondary_structure`.
- **Philosophy**: Fast topological inventory management preserving stable element identifiers rather than renumbering them, maintaining chemical integrity across form conversions.

---

## Elements Box
The **{doc}`Elements <../../tools/element/index>`** box (`molsysmt.element`) provides hierarchical access and manipulation across structural scales.
- **Sub-namespaces**: `atom`, `group` (amino acids, nucleotides, ions), `component`, `molecule`, `entity`, `chain`.
- **Philosophy**: Enables targeted queries and operations tailored to specific biological tiers (e.g., getting all alpha-carbon atoms of a chain or retrieving residue sequences for specific protein entities).

---

## PBC & Physical Mechanics Box
Physical conditions, periodic boundaries, and forcefield specifications are organized under specialized mechanics namespaces:
- **{doc}`PBC <../../tools/pbc/index>`** (`molsysmt.pbc`): `get_box`, `set_box`, `unwrap`, `wrap`, `get_box_volume`, `get_box_angles`.
- **{doc}`Physical-Chemical Properties <../../tools/physchem/index>`** (`molsysmt.physchem`): `get_charge`, `get_mass`, `get_degrees_of_freedom`.
- **{doc}`Molecular Mechanics <../../tools/molecular_mechanics/index>`** (`molsysmt.molecular_mechanics`): Forcefield assignments, atom types, and mechanics parameters.

---

## Third-Party Bridges Box
The **{doc}`Third Party <../../tools/third_party/index>`** box (`molsysmt.third_party`) hosts specialized bridges to external libraries in the computational biology ecosystem.
- **Supported Integrations**: OpenMM, MDAnalysis, MDTraj, ParmEd, PyTraj, RDKit, Biopython, NGLView, MolSysViewer.
- **Philosophy**: Zero-friction handshakes allowing MolSysMT to delegate specialized computation or visualization to external engines without writing custom file conversion scripts.

---

:::{admonition} How to Explore the Toolbox
:class: note
- **Step-by-Step Tutorials**: To learn how to use each tool with interactive code examples, explore the **{doc}`Tools User Guide <../../tools/index>`**.
- **Technical Specifications**: To consult exact function signatures, argument types, docstrings, and developer API details, visit the **{doc}`Technical API Documentation <../../../../api/index>`**.
:::
