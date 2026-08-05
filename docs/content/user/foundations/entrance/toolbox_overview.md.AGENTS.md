# Micro-Governance: `toolbox_overview.md` (`toolbox_overview.md.AGENTS.md`)

This micro-governance contract governs [`docs/content/user/foundations/entrance/toolbox_overview.md`](toolbox_overview.md).

---

## 🔒 Frozen & Inviolable Content

1. **Format Policy**:
   - MUST remain a pure MyST Markdown (`.md`) page without code cells.

2. **Mandatory MyST Section Anchor & H1**:
   - `(user-foundations-entrance-toolbox-overview)=`
   - Header H1 MUST be `# Overview of Tools`

3. **Inviolable Tool Sections (Without "Box" in H2 Headings)**:
   - **`## Basic`**: Must link to `../../tools/basic/index`.
   - **`## Form`**: Must link to `../../tools/form/index`.
   - **`## Element`**: Must link to `../../tools/element/index`.
   - **`## Build`**: Must link to `../../tools/build/index`.
   - **`## Structure`**: Must link to `../../tools/structure/index` (stipulating nm units, `(n_structures, n_atoms, 3)` shape, 3x3 rotation matrices, precompiled Rust kernels).
   - **`## Topology`**: Must link to `../../tools/topology/index`.
   - **`## PBC`**: Must link to `../../tools/pbc/index`.
   - **`## Physchem`**: Must link to `../../tools/physchem/index`.
   - **`## Molecular Mechanics`**: Must link to `../../tools/molecular_mechanics/index`.
   - **`## Hbonds`**: Must link to `../../tools/hbonds/index`.
   - **`## Third Party`**: Must link to `../../tools/third_party/index`.

4. **Required Navigation Admonition**:
   - Must present the distinction between the **{doc}`Tools User Guide <../../tools/index>`** (tutorials per function) and the **{doc}`Technical API Documentation <../../../../api/index>`** (docstring specifications) inside an `{admonition}` note box at the end of the page.
