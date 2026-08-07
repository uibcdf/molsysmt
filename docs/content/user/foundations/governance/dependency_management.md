(user-foundations-governance-dependency-management)=
# Dependency Management

MolSysMT seamlessly interoperates with dozens of third-party libraries across the structural biology ecosystem without forcing users to install bloated monolithic environments.

---

## Hard vs. Soft Dependencies

Dependency status is managed centrally through **`molsysmt._depdigest`**:

- **Hard Dependencies**: Core essential libraries required for basic operation (e.g. NumPy, SciPy, PyUnitWizard, ArgDigest, SMonitor).
- **Soft Dependencies**: Optional feature-enabling packages (e.g. MDTraj, OpenMM, MDAnalysis, ParmEd, PyTraj, NGLView, PDBFixer, BioPython, Plotly).

---

## Lazy Imports and Capability Enforcement

- **Lazy Import Policy**: Soft dependencies are never imported at top-level module evaluation. They are imported inside functions or methods on demand.
- **The `@dep_digest` Decorator**: Functions requiring optional libraries use `@dep_digest(library)` to verify availability before execution, offering clear installation instructions if missing.
- **Capability Filtering**: Users can query installed ecosystem capabilities dynamically via `molsysmt.configure.show_all_capabilities`.
