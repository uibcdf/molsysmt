# Post-Review Notes: Format Modernization (BCIF vs MMTF)

These points were identified during the Master review on April 21, 2026.

---

### 1. High-Performance Formats
- **BCIF as Standard:** Transition the entire course to use **BinaryCIF (.bcif.gz)** as the primary high-performance binary format, following the Protein Data Bank's official guidelines.
- **MMTF Deprecation:** MMTF should only be mentioned as a "supported but legacy" format. Remove it from all primary examples.

### 2. Implementation
- Verify that `systems['T4 lysozyme L99A']['181l.bcif.gz']` is used in all Common Core modules requiring a fast structural load.

---
**Status:** In progress.
