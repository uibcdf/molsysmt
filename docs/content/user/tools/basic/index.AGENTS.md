# Micro-Governance: `tools/basic/index.md` (`index.AGENTS.md`)

This micro-governance contract governs [`docs/content/user/tools/basic/index.md`](index.md).

---

## 🔒 Frozen & Inviolable Content

1. **Format Policy**:
   - MUST remain a pure MyST Markdown (`.md`) page.
   - Header H1 MUST be `# Basic`.
   - Table format MUST be a 2-column Markdown table mapping function notebook links to short descriptions (`| [Title](file.ipynb) | Description |`).
   - MUST include hidden `toctree` containing all tutorial `.ipynb` files in the directory.

2. **Function Catalog Invariant**:
   - The table and `toctree` MUST remain in sync with all user-facing tutorial notebooks in `docs/content/user/tools/basic/`.
