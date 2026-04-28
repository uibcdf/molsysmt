# Proposed Course Structure: "Introduction to MolSysMT"

This document outlines a 50-module comprehensive curriculum organized into 6 operational phases. It follows a "spiral learning" approach: from immediate results to deep architectural mastery.

---

## Phase 1: First Contact (Quick Start & Visual Selection)
*Goal: Load, visualize, and interact. Get results in 5 minutes.*

### Module 1: Philosophy, Forms & Quick Reports
- **Objective:** Understand why MolSysMT is different.
- **Topics:** Form agnosticism, `convert()`, and visual inventory with `info()`.

### Module 2: Visualizing Anything
- **Objective:** Immediate visual feedback.
- **Topics:** `view()`. MolSysViewer (native) vs. third-party viewers.

### Module 3: Talking to Atoms (Selection Language)
- **Objective:** Master the selection syntax.
- **Topics:** Standard keywords, logic, proximity, and hierarchical grouping.

### Module 4: Interactive Selection
- **Objective:** Sync Python with the 3D Viewer.
- **Topics:** Pick residues with the mouse and fetch indices back to Python.

### Module 5: Programmatic Extraction (`get`)
- **Objective:** Extract raw data for Python scripts.
- **Topics:** Coordinates, names, and IDs. Understanding the coordinate tensor shape.

### Module 6: Unit Safety (PyUnitWizard)
- **Objective:** Physical consistency across the MolSysSuite.
- **Topics:** Default units, global configuration, and quantity agnosticism.

### Module 7: System Modification (`set`)
- **Objective:** Modify system attributes in memory.
- **Topics:** Changing coordinates and renaming biological units. Mutable vs Immutable forms.

### Module 8: Discovery & Attributes
- **Objective:** Audit the capabilities of any object.
- **Topics:** `has_attribute()`, `get_attributes()`, and the capability matrix.

---

## Phase 2: Molecular Anatomy (Hierarchies & Navigation)
*Goal: Understand the internal organization and how to navigate it.*

### Module 9: Working with Lists (Composite Systems)
- **Objective:** Combine data from multiple sources (e.g., Topology + Trajectory).
- **Topics:** Data precedence and the virtual system model.

### Module 10: Hierarchical Levels
- **Objective:** Navigate Atom, Group, Component, Molecule, Chain, and Entity.
- **Topics:** Understanding the "Group" vs "Residue" terminology.

### Module 11: Navigating Between Levels
- **Objective:** Map information between biological scales.
- **Topics:** Mapping upward (Atom -> Group) and downward (Entity -> Atoms).

### Module 12: Iterating Hierarchies (`Iterator`)
- **Objective:** Sequential processing of biological units.
- **Topics:** Efficient looping over groups, chains, and structures.

### Module 13: System Auditing and Curing
- **Objective:** Find and prepare for structural errors.
- **Topics:** Missing atoms, gaps in sequences, and missing bonds.

### Module 14: Covalent Connectivity
- **Objective:** Master the covalent skeleton.
- **Topics:** Bonded atom pairs, covalent blocks, and NetworkX graph conversion.

### Module 15: Comparing Systems
- **Objective:** Verify identity and consistency.
- **Topics:** Topological identity vs Structural similarity using `compare()`.

### Module 16: Semantic Labeling
- **Objective:** Generate human-readable labels.
- **Topics:** `get_label()` and custom nomenclature templates.

---

## 🛣️ Branching Point: Specialized Paths (Modules 17-50)

From this point forward, the curriculum branches into four specialized domains. Each path applies Phases 3 to 6 to a distinct computational challenge:

1.  **Path A: Peptide-Based Inhibition of Amyloid-Beta Aggregation.**
2.  **Path B: Rational Engineering of Plastic-Degrading Enzymes.**
3.  **Path C: Binding Affinity Optimization of Antiviral Inhibitors.**
4.  **Path D: Dynamic Analysis of Membrane-Embedded Ion Channels.**

---

## Phase 3: The Virtual Lab (Editing, Repairing & Building)
*Goal: Mutate, repair, solvate, and build structures.*

### Module 17: Surgical Extraction & Deletion
- **Objective:** Isolate binding pockets or remove solvent.
- **Topics:** `extract()`, `remove()`, and `copy()`.

### Module 18: Structural Auditing (Diagnostics)
- **Objective:** Find what's broken before fixing it.
- **Topics:** `get_missing_residues()`, `get_missing_heavy_atoms()`, `get_non_standard_residues()`.

### Module 19: Structural Repair & Mutagenesis
- **Objective:** Fix gaps and change residues.
- **Topics:** `mutate()`, adding hydrogens, and heavy atom reconstruction.

### Module 20: Peptide Synthesis
- **Objective:** Build structures from sequences.
- **Topics:** `build_peptide()` and terminal cappings.

### Module 21: Solvation & Ion Engineering
- **Objective:** Hydrate the system for simulation.
- **Topics:** `solvate()`, `make_water_box()`, and salt concentrations.

### Module 22: Attribute Engineering (Patching)
- **Objective:** Fix IDs and names programmatically.
- **Topics:** Using `set()` to update topology and coordinates. The "Patch Mode": correcting atom names or chain IDs in a defective topology without rebuilding.

### Module 23: Conformational Engineering
- **Objective:** Rotate dihedrals to fix clashes or prepare states.
- **Topics:** `set_dihedral_angles()` and `shift_dihedral_angles()`.

### Module 24: The MolSysBuilder API
- **Objective:** High-level declarative building.
- **Topics:** The `editable()` entrypoint and custom building from scratch.

### Module 25: PDB Bioassemblies & AltLocs
- **Objective:** Handle complex structural records.
- **Topics:** `make_bioassembly()` and solving alternate locations.

---

## Phase 4: Data Analyst (Geometric & Physical Analysis)
*Goal: Extract scientific meaning from structures and trajectories.*

### Module 26: Geometrical Measurements
- **Objective:** Distances, angles, and dihedrals.
- **Topics:** `get_distances()`, `get_minimum_distances()`.

### Module 27: Proximity & Neighborhoods
- **Objective:** Find what's around your ligand.
- **Topics:** `get_contacts()`, `get_neighbors()`.

### Module 28: Visualizing Interaction Matrices
- **Objective:** Instant reporting of contacts.
- **Topics:** `show_contacts()` plots.

### Module 29: Ensemble Descriptors (Global Metrics)
- **Objective:** RG, Center of Mass, RMSF.
- **Topics:** `get_radius_of_gyration()`, `get_center()`, `get_rmsf()`.

### Module 30: Comparison & Superposition
- **Objective:** Align structures and measure RMSD.
- **Topics:** `get_rmsd()`, `least_rmsd_align()`, `least_rmsd_fit()`.

### Module 31: Principal Components (PCA) & Axes
- **Objective:** Analyze major modes of motion.
- **Topics:** `get_principal_axes()`, `align_principal_axes()`, and PCA.

### Module 32: Secondary Structure & Folds
- **Objective:** Characterize folding patterns.
- **Topics:** `get_secondary_structure()` (DSSP integration).

### Module 33: Hydrogen Bonds & Salt Bridges
- **Objective:** Map non-covalent networks.
- **Topics:** `get_hbonds()`, `get_salt_bridges()`.

### Module 34: Advanced H-Bond Algorithms
- **Objective:** Buch and Luzar-Chandler criteria.
- **Topics:** Donor/Acceptor inclusion rules.

### Module 35: Physicochemical Properties
- **Objective:** Mass, Charge, SASA, Volume, Hydrophobicity.
- **Topics:** `get_sasa()`, `get_charge()`, `get_volume()`. Interface analysis: `get_area_buried` and `get_buried_fraction`.

---

## Phase 5: The Physics Lab (Environment & Simulation)
*Goal: Manage boxes, periodicity, energies, and external engines.*

### Module 36: PBC Geometry & Conventions
- **Objective:** Master simulation boxes.
- **Topics:** `has_pbc()`, box shapes, lengths, and angles.

### Module 37: Wrapping & Unwrapping
- **Objective:** Handle periodicity correctly.
- **Topics:** `wrap_to_pbc()` vs `wrap_to_mic()`, and `unwrap()`.

### Module 38: Molecular Mechanics (Energies)
- **Objective:** Calculate potential energy.
- **Topics:** `get_potential_energy()`, `get_forces()`, and `MolecularMechanicsDict`.

### Module 39: Energy Minimization
- **Objective:** Optimize the structure.
- **Topics:** `potential_energy_minimization()`.

### Module 40: AMBER TLeap Integration
- **Objective:** Parametrize systems with AMBER.
- **Topics:** Using `tleap` through MolSysMT.

### Module 41: OpenMM Integration
- **Objective:** Bridge to simulation production.
- **Topics:** Direct interaction with OpenMM objects.

### Module 42: Geometric Transformations (Space)
- **Objective:** Move molecules in the box.
- **Topics:** `translate()`, `rotate()`, `center()`, `move_away()`.

---

## Phase 6: Pipeline Developer (Performance & Scaling)
*Goal: Process Big Data and extend the framework.*

### Module 43: Trajectory Management (Slicing)
- **Objective:** Master time-based data slicing.
- **Topics:** `concatenate_structures()`, frame slicing, and structure IDs.

### Module 44: Scalability & Heavy Trajectories
- **Objective:** Handle files larger than RAM.
- **Topics:** `ChunkedExecutor`, `Iterator()`, and `Reducer`.

### Module 45: Performance Optimization
- **Objective:** JIT kernels and startup speed.
- **Topics:** `warmup_numba()`.

### Module 46: Virtual Forms & Memory I/O
- **Objective:** Cloud-friendly and disk-less workflows.
- **Topics:** `string:pdb_text`, memory buffers, and resource safety.

### Module 47: Writing Your Own Form-Agnostic Functions
- **Objective:** Extend MolSysMT with your own tools.
- **Topics:** Using `@arg_digest` in custom functions.

### Module 48: Framework Reliability & SMonitor
- **Objective:** Understand error handling and diagnostics.
- **Topics:** `smonitor` signals and traceability.

### Module 49: Capability Matrix & Config
- **Objective:** Fine-tune the framework.
- **Topics:** `supported.forms`, `supported.conversions`, and `msm.configure`.

### Module 50: Best Practices, Future & Contribution
- **Objective:** Master the MolSysMT way of coding.
- **Topics:** Design patterns, 1.x roadmap, and contributing.
