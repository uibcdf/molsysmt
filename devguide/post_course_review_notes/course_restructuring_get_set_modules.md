# Post-Course Review Notes: Course Restructuring (Core Verbs)

These points were identified during the Master review on April 21, 2026.

---

### 1. New Modules in Common Core
To align the course with the "Golden Quartet" of MolSysMT, we need to insert two dedicated modules:

- **New Module 7: Programmatic Data Extraction with `get()`**
    - Focus: Deep dive into the `get()` function.
    - Contrast: `get()` (Data) vs `info()` (Visual).
    
- **New Module 8: System Modification with `set()`**
    - Focus: Deep dive into the `set()` function.
    - Requirements: Explain the need for mutable forms (like `molsysmt.MolSys`).
    - Reference: Link to the full list of modifiable attributes in the User Guide.

- **New Module 11: Iterating over Hierarchies with `Iterator()`**
    - Focus: Loop over groups, chains or entities programmatically.
    - Contrast: When to use `get()` (fast/vectorized) vs `Iterator()` (memory efficient/sequential).
    - Importance: Crucial for Phase 6 (Heavy Trajectories).

---
**Status:** Pending implementation (will require re-numbering modules 7-50).
