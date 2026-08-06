# Micro-Governance: `the_molecular_system.md` (`the_molecular_system.md.AGENTS.md`)

This micro-governance contract governs [`docs/content/user/foundations/molecular_system/the_molecular_system.md`](the_molecular_system.md).

---

## 🔒 Content & Style Directives

1. **Format Policy**:
   - MUST remain a pure MyST Markdown (`.md`) narrative page without code cells.

2. **Mandatory MyST Section Anchor**:
   - `(user-foundations-molecular-system-definition)=`

3. **Core Conceptual Invariants (Must NOT be removed or altered)**:
   - **Form-Agnostic Philosophy & Attribute Heterogeneity**: Explain that a molecular system is an abstract entity independent of file format or Python class. State clearly that different forms may carry different levels of detail or subsets of attributes (e.g. `openmm.Topology` has topology but no coordinates; `mdtraj.Trajectory` has coordinates but may lack force field metadata).
   - **Form-Agnostic Functionality**: State clearly that virtually all MolSysMT functions are form-agnostic, with the sole exception of internal helper functions within the form-specific `molsysmt.form` submodules.
   - **Four Architectural Layers**: Maintain the 4 conceptual layers (Topology Layer, Structure Layer, Molecular Mechanics Layer, Chemical State Layer) with varied, non-repetitive list-opening phrasing.
   - **Single vs. Multiple-Item Systems**: 
     - *Single-Item System*: Emphasize that a single-item system does NOT need to contain every attribute; a model with missing attributes is valid and represents the system as currently defined.
     - *Multiple-Item System*: Explain how MolSysMT merges complementary items (e.g. `.prmtop` + `.inpcrd` or `.psf` + `.dcd`) into a single system.

4. **Foundations Editorial Rule**:
   - Do NOT include `tools/` function tutorial artifacts (no `:::{versionadded}`, no top italicized gerund summary line, and no function `{seealso}` boxes).
