# Foundations Index Micro-Governance (`index.AGENTS.md`)

This file defines the micro-governance rules, design constraints, and content protection contract for the main Foundations index ([`docs/content/user/foundations/index.ipynb`](index.ipynb)).

---

## 🔒 Frozen Content & Inviolable Requirements

1. **Title & Heading:**  
   Header H1 MUST be `# Foundations` (do NOT use `# User Guide Foundations` to maintain clean sidebar navigation).

2. **The 8 Foundational Subdirectory Entries:**  
   The page MUST link to all 8 thematic subdirectory index files:
   - `01_entrance/index.md` (1. The Entrance)
   - `02_molecular_system/index.md` (2. The Molecular System)
   - `03_native_world/index.md` (3. The Native World)
   - `04_language/index.md` (4. The Language)
   - `05_performance/index.md` (5. Performance)
   - `06_governance/index.md` (6. Governance)
   - `07_support/index.md` (7. Support & Coverage)
   - `08_ecosystem/index.md` (8. The Ecosystem)

3. **Toctree Structure:**  
   The hidden `toctree` block MUST maintain `:maxdepth: 2` and link directly to the 8 group `index.md` files.

---

## 🏷️ Section Anchors

- Top anchor: `(user-foundations-index)=`
