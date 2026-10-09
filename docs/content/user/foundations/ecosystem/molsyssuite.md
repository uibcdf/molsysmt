(user-foundations-ecosystem-molsyssuite)=
# MolSysSuite

MolSysSuite is an integrated open-source collection of computational biophysics software packages developed at UIBCDF. It covers structural molecular modeling, molecular docking, trajectory manipulation, 3D visualization, AI-assisted workflows, topological analysis, pharmacophore identification, and elastic network dynamics.

Sabueso belongs to MOLI's Scientific Context and can provide knowledge to MolSysSuite workflows.

---

## MolSysMT

MolSysMT is the foundational molecular systems, topology, and trajectory kernel of the suite. It provides a form-agnostic bridge across third-party Python structural biology libraries (MDTraj, OpenMM, MDAnalysis, ParmEd, PyTraj, BioPython, OpenFF, RDKit, NetworkX), zero-copy array operations, a declarative selection engine, and unit-safe data manipulation.

---

## MolSysViewer

MolSysViewer is the native 3D WebGL visualization widget of the suite. Engineered for interactive Jupyter Notebook, JupyterLab, and web application environments, it enables high-performance 3D rendering, custom molecular representations, shape overlays, dynamic selections, and synchronized session state management.


MolSysViewer uses MolSysMT as its native backend. No separate MolSysMT addon or `view.addons.molsysmt` namespace is required. Use native Viewer workflows, or calculate with public MolSysMT tools and reload or reconcile the result through the Viewer API.

---

## MolSys-AI

*(Under development)*

MolSys-AI is the specialist AI subsystem for MolSysSuite. It is being developed to assist with scientific workflows, interpretation, and use of the suite's tools.

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

## DockingMT

*(Under development)*

DockingMT is the molecular docking component of the suite. It provides reproducible, inspectable docking workflows and integrates molecular inputs from MolSysMT with docking engines.

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
