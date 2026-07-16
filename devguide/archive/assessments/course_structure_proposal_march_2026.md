# Proposed Course Structure: "Introduction to MolSysMT"

This document outlines a 50-module comprehensive curriculum organized into 6 operational phases. It follows a "spiral learning" approach: from immediate results to deep architectural mastery.

---

## Phase 1: First Contact (Foundations & Input)
*Goal: Load, understand, and compose systems.*

### Module 1: The Form-Agnostic Philosophy
- **Objective:** Understand why MolSysMT is unique.
- **Topics:** Form agnosticism, `convert()`, and basic `info()`.

### Module 2: Native Forms and The Trinity
- **Objective:** Master the internal data model.
- **Topics:** `MolSys = Topology + Structures`. High-performance formats (H5MSM).

### Module 3: Combined Sources (Trajectories)
- **Objective:** Load complex systems from multiple files.
- **Topics:** Mixing Topologies and Coordinates. The Composite System model.

### Module 4: Visualizing Anything
- **Objective:** 3D rendering of full systems.
- **Topics:** `view()`. Native MolSysViewer vs. third-party tools.

---

## Phase 2: Surgeon (Interaction & Anatomy)
*Goal: Extract, modify, and navigate the biological hierarchy.*

### Module 5: Selection Language Basics
- **Objective:** Talk to the system precisely.
- **Topics:** Standard keywords, logic, and proximity operators.

### Module 6: Interactive Selection
- **Objective:** Mouse-to-Python synchronization.
- **Topics:** Pick residues in 3D and fetch indices into scripts.

### Module 7: Programmatic Extraction (`get`)
- **Objective:** Turn molecular systems into raw data.
- **Topics:** Extracting coordinates (the 3D tensor) and names.

### Module 8: Unit Safety with PyUnitWizard
- **Objective:** Physical consistency across the MolSysSuite.
- **Topics:** Default units, global configuration, and agnosticism.

### Module 9: System Modification (`set`)
- **Objective:** Edit systems in memory.
- **Topics:** Moving atoms and renaming biological units in native objects.

### Module 10: Discovery & Attributes
- **Objective:** Audit technical capabilities.
- **Topics:** `has_attribute()` and the attribute taxonomy.

### Module 11: Hierarchical Levels
- **Objective:** The biological hierarchy (Atom to Entity).
- **Topics:** Understanding the "Group" vs "Residue" convention.

### Module 12: Navigating Between Levels
- **Objective:** Map information between biological scales.
- **Topics:** Jumping between Atoms, Groups, and Entities with `get()`.

### Module 13: Iterating over Hierarchies
- **Objective:** Efficient processing of massive systems.
- **Topics:** The `Iterator()` function and chunked processing.

### Module 14: System Auditing and Curing
- **Objective:** Diagnosing broken data.
- **Topics:** Gaps, missing atoms, and missing bonds with `msm.build`.

### Module 15: Covalent Connectivity
- **Objective:** Master the covalent skeleton.
- **Topics:** Bonded pairs, blocks, and NetworkX graphs.

### Module 16: Comparing Systems
- **Objective:** Verify identity and consistency.
- **Topics:** Topological vs. Structural similarity with `compare()`.

### Module 17: Semantic Labeling
- **Objective:** Professional nomenclature for reports.
- **Topics:** `get_label()` and custom nomenclature templates.

### Module 18: Merging and Growing Systems
- **Objective:** Combine different systems into one.
- **Topics:** `merge()`, `add()`, and concatenating trajectories (`concatenate_structures`).

### Module 19: Surgical Extraction and Removal
- **Objective:** Isolate components and clean systems.
- **Topics:** `extract()`, `remove()`, and safe duplication with `copy()`.

---

## 🗺️ The Crossroads: Specialized Domains

### Module 20: The Specialized Domains (The Atlas)
- **Objective:** Get an overview of the full library capabilities.
- **Topics:** Brief introduction to `build`, `structure`, `topology`, `physchem`, `hbonds`, `pbc`, and `molecular_mechanics`. Preparing for the specialized paths.

---

## 🛣️ Branching Point: Specialized Paths (Modules 21-50)

From this point forward, the curriculum branches into four specialized domains. Each path applies Phases 3 to 6 to a distinct computational challenge:

1.  **Path A: Peptide-Based Inhibition of Amyloid-Beta Aggregation.**
2.  **Path B: Rational Engineering of Plastic-Degrading Enzymes.**
3.  **Path C: Binding Affinity Optimization of Antiviral Inhibitors.**
4.  **Path D: Dynamic Analysis of Membrane-Embedded Ion Channels.**

---

## Phase 3: Architect (Editing & Building)
*(Starts at Module 21 in each path)*

### Module 21: Solvation & Ion Engineering
- **Objective:** Hydrate the system for simulation.
- **Topics:** `solvate()`, `make_water_box()`, and salt concentrations.

### Module 22: Mutagenesis & Structural Repair
- **Objective:** Fix gaps and change residues.
- **Topics:** `mutate()`, adding hydrogens, and heavy atom reconstruction.

### Module 23: Peptide Synthesis
- **Objective:** Build structures from sequences.
- **Topics:** `build_peptide()` and terminal cappings.

### Module 24: Attribute Engineering (Patching)
- **Objective:** Fix IDs and names programmatically.
- **Topics:** Correcting atom names or chain IDs in a defective topology without rebuilding.

### Module 25: Conformational Engineering
- **Objective:** Rotate dihedrals to fix clashes or prepare states.
- **Topics:** `set_dihedral_angles()` and `shift_dihedral_angles()`.

### Module 26: PDB Bioassemblies & AltLocs
- **Objective:** Handle complex structural records.
- **Topics:** `make_bioassembly()` and solving alternate locations.

### Module 27: The MolSysBuilder API
- **Objective:** High-level declarative building.
- **Topics:** The `editable()` entrypoint and custom building from scratch.

---

## Phase 4: Data Analyst (Geometric & Physical Analysis)

### Module 28: Geometrical Measurements
- **Objective:** Distances, angles, and dihedrals.
- **Topics:** `get_distances()`, `get_minimum_distances()`.

### Module 29: Proximity & Neighborhoods
- **Objective:** Find what's around your ligand.
- **Topics:** `get_contacts()`, `get_neighbors()`.

### Module 30: Visualizing Interaction Matrices
- **Objective:** Instant reporting of contacts.
- **Topics:** `show_contacts()` plots.

### Module 31: Ensemble Descriptors (Global Metrics)
- **Objective:** RG, Center of Mass, RMSF.
- **Topics:** `get_radius_of_gyration()`, `get_center()`, `get_rmsf()`.

### Module 32: Comparison & Superposition
- **Objective:** Align structures and measure RMSD.
- **Topics:** `get_rmsd()`, least_rmsd_align()`, `least_rmsd_fit()`.

### Module 33: Principal Components (PCA) & Axes
- **Objective:** Analyze major modes of motion.
- **Topics:** `get_principal_axes()`, `align_principal_axes()`, and PCA.

### Module 34: Secondary Structure & Folds
- **Objective:** Characterize folding patterns.
- **Topics:** `get_secondary_structure()` (DSSP integration).

### Module 35: Hydrogen Bonds & Salt Bridges
- **Objective:** Map non-covalent networks.
- **Topics:** `get_hbonds()`, `get_salt_bridges()`.

### Module 36: Advanced H-Bond Algorithms
- **Objective:** Buch and Luzar-Chandler criteria.
- **Topics:** Donor/Acceptor inclusion rules.

### Module 37: Physicochemical Properties
- **Objective:** Mass, Charge, SASA, Volume, Hydrophobicity.
- **Topics:** `get_sasa()`, `get_charge()`, `get_volume()`. Interface analysis: `get_area_buried` and `get_buried_fraction`.

---

## Phase 5: Physics Lab (Environment & Simulation)

### Module 38: PBC Geometry & Conventions
- **Objective:** Master simulation boxes.
- **Topics:** `has_pbc()`, box shapes, lengths, and angles.

### Module 39: Wrapping & Unwrapping
- **Objective:** Handle periodicity correctly.
- **Topics:** `wrap_to_pbc()` vs `wrap_to_mic()`, and `unwrap()`.

### Module 40: Molecular Mechanics (Energies)
- **Objective:** Calculate potential energy.
- **Topics:** `get_potential_energy()`, `get_forces()`, and `MolecularMechanicsDict`.

### Module 41: Energy Minimization
- **Objective:** Optimize the structure.
- **Topics:** `potential_energy_minimization()`.

### Module 42: AMBER TLeap Integration
- **Objective:** Parametrize systems with AMBER.
- **Topics:** Using `tleap` through MolSysMT.

### Module 43: OpenMM Integration
- **Objective:** Bridge to simulation production.
- **Topics:** Direct interaction with OpenMM objects.

### Module 44: Geometric Transformations (Space)
- **Objective:** Move molecules in the box.
- **Topics:** `translate()`, `rotate()`, `center()`, `move_away()`.

---

## Phase 6: Pipeline Developer (Performance & Scaling)

### Module 45: Trajectory Management (Slicing)
- **Objective:** Master time-based data slicing.
- **Topics:** `concatenate_structures()`, frame slicing, and structure IDs.

### Module 46: Scalability & Heavy Trajectories
- **Objective:** Handle files larger than RAM.
- **Topics:** `ChunkedExecutor`, `Iterator()`, and `Reducer`.

### Module 47: Performance Optimization
- **Objective:** JIT kernels and startup speed.
- **Topics:** `warmup_numba()`.

### Module 48: Virtual Forms & Memory I/O
- **Objective:** Cloud-friendly and disk-less workflows.
- **Topics:** `string:pdb_text`, memory buffers, and resource safety.

### Module 49: Writing Your Own Form-Agnostic Functions
- **Objective:** Extend MolSysMT with your own tools.
- **Topics:** Using `@arg_digest` in custom functions.

### Module 50: Best Practices, Future & Contribution
- **Objective:** Master the MolSysMT way of coding.
- **Topics:** Design patterns, 1.x roadmap, and contributing.
