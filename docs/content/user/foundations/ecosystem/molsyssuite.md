(user-foundations-ecosystem-molsyssuite)=
# MolSysSuite

MolSysSuite is an integrated open-source collection of computational biophysics software packages developed at UIBCDF. Designed to cover structural molecular modeling, trajectory manipulation, topological analysis, pharmacophore identification, elastic network dynamics, and database query management, MolSysSuite provides a unified ecosystem for molecular simulations and structural bioinformatics.

---

## MolSysMT

MolSysMT is the foundational molecular systems, topology, and trajectory kernel of the suite. It provides a form-agnostic bridge across third-party Python structural biology libraries (MDTraj, OpenMM, MDAnalysis, ParmEd, PyTraj, BioPython, OpenFF, RDKit, NetworkX), zero-copy array operations, a declarative selection engine, and unit-safe data manipulation.

---

## MolSysViewer

MolSysViewer is the native 3D WebGL visualization widget of the suite. Engineered for interactive Jupyter Notebook, JupyterLab, and web application environments, it enables high-performance 3D rendering, custom molecular representations, shape overlays, dynamic selections, and synchronized session state management.

---

## TopoMT

*(Under development)*

TopoMT is the topological analysis and molecular connectivity package of the suite. It provides covalent graph representations, contact network calculations, secondary structure topology assignment, and structural graph invariants.

---

## PharmacophoreMT

*(Under development)*

PharmacophoreMT is the 3D pharmacophore modeling package of the suite. It enables spatial feature extraction, ligand interaction field mapping, pharmacophoric query construction, and high-throughput virtual screening matching.

---

## ElastNetMT

*(Under development)*

ElastNetMT is the elastic network modeling and normal mode analysis package of the suite. It implements Anisotropic Network Models (ANM), Gaussian Network Models (GNM), coarse-grained vibrational dynamics, and conformational flexibility predictions.

---

## Sabueso

*(Under development)*

Sabueso is the biological database query and metadata parser agent of the suite. It automates information retrieval, sequence-structure mapping, entity identification, and metadata synchronization across major structural repositories (PDB, UniProt, AlphaFold DB).

---

## Infrastructure and Developer Tooling

MolSysSuite relies on a dedicated suite of core software engineering and governance libraries developed to ensure strict numerical safety, lazy loading, boundary validation, and testing integrity:

| Tooling Package | Category | Primary Function in Suite |
| :--- | :--- | :--- |
| **`PyUnitWizard`** | Physical Quantities | Standardizes physical unit handling, dimensional consistency checks, and Fast-Track unit bypass. |
| **`ArgDigest`** | Boundary Validation | Enforces contract validation and parameter digestion on public API boundaries via `@digest`. |
| **`DepDigest`** | Dependency Management | Manages centralized soft dependency registration, lazy imports, and runtime availability checks. |
| **`SMonitor`** | Diagnostics & Logging | Provides catalog-driven warning systems, structured diagnostics, and execution monitoring. |
| **`Pytest-Receptor`** | Testing Infrastructure | Receptor-aware test suite fixtures and deterministic validation frameworks. |
