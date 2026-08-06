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
     4. Structure (`structure/index`)
     5. Periodic Boundary Conditions (`pbc/index`)
     6. Physicochemical Properties (`physchem/index`)
     7. Hydrogen Bonds (`hbonds/index`)
     8. Molecular Mechanics (`molecular_mechanics/index`)
     9. Element (`element/index`)
     10. Form (`form/index`)
     11. Third Party (`third_party/index`)
