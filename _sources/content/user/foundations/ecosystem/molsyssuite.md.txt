(user-foundations-ecosystem-molsyssuite)=
# MolSysSuite

MolSysSuite is an integrated open-source collection of computational biophysics software packages developed at UIBCDF. Designed to cover structural molecular modeling, trajectory manipulation, 3D visualization, AI-assisted workflows, topological analysis, pharmacophore identification, elastic network dynamics, and database query management, MolSysSuite provides a unified ecosystem for molecular simulations and structural bioinformatics.

---

## MolSysMT

MolSysMT is the foundational molecular systems, topology, and trajectory kernel of the suite. It provides a form-agnostic bridge across third-party Python structural biology libraries (MDTraj, OpenMM, MDAnalysis, ParmEd, PyTraj, BioPython, OpenFF, RDKit, NetworkX), zero-copy array operations, a declarative selection engine, and unit-safe data manipulation.

---

## MolSysViewer

MolSysViewer is the native 3D WebGL visualization widget of the suite. Engineered for interactive Jupyter Notebook, JupyterLab, and web application environments, it enables high-performance 3D rendering, custom molecular representations, shape overlays, dynamic selections, and synchronized session state management.

---

## MolSys-AI

*(Under development)*

MolSys-AI is the AI-assisted agentic assistant and workflow automation package of the suite. It enables natural language query interpretation, automated simulation protocol assembly, intelligent trajectory diagnostics, and agent-driven biophysical analysis.

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

MolSysSuite relies on a dedicated suite of core software engineering and governance libraries developed to ensure strict numerical safety, lazy loading, boundary validation, and testing integrity across all suite packages.

### PyUnitWizard

PyUnitWizard standardizes physical unit handling, dimensional consistency checks, and Fast-Track unit bypass across Python scientific packages. It ensures seamless inter-conversion between unit libraries (Pint, OpenMM units, PyUnitWizard native quantities) and zero-overhead numerical extraction for high-performance array operations.

### ArgDigest

ArgDigest provides a declarative public boundary validation framework for Python packages. By decorating public API functions with `@digest`, ArgDigest validates argument contracts, sanitizes input types, handles default values, and enables explicit trusted delegation without boilerplate validation logic inside internal methods.

### DepDigest

DepDigest is the centralized dependency management infrastructure for MolSysSuite. It manages soft dependency registration, lazy loading, and runtime package availability inspection, ensuring that optional third-party packages are never imported at top-level load time.

### SMonitor

SMonitor is an execution monitoring, structured diagnostics, and warning catalog system. It provides catalog-driven warning protocols, diagnostic tracing, and execution monitoring to maintain operational transparency and error reporting across suite packages.

### Pytest-Receptor

Pytest-Receptor provides testing infrastructure, fixtures, and deterministic verification frameworks tailored for receptor-aware computational biophysics workflows and structural modeling test suites.
