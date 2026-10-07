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

## Scientific Coverage

A preparation tool can return an incomplete modeled system when a reconstruction
is outside its validated coverage. Native heavy-atom repair reports those gaps;
the same limits apply when mutation or terminal capping delegates to that tool.
Inspect unresolved inventories and diagnostics before using the result. A target
group name, a completed terminus or matching atom counts do not establish complete
chemistry, a validated conformation or an energy minimum. An explicitly selected
optional engine has its own reconstruction policy; there is no automatic fallback.
See {ref}`Tutorial_Mutate` and {ref}`Tutorial_Add_missing_terminal_cappings`.
