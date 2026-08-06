# Micro-Governance: `tools/index.md` (`index.AGENTS.md`)

This micro-governance contract governs [`docs/content/user/tools/index.md`](index.md).

---

## 🔒 Frozen & Inviolable Content

1. **Format & Layout Policy**:
   - MUST remain a pure MyST Markdown (`.md`) page.
   - Header H1 MUST be `# Tools`.
   - Header H2 MUST be `## **Sections**`.

2. **Mandatory MyST Section Anchors**:
   - `(User_Tools)=`
   - `(user-tools-index)=`

3. **Grid Layout & Card Order Invariant**:
   - Grid MUST use `::::{grid} 1 2 2 4` with `:gutter: 3`.
   - Cards MUST be ordered matching `toctree` from left to right, top to bottom:
     1. Basic (`basic/index`)
     2. Build (`build/index`)
     3. Topology (`topology/index`)
     4. Structure (`structure/index`)
     5. PBC (`pbc/index`)
     6. Physchem (`physchem/index`)
     7. Hbonds (`hbonds/index`)
     8. Molecular Mechanics (`molecular_mechanics/index`)
     9. Element (`element/index`)
     10. Form (`form/index`)
     11. Third Party (`third_party/index`)
