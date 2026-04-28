# Post-Review Notes: Module 13 (Comparing Systems)

These points were identified during the Master review on April 21, 2026.

---

### 1. Terminology & Precision
- **Structural vs Topological:** Strictly enforce the MolSysMT definition in the course:
    - **Topological Comparison:** Checking identity of atoms, groups, bonds, and sequence.
    - **Structural Comparison:** Checking coordinates, RMSD, and spatial poses.
- **Suite-wide Audit:** Audit all 50 modules to ensure the word "Structural" is not used as a synonym for "Molecular" or "Systemic".

### 2. Pedagogy
- **Implicit vs Explicit:** Reinforce that `msm.compare()` is the high-level entry point, but functions like `msm.topology.is_identical()` or `msm.structure.get_rmsd()` are the specialized tools for deep dives.

---
**Status:** Pending implementation.
