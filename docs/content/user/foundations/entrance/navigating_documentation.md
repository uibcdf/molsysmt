(user-foundations-entrance-navigating-documentation)=
# Navigating the Documentation

The MolSysMT documentation is organized into complementary sections designed to support users at every stage of their workflow — whether you need a 5-minute quickstart or a deep conceptual understanding.

---

## Quickstart Guide
If you want an immediate hands-on feeling for MolSysMT, skip directly to the interactive Quickstart tutorial in the Showcase section:
- **{doc}`../../../showcase/quickstart`**  
Load a system, inspect basic topological attributes, perform simple selections, and run basic transformations in minutes.

---

## Foundations
If you are starting a new research project or want to understand the architectural philosophy and data models behind MolSysMT, explore the 8 sections of **Foundations** step by step:
1. **Entrance**: Mission statement, installation, and roadmap.
2. **Molecular System**: The internal representation model, structural axes, and attributes.
3. **Native World**: Working natively with `molsysmt.MolSys`, `molsysmt.Topology`, and `molsysmt.Structures`.
4. **Language**: Mastering the selection syntax, query semantics, and form conversions.
5. **Performance**: Parallel execution, Rust kernels, and memory efficiency for large trajectories.
6. **Governance**: Standards, data invariants, and error-handling principles.
7. **Support**: Supported forms, tier stability guarantees, and diagnostic logging.
8. **Ecosystem**: Integration with the broader **MolSysSuite** stack and third-party ecosystems.

---

## Tools API Reference
When you need to look up function signatures, arguments, or usage examples for a specific task, consult the **Tools API** reference:
- **Basic**: Core operations (`get`, `set`, `select`, `convert`, `build`, `view`, `compare`).
- **Build**: Structure preparation, missing heavy atoms, cappings, protonation at pH, and solvation.
- **Structure**: RMSD, distances, SASA, radius of gyration, superposition, and dihedrals.
- **Topology**: Bond matrices, covalent paths, sequence extractions, and secondary structure.
- **Elements**: Selection and manipulation by atom, group, component, molecule, or chain.
- **Third Party**: Specialized bridges to OpenMM, MDAnalysis, MDTraj, ParmEd, RDKit, and NGLView.

---

## Cookbook
If you want to see how multiple tools combine to solve complete scientific tasks, consult the **{doc}`Cookbook <../../cookbook/index>`**:
- Multi-step system preparation and solvation pipelines.
- Trajectory alignment and structural fluctuation analysis.
- Converting complex multi-file trajectories into clean native H5MSM files.

---

## The Four Paths Course
If you want a systematic, step-by-step training curriculum from beginner to advanced mastery, follow **The Four Paths of the MolSysMT Master**:
- A 156-notebook comprehensive course covering foundational theory, hands-on tutorials, applied case studies, and advanced engineering paths.

---

## Showcase
If you are interested in exploring complex integrations and visualization workflows, browse the **Showcase**:
- End-to-end notebooks demonstrating seamless interoperation with OpenMM simulations, MDAnalysis trajectory processing, and interactive MolSysViewer / NGLView visualizations.

---

## Documentation Formats

Throughout the documentation, you will encounter two types of pages:

1. **Conceptual Guides (`.md`)**: Written in MyST Markdown, these narrative pages explain architectural principles, design choices, and conceptual frameworks without requiring code execution.
2. **Interactive Notebooks (`.ipynb`)**: Executable Jupyter Notebooks with live Python code cells, structured outputs, and 3D visual representations. You can download and run them locally or execute them directly in your Python environment.
