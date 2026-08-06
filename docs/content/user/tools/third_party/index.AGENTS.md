# Micro-Governance: `tools/third_party/index.md` (`index.AGENTS.md`)

This micro-governance contract governs [`docs/content/user/tools/third_party/index.md`](index.md).

---

## 🔒 Frozen & Inviolable Content

1. **Format Policy**:
   - MUST remain a pure MyST Markdown (`.md`) page.
   - Header H1 MUST be `# Third Party`.
   - Table format MUST be a 2-column Markdown table mapping package sub-indexes to short descriptions (`| [Title](sub/index.md) | Description |`).
   - MUST include hidden `toctree` containing all third-party sub-index files (`nglview/index.md`, `openmm/index.md`).

2. **Function Catalog Invariant**:
   - The table and `toctree` MUST remain in sync with all third-party sub-indexes in `docs/content/user/tools/third_party/`.
