(user-foundations-entrance-what-is-molsysmt)=
# What is MolSysMT?

**MolSysMT** (*Molecular Systems Multi-Toolkit*) is a Python library built to handle, prepare, query, transform, analyze, and visualize molecular models through **one uniform API**.

In computational structural biology and molecular simulation, taking a research project from raw coordinates to scientific insight typically requires chaining four or five different software libraries — each with its own incompatible object model, naming conventions, and file formats. Research groups frequently spend up to 70% of their time writing brittle "glue code", manually converting file formats, repairing incomplete structures, and fixing lost physical units. 

**MolSysMT was created to eliminate this technical friction entirely.**

---

## The Form-Agnostic Paradigm

The foundational principle behind MolSysMT is **Form Agnosticism**. MolSysMT abstracts away the underlying storage medium and representation layer. It does not matter whether your molecular model lives as a PDB or mmCIF file on disk, an OpenMM `Topology` object in memory, an MDAnalysis `Universe`, an MDTraj `Trajectory`, or an interactive NGLView canvas.

Rather than forcing you to learn specialized accessors for every individual tool, MolSysMT provides a single, intuitive vocabulary of core operations — such as `get`, `set`, `select`, `convert`, `build`, `view`, and `compare` — that behave identically across **89 supported forms** (including 75 Tier-1 fully guaranteed representations).

---

## Core Architectural Pillars

### 1. Universal Interoperability & Zero-Loss Bridges
MolSysMT acts as a universal bridge across files, web databases, and third-party object models. It connects your workflows without requiring you to abandon the tools you already rely on. Every conversion carries explicit fidelity tracking so you always know exactly which attributes are preserved.

### 2. Native Structure Preparation Pipeline
Structure preparation — diagnosing missing heavy atoms, adding terminal cappings, placing hydrogens at specific pH values, solvating in water boxes, and neutralizing with counterions — is implemented directly within MolSysMT. You can prepare simulation-ready models natively without requiring external tools like PDBFixer or OpenMM.

### 3. Native High-Performance Compute in Rust
Analytical operations (including pairwise distances, neighbor lists, RMSD, structural superposition, radius of gyration, RMSF, principal component axes, SASA, and dihedral angles) are powered by precompiled Rust compute kernels. They run with **zero JIT compilation warmup**, zero startup latency, and configurable multi-threaded execution.

### 4. Physical Safety & Unit Consistency
All physical quantities in MolSysMT carry explicit physical units powered by `pyunitwizard` (nanometers, picoseconds, radians, elementary charges, Kelvin). Unit conversions, array dimensions, and coordinate invariants are validated automatically to safeguard scientific integrity.

---

## The Engine of MolSysSuite

MolSysMT serves as the foundational "Operating System" for molecular data within the [**MolSysSuite**](https://www.uibcdf.org/) ecosystem developed at the UIB-CDF. Higher-level specialized libraries — such as **TopoMet** for topological analysis, **ElastNetMT** for elastic network models, and **MolSysViewer** for 3D web visualization — rely on MolSysMT as their underlying data engine.

---

:::{admonition} Explore at Your Own Pace
:class: note
You will have the opportunity to test and verify every one of these architectural capabilities through hands-on code examples, interactive 3D visualizations, and step-by-step tutorials throughout the subsequent sections of this **User Guide**.
:::

:::{admonition} Key Takeaway
:class: tip
MolSysMT acts as the unified **Operating System** for your molecular data. It provides a single, form-agnostic API to build, prepare, query, transform, analyze, and visualize systems without changing libraries every time your research task changes.
:::
