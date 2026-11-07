(user-foundations-governance-dependency-management)=
# Dependency Management

MolSysMT seamlessly interoperates with dozens of third-party libraries across the structural biology ecosystem without forcing users to install bloated monolithic environments.

---

## Hard vs. Soft Dependencies

Dependency status is managed centrally through **DepDigest** ([https://www.uibcdf.org/depdigest](https://www.uibcdf.org/depdigest)) via `molsysmt._depdigest`:

- **Hard Dependencies**: Core libraries required for basic operation, such as
  NumPy, pandas, PyUnitWizard, ArgDigest and SMonitor.
- **Soft Dependencies**: Optional feature-enabling packages, such as MDTraj,
  OpenMM, MDAnalysis, ParmEd, PyTraj, NGLView, PDBFixer and Biopython.

Documentation tools have a separate installation route. For example, Plotly
belongs to the `docs` extra and the documentation environment because the
NGLView showcase uses it to generate an interactive contact map. It does not
enable a MolSysMT runtime form or calculation. The development environment
also includes that documentation tool for local regeneration.

---

## Lazy Imports and Capability Enforcement

- **Lazy Import Policy**: Soft dependencies are never imported at top-level module evaluation. They are imported inside functions or methods on demand.
- **The `@dep_digest` Decorator**: Functions requiring optional libraries use `@dep_digest(library)` to verify availability before execution, offering clear installation instructions if missing.
- **Capability Inspection**: Users can inspect installed ecosystem capabilities dynamically via `molsysmt.configure.show_all_capabilities`.

Optional capabilities can also require a compatibility constraint on a
provider's transitive dependency. The `soft` extra excludes PyParsing 3.3.3 for
MDTraj input selection; this does not make either package a hard dependency.
Existing externally assembled environments must also satisfy the constraint.
See {ref}`user-foundations-support-selection-syntaxes` for the affected
comparisons, supported checked pairs and update instructions.
