# Micro-Governance: `tools/element/index.md` (`index.AGENTS.md`)

This micro-governance contract governs [`docs/content/user/tools/element/index.md`](index.md).

---

## 🔒 Frozen & Inviolable Content

1. **Format Policy**:
   - MUST remain a pure MyST Markdown (`.md`) page.
   - Header H1 MUST be `# Element`.
   - Table format MUST be a 2-column Markdown table mapping structural tier links to short descriptions (`| [Title](sub/index.md) | Description |`).
   - MUST include hidden `toctree` containing all structural tier sub-index files (`atom/index.md`, `group/index.md`, `component/index.md`, `molecule/index.md`, `entity/index.md`, `chain/index.md`).

2. **Function Catalog Invariant**:
   - The table and `toctree` MUST remain in sync with all structural element tiers in `docs/content/user/tools/element/`.
