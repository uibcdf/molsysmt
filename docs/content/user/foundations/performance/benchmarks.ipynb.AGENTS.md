# Micro-Governance: `benchmarks.ipynb` (`benchmarks.ipynb.AGENTS.md`)

This micro-governance contract governs [`docs/content/user/foundations/performance/benchmarks.ipynb`](benchmarks.ipynb).

---

## 🔒 Directives

1. **Title & MyST Anchor**:
   - Title MUST be `# Benchmarks`.
   - MUST preserve top anchor `(user-foundations-performance-benchmarks)=`.

2. **Table Formatting & Status**:
   - Displays the producer-defined competitive timing matrix against MDTraj,
     MDAnalysis, and SciPy where the benchmark operation uses it.
   - Values MUST be loaded from the published competitor baseline, never maintained as
     independent timing literals in the notebook.
   - Temporarily frozen; pending expansion documented in `devguide/pending_proposals/benchmarks_future_expansion.md`.
