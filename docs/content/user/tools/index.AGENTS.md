# Micro-Governance: `tools/index.md` (`index.AGENTS.md`)

This micro-governance contract governs [`docs/content/user/tools/index.md`](index.md).

---

## 🔒 Frozen & Inviolable Content

1. **Format Policy**:
   - MUST remain a pure MyST Markdown (`.md`) page.
   - Header H1 MUST be `# **Tools**`.
   - MUST NOT include introductory paragraphs before the grid cards; the page starts directly with the card grid following `# **Tools**`.

2. **Mandatory MyST Section Anchors**:
   - `(User_Tools)=`
   - `(user-tools-index)=`

3. **Grid Layout & Card Order Invariant**:
   - Grid MUST use `::::{grid} 1 2 2 4` with `:gutter: 2`.
   - Cards MUST use brief, direct "Set of functions to..." descriptions.
   - Cards MUST be ordered matching `toctree` from left to right, top to bottom:
     1. Basic (`basic/index`)
     2. Build (`build/index`)
     3. Topology (`topology/index`)
     4. Chemical States (`chemical_states/index`)
     5. Structure (`structure/index`)
     6. Periodic Boundary Conditions (`pbc/index`)
     7. Physicochemical Properties (`physchem/index`)
     8. Hydrogen Bonds (`hbonds/index`)
     9. Interactions (`interactions/index`)
     10. Molecular Mechanics (`molecular_mechanics/index`)
     11. Element (`element/index`)
     12. Form (`form/index`)
     13. Third Party (`third_party/index`)
     14. MolSysViewer tools (`molsysviewer_tools`)
