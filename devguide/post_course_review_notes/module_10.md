# Post-Review Notes: Module 10 (Navigating Hierarchies)

These points were identified during the Master review on April 21, 2026.

---

### 1. Pedagogy & Tooling
- **The Iterator Alternative:** Evaluate the introduction of a new module for `molsysmt.basic.Iterator()`. Many hierarchical queries (like "n_atoms per residue") are currently solved with `msm.get(element='group', n_atoms=True)`, but `Iterator` provides a more pythonic way to loop over systems.
- **Direct vs. Iterative:** If the `Iterator` module is added, ensure we contrast when it's better to use a single `get()` call (vectorized/fast) vs an `Iterator` (memory efficient for large systems).

### 2. Narrative
- **Simplified Language:** The term "Relational Algebra" has been removed to avoid technical friction with biological users. Ensure future modules maintain this aseptic but descriptive language ("Hierarchical Mapping").

---
**Status:** Pending implementation.
