# Proposal: Centralized User Support, Bug Reporting & Community Channels Page

> **Status:** Pending Architectural Placement & Implementation  
> **Date:** August 2026

## 🎯 Overview

Currently, instructions for seeking help, reporting bugs, asking usage questions, or suggesting feature proposals are scattered or implicit. 

This proposal establishes a **dedicated, centralized documentation unit** explaining to users:
- **Questions & Doubts**: Where and how to ask usage questions (e.g. GitHub Discussions / Community channels).
- **Bug Reporting**: Step-by-step guidelines for filing reproducible bug reports on GitHub Issues.
- **Feature Proposals**: How to submit feature requests and architectural proposals.
- **Contact & Maintainers**: Direct contact channels with the UIBCDF maintainer team.

---

## 🧭 Architectural Placement Consideration

We must evaluate the optimal location for this centralized page:

- **Option A (Under `About` Section)**:  
  Place the unit under `docs/content/about/community_and_support.md` (or `contact.md`), since community guidelines, maintainer contacts, and governance fit naturally in the *About* portal. Cross-link to this page from Foundations, User Guide entrance, and Cookbook.

- **Option B (Under `User Guide > Entrance`)**:  
  Place it directly under `docs/content/user/foundations/entrance/support_and_community.md`.

- **Option C (Dedicated Top-Level Portal)**:  
  Expose a top-level link in `index.ipynb` or footer.

*Recommendation:* **Option A** (Centralized under `About`, with active `{ref}` cross-references across Foundations, User Guide, and Cookbook).

---

## 📋 Action Items for Implementation
1. **Draft Page Content**: Include templates for bug reports, minimal reproducible examples (MREs), and GitHub issue links.
2. **Cross-Link Integration**: Add `{ref}` cross-references across `foundations/entrance/`, `foundations/governance/`, and `cookbook/`.
3. **Sphinx Hierarchy Update**: Update `toctree` in the target portal (`about/index.md` or `entrance/index.md`).
