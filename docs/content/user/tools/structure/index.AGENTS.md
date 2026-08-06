# Micro-Governance: `tools/structure/index.md` (`index.AGENTS.md`)

This micro-governance contract governs [`docs/content/user/tools/structure/index.md`](index.md).

---

## 🔒 Frozen & Inviolable Content

1. **Format Policy**:
   - MUST remain a pure MyST Markdown (`.md`) page.
   - Header H1 MUST be `# Structure`.
   - Table format MUST be a 2-column Markdown table mapping function tutorial links to short descriptions (`| [Title](file.ipynb) | Description |`).
   - MUST include hidden `toctree` containing all tutorial `.ipynb` files in `docs/content/user/tools/structure/`.

2. **Function Catalog Invariant**:
   - The table and `toctree` MUST remain in sync with all user-facing tutorial notebooks in `docs/content/user/tools/structure/`.
