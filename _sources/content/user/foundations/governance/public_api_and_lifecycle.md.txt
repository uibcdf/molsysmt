(user-foundations-governance-public-api-and-lifecycle)=
# Public API & Lifecycle Standards

MolSysMT enforces strict architectural boundaries between user-facing public APIs and internal private implementation modules.

---

## Public vs. Private Boundaries

- **Public APIs (`molsysmt.*`)**: Functions and classes exported in package top-level `__init__.py` modules intended for end users. All public functions are guarded by the `@digest` decorator.
- **Private Helpers (`molsysmt._private.*`)**: Internal helper functions designed for high-speed focused logic. Private helpers **must never** use the `@digest` decorator and are never exposed directly in public user APIs.

---

## API Lifecycle Integrity

Any addition or modification to the public API is considered incomplete until four lifecycle requirements are satisfied:

1. **Docstring Standards**: NumPy-style docstrings with a gerund summary line, detailed parameters, returns, and deterministic doctests.
2. **User Guide Coverage**: Updating relevant Foundations, Toolbox, and Cookbook documentation pages.
3. **Master Course Alignment**: Verifying and updating corresponding modules of *The Four Paths of the MolSysMT's Master* course.
4. **Deprecation Policy**: Obsoleted functions follow a transparent deprecation cycle, issuing user warnings before removal across minor releases.
