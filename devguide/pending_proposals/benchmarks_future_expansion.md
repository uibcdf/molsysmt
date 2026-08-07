# Proposal: Future Expansion of Benchmarks Suite and Documentation

> **Status:** Pending Future Revision  
> **Date:** August 2026

## 🎯 Overview
The current `benchmarks.ipynb` in `docs/content/user/foundations/performance/` includes a baseline competitive matrix comparing MolSysMT Public API, MolSysMT Native Rust Kernels, MDTraj, MDAnalysis, and SciPy.

## 📋 Action Items for Future Revision
1. **Live Automated Benchmarks**: Expand the benchmarking suite in `benchmarks/` to run automated throughput passes on CI/CD releases.
2. **Detailed Memory Profile Charts**: Generate interactive or static memory footprint charts (RSS scaling curves over structure count) comparing Eager Path vs Heavy Path (`ChunkedExecutor`).
3. **Domain-Specific Kernels**: Add granular benchmarks for SASA integrations, minimum image conventions, RMSD superposition, and contact maps.
