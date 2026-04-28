# Post-Review Notes: Sequence Analysis Relocation

These points were identified during the Master review on April 21, 2026.

---

### 1. Structural Changes
- **Module 11 Removal:** The "Sequences and Identity" module has been removed from the Common Core to maintain conceptual purity.
- **Form-Based Sequences:** Reinforce in the early modules that a sequence is a **Form** (e.g., `string:amino_acids_1`), not a special attribute.

### 2. Specialized Paths Integration
- **Alignment & Identity:** Move the sequence alignment and identity calculation tutorials to the specialized paths:
    - **Enzyme Engineering:** Compare wild-type vs. mutants.
    - **Alzheimer:** Analyze sequence conservation in Amyloid-beta across species.
- **API Reference:** Ensure these tutorials use the `msm.topology` submodule explicitly.

---
**Status:** Pending implementation in Paths A-D.
