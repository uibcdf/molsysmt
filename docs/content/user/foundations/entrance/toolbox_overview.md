(user-foundations-entrance-toolbox-overview)=
# Overview of Tools

As a Multi-Toolkit, MolSysMT organizes its functional API into specialized tool compartments (namespaces). Each compartment is dedicated to a specific domain of molecular operations — from system preparation and coordinate geometry to topological connectivity, periodic boundary conditions, physical-chemical properties, and third-party interoperability.

This modular architecture provides purpose-built function names and a uniform
vocabulary across the supported forms. Each calculation requires the information
appropriate to its domain.

---

## Basic
Element IDs are nullable labels, while indices are positions. Universal and
native `get()` keep missing IDs as `None`; literal strings such as `"None"`
or `"<NA>"` remain labels. Preparation tools must transport correspondence by
indices rather than infer it from labels or make existing labels unique.

The **{doc}`Basic <../../tools/basic/index>`** module (`molsysmt.basic`) provides core, form-agnostic operations used across almost every workflow.
- **Key Operations**: `get`, `set`, `select`, `convert`, `extract`, `view`, `compare`, `add`, `contains`, `copy`, `remove`, `append_structures`.
- **Philosophy**: A shared query and operation vocabulary for supported files, external objects and native systems. Each operation needs the relevant attributes and an implemented delivery route; a topology-only form cannot supply coordinates.

---

## Form
The **{doc}`Form <../../tools/form/index>`** module (`molsysmt.form`) hosts the format adapters used by discovery, conversion and attribute delivery.
- **Key Operations**: Public queries use `msm.get_form()`, `msm.get_attributes()` and `msm.has_attribute()` through the Basic API; individual adapters supply their delivery routes.
- **Philosophy**: Dynamic introspection layer that determines how attributes and structural features are extracted or converted across supported data forms.

---

## Element
The **{doc}`Element <../../tools/element/index>`** module (`molsysmt.element`) provides targeted access and manipulation across molecular element types.
- **Sub-namespaces**: `atom`, `group` (including amino acids, nucleotides, water, ions, lipids and small molecules), `component`, `molecule`, `entity`, `chain`.
- **Philosophy**: Hierarchical queries allowing operations tailored to specific structural scales (e.g., querying alpha-carbon atoms of a chain or retrieving residue sequences for specific protein entities).

---

## Build
The **{doc}`Build <../../tools/build/index>`** module (`molsysmt.build`) provides native structure preparation, capping, hydrogen placement, solvation, and molecular repair capabilities.
Preparation can retain operation-scoped evidence and atom correspondences in
`ChemicalStates`. Replacing solvent with ions requires an explicit composition
contract: an added population, a neutralizing population and an approximate
concentration are distinct requests. A stored chemical charge, a force-field
charge and a tabulated pH reference are distinct sources of evidence.
- **Key Operations**: `editable`, `get_missing_heavy_atoms`, `add_missing_heavy_atoms`, `get_missing_terminal_cappings`, `add_missing_terminal_cappings`, `add_missing_hydrogens`, `solvate`, `mutate`.
- **Philosophy**: Modular construction and repair with explicit prerequisites. Operations combine native tools and lazily loaded optional engines according to their supported method; successful local repair does not certify complete chemical preparation.

---

## Structure
The **{doc}`Structure <../../tools/structure/index>`** module (`molsysmt.structure`) handles coordinate geometry, spatial measurements, structural analysis, and 3D transformations.
- **Key Operations**: `get_distances`, `get_vectors`, `get_contacts`, `get_rmsd`, `get_rmsf`, `least_rmsd_fit`, `least_rmsd_align`, `get_radius_of_gyration`, `get_principal_axes`, `get_dihedral_angles`, `center`, `translate`, `rotate`.
- **Philosophy**: Geometric tools reuse the bundled Rust kernels. Coordinate arrays have shape `(n_structures, n_atoms, 3)`; kernel boundaries use explicit nm values, while public quantities follow your PyUnitWizard policy. Proper rotation matrices are 3×3, and fitting a unique three-dimensional rotation requires at least three non-collinear points. Other measurements have their own prerequisites.

---

## Topology
The **{doc}`Topology <../../tools/topology/index>`** module (`molsysmt.topology`) compares sequences over represented groups. Native Topology owns stable atoms, groups, molecules, entities and chains, without bonds or chemical-state components.
- **Key Operations**: `get_sequence_alignment`, `get_sequence_identity`.
- **Philosophy**: Stable inventory and explicit source-index correspondence, independently of chemical connectivity and coordinates.

---

## Chemical States
The **{doc}`Chemical States <../../tools/chemical_states/index>`** module (`molsysmt.chemical_states`) analyzes a selected stored chemical graph. ChemicalStates owns bonds, assignments and state-local components.
- **Key Operations**: `get_bondgraph`, `get_covalent_blocks`, `get_covalent_paths`, `get_rings`, `get_rotatable_bonds`, `get_rigid_fragments`, `get_substructure_matches`, `get_atom_correspondences`, `get_dihedral_quartets`.
- **Philosophy**: Explicit state selection and honest chemical prerequisites. Graph editing does not redefine stable molecules; geometric dihedral measurements remain in `structure`.

---

## PBC
The **{doc}`PBC <../../tools/pbc/index>`** module (`molsysmt.pbc`) manages periodic boundary conditions, unit cell box vectors, and boundary unwrapping.
- **Key Operations**: `get_box_from_lengths_and_angles`, `get_lengths_from_box`, `get_angles_from_box`, `get_volume_from_box`, `unwrap`, `wrap_to_mic`, `wrap_to_pbc`.
- **Philosophy**: Explicit periodic reconstruction and minimum-image operations on molecular structures. Supply a valid box and request the intended periodic behavior; an operation does not infer missing boxes or silently make molecules whole.

---

## Physchem
The **{doc}`Physchem <../../tools/physchem/index>`** module (`molsysmt.physchem`) computes physical and chemical properties of molecular systems.
- **Key Operations**: `get_charge`, `get_mass`, `get_sasa`, `get_tpsa`, `get_lipophilicity`, `get_aromatic_rings`, `get_chemical_readiness`.
- **Philosophy**: Physical and chemical descriptors with explicit method definitions and chemical prerequisites. Dimensional results carry PyUnitWizard quantities; dimensionless descriptors retain their documented scale. Tabulated reference values and coordinate-dependent observables describe different properties.

---

## Molecular Mechanics
The **{doc}`Molecular Mechanics <../../tools/molecular_mechanics/index>`** module (`molsysmt.molecular_mechanics`) handles forcefield definitions, atom types, and mechanics parameters.
- **Key Operations**: `get_engine_forcefield`, `get_degrees_of_freedom`, `get_forces`, `get_potential_energy`, `potential_energy_minimization`.
- **Philosophy**: Engine-backed mechanical calculations with explicit optional dependencies. The native MolecularMechanics container remains experimental. H5MSM 1.0 preserves its admitted parameters and original assignment reports; explicit 0.5 output refuses stored mechanics. Persistence does not validate a force-field assignment or run a calculation.

---

## Interactions
The **{doc}`Interactions <../../tools/interactions/index>`** module (`molsysmt.interactions`) detects and characterizes chemically interpreted interactions, including hydrogen bonds, disulfide candidates, ionic, hydrophobic, aromatic, halogen and metal-mediated observations.
- **Results**: Sparse `Interactions` analyses with participant roles, evaluated scope, units and scientific provenance; callers explicitly attach named analyses to MolSys.
- **Philosophy**: Coordinate-dependent observations remain separate from the stored chemical graph. Controlled edits invalidate affected evidence; detectors do not rerun automatically.

---

## Hbonds
The **{doc}`Hbonds <../../tools/hbonds/index>`** module (`molsysmt.interactions.hbonds`) detects and analyzes hydrogen-bonding networks across structures and trajectories.
- **Key Operations**: `get_hbonds`, `get_hbond_sites`, `get_hbond_site_directions`, `get_acceptor_atoms`, `get_donor_atoms`.
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
