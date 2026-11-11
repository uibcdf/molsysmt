(user-foundations-entrance-what-is-molsysmt)=
# What is MolSysMT?

**MolSysMT** (*Molecular Systems Multi-Toolkit*) is a Python library built to handle, prepare, query, transform, analyze, and visualize molecular models through **one uniform API**.

Molecular workflows often combine libraries with different object models,
naming conventions and file formats. Transferring a system between them can
require conversion code, explicit index maps and careful unit handling.

MolSysMT provides reusable tools for those tasks so you can focus on the
scientific workflow and inspect the assumptions made at each boundary.

---

## The Form-Agnostic Paradigm

The foundational principle is **Form Agnosticism**: public functions share a
vocabulary across supported representations, including PDB/mmCIF files,
OpenMM topology objects, MDAnalysis Universes and MDTraj trajectories.

Operations such as `get`, `set`, `select`, `convert`, `view` and `compare`
reuse that vocabulary. The source must supply the required attributes and the
operation must have a supported route. A sequence does not contain coordinates;
a graphics projection need not preserve every chemical assignment. Consult
{ref}`supported forms <user-foundations-support-forms>` and their declared
tiers rather than assuming every operation works on every representation.

---

## Core Architectural Pillars

(universal-interoperability-zero-loss-bridges)=
### 1. Interoperability and Conversion Fidelity
MolSysMT connects supported files, database identifiers and third-party objects.
Inspect a conversion's declared profile and optional report to understand what
can be preserved; strict conversion refuses reported losses. An unsupported
field or route is not made lossless by using a common API. See
{ref}`converting systems <Tutorial_Convert>`.

### 2. Native Structure Preparation Pipeline
Preparation combines reusable native tools with explicitly selected optional
engines. Native assessment, bounded template repair, chemical-state handling
and index/evidence tools support larger preparation workflows. Hydrogen
placement and solvation have method-specific dependencies, including RDKit,
PDBFixer or OpenMM where declared. A successful individual step does not certify
a simulation-ready system or choose the correct chemical state for your study.

Heavy-atom assessment uses exact residue chemistry where available, including curated MSE, SEP, TPO, and MLY templates. Native repair supports bounded gaps in MSE, SEP, and TPO; MLY gaps remain unassessed because their placement has not been validated. A modified residue without a matching template is also reported as unassessed during native repair.

### 3. Native High-Performance Compute in Rust
Analytical operations, including distances, neighbor lists, RMSD, fitting,
gyration radius, RMSF, principal axes, SASA and dihedrals, reuse the bundled Rust
kernels. Binary packages require no JIT compilation warmup. Importing providers,
preparing arrays and building indexes still have costs; performance and parallel
execution depend on the operation, workload and resource policy.

### 4. Physical Safety & Unit Consistency
PyUnitWizard manages unit-bearing inputs, conversions and results. Coordinate
and box kernels use explicit nm values, time uses ps, and angles use radians at
their declared boundaries; public quantities follow the selected unit policy.
Some native numeric attributes have fixed documented units, such as partial
charge arrays in elementary charge. Unit and shape validation protect these
contracts; they do not independently validate a scientific model.

### 5. Purpose-Built Infrastructure Libraries
MolSysMT uses UIBCDF support libraries at the corresponding **MolSysSuite**
boundaries:
- **`pyunitwizard`**: Universal management, validation, and conversion of physical quantities and units.
- **`argdigest`**: Strict argument validation, normalization, and declarative function contracts at public boundaries.
- **`depdigest`**: Optional dependency checks, lazy loading and feature discovery.
- **`smonitor`**: Structured diagnostic logging, telemetry, and transparent signal instrumentation across computational workflows.

---

## The Engine of MolSysSuite

MolSysMT supplies core molecular-system representation, manipulation and general
analysis within [**MolSysSuite**](https://www.uibcdf.org/). Specialized components
can reuse those contracts: **TopoMT** studies cavities, pockets and surface
topography, **ElastNetMT** builds elastic-network models, and **MolSysViewer**
provides molecular visualization. Their scientific and graphical capabilities
retain their own scope and validation.

---

:::{admonition} Explore at Your Own Pace
:class: note
Use the **User Guide** examples to explore these contracts and their stated
limits. Consult each method's evidence and prerequisites before choosing it
for a scientific study.
:::

:::{admonition} Key Takeaway
:class: tip
MolSysMT provides a shared molecular-data API and reusable tools. Form
agnosticism preserves a common vocabulary while keeping missing information,
conversion limits and scientific assumptions explicit.
:::
