# Foundations Index Micro-Governance (`index.AGENTS.md`)

This file defines the micro-governance rules, design constraints, and content protection contract for the main Foundations index ([`docs/content/user/foundations/index.md`](index.md)).

---

## 🔒 Frozen Content & Inviolable Requirements

1. **Title & Heading:**  
   Header H1 MUST be `# Foundations` (do NOT use `# User Guide Foundations` to maintain clean sidebar navigation).

2. **Introductory Overview:**  
   The page MUST feature a 2-paragraph conceptual overview introducing the form-agnostic philosophy and framework principles before the section grid.

3. **The 8 Foundational Subdirectory Entries:**  
   The page MUST link to all 8 thematic subdirectory index files without leading number prefixes:
   - `entrance/index.md` (The Entrance)
   - `molecular_system/index.md` (The Molecular System)
   - `native_world/index.md` (The Native World)
   - `language/index.md` (The Language)
   - `performance/index.md` (Performance)
   - `governance/index.md` (Governance)
   - `support/index.md` (Supported)
   - `ecosystem/index.md` (The Ecosystem)

4. **Toctree Structure:**  
   The hidden `toctree` block MUST maintain `:maxdepth: 2` and link directly to the 8 group `index.md` files.

---

## 🏷️ Section Anchors

- Top anchor: `(user-foundations-index)=`
