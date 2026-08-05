(user-foundations-entrance-navigating-documentation)=
# Navigating the Documentation

The MolSysMT documentation is organized into complementary sections designed to support users at every stage of their workflow — whether you need a 5-minute quickstart or a deep conceptual understanding.

---

## Quickstart Guide
If you want an immediate hands-on feeling for MolSysMT, skip directly to the interactive Quickstart tutorial in the **{doc}`Showcase <../../../showcase/index>`** section:
- **{doc}`Quickstart Guide <../../../showcase/quickstart>`**  
Load a system, inspect basic topological attributes, perform simple selections, and run basic transformations in minutes.

---

## Foundations
If you are starting a new research project or want to understand the architectural philosophy and data models behind MolSysMT, explore the 8 sections of **{doc}`Foundations <../index>`** step by step:
1. **{doc}`Entrance <index>`**: Mission statement, installation, and documentation roadmap.
2. **{doc}`Molecular System <../molecular_system/index>`**: The internal representation model, structural axes, and attributes.
3. **{doc}`Native World <../native_world/index>`**: Working natively with `molsysmt.MolSys`, `molsysmt.Topology`, and `molsysmt.Structures`.
4. **{doc}`Language <../language/index>`**: Mastering the selection syntax, query semantics, and form conversions.
5. **{doc}`Performance <../performance/index>`**: Parallel execution, Rust kernels, and memory efficiency for large trajectories.
6. **{doc}`Governance <../governance/index>`**: Standards, data invariants, and error-handling principles.
7. **{doc}`Support <../support/index>`**: Supported forms, tier stability guarantees, and diagnostic logging.
8. **{doc}`Ecosystem <../ecosystem/index>`**: Integration with the broader **MolSysSuite** stack and third-party ecosystems.

---

## Tools
When you need to look up function signatures, tutorials, or usage examples for specific tools, consult the **{doc}`Tools <../../tools/index>`** section:
- **{doc}`Basic <../../tools/basic/index>`**: Core operations (`get`, `set`, `select`, `convert`, `build`, `view`, `compare`).
- **{doc}`Build <../../tools/build/index>`**: Structure preparation, missing heavy atoms, cappings, protonation at pH, and solvation.
- **{doc}`Structure <../../tools/structure/index>`**: RMSD, distances, SASA, radius of gyration, superposition, and dihedrals.
- **{doc}`Topology <../../tools/topology/index>`**: Bond matrices, covalent paths, sequence extractions, and secondary structure.
- **{doc}`Elements <../../tools/element/index>`**: Selection and manipulation by atom, group, component, molecule, or chain.
- **{doc}`Third Party <../../tools/third_party/index>`**: Specialized bridges to OpenMM, MDAnalysis, MDTraj, ParmEd, RDKit, and NGLView.

---

## Cookbook
If you want to see how multiple tools combine to solve complete scientific tasks, consult the **{doc}`Cookbook <../../cookbook/index>`**:
- Multi-step system preparation and solvation pipelines.
- Trajectory alignment and structural fluctuation analysis.
- Converting complex multi-file trajectories into clean native H5MSM files.

---

## Master Course
If you want a systematic, step-by-step training curriculum from beginner to advanced mastery, follow **{doc}`The Four Paths of the MolSysMT Master <../../../course/index>`**:
- A 156-notebook comprehensive course covering foundational theory, hands-on tutorials, applied case studies, and advanced engineering paths.

---

## Showcase
If you are interested in exploring complex integrations and visualization workflows, browse the **{doc}`Showcase <../../../showcase/index>`**:
- End-to-end notebooks demonstrating seamless interoperation with OpenMM simulations, MDAnalysis trajectory processing, and interactive MolSysViewer / NGLView visualizations.

---

## Documentation Formats

Throughout the documentation, you will encounter two types of pages:

1. **Conceptual Guides (`.md`)**: Written in MyST Markdown, these narrative pages explain architectural principles, design choices, and conceptual frameworks without requiring code execution.
2. **Interactive Notebooks (`.ipynb`)**: Executable Jupyter Notebooks with live Python code cells, structured outputs, and 3D visual representations. You can download and run them locally or execute them directly in your Python environment.
