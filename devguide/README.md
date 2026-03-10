# MolSysMT Developer Guide

This folder is the single source of truth for developer-facing conventions,
invariants, and internal policies in MolSysMT. Other files (for example,
`docs/content/developer/*`, `README.md`, and tutorials) must
align with these rules. If conflicts exist, **`devguide/` takes precedence**.

## 🚀 March 2026 Stabilization Sprint: Milestone Reached (Tag 0.14.0)
During this session, we have finalized **Phase 2** of the 1.0.0 roadmap. MolSysMT now achieves total interoperability across the structural biology and cheminformatics landscape.

**Key Achievements:**
- **Indestructible Core**: Identity and parity verified for Native, OpenMM, and MDTraj.
- **Extended Ecosystem**: Native support for RDKit, BioPython (Bio.PDB), and MDAnalysis AtomGroups.
- **Lazy Loading 2.0**: Implemented a string-based registry for instantaneous imports.
- **Visual Introspection**: MolSysViewer and NGLView are now first-class molecular systems.

## Recommended Reading Order
1) `1.0.0_maturity_audit.md` (Current state and roadmap)
2) `support_tiers.md` (Form classification)
3) `digestion_and_dependencies.md` (Lazy Loading & ArgDigest policies)
4) `forms_and_conversions.md` (Graph conversion rules)
5) `viewers_and_visualization.md` (Visual backend policy)
6) `architecture.md`
7) `element_and_native_rebuild.md`
8) `api_surface.md`
9) `testing_strategy.md`
10) `smonitor_feedback_proposals.md` (Temporary diagnostic improvements under evaluation)

## Scope
These documents define how MolSysMT should be implemented and maintained:
API boundaries, data conventions, forms, dependency rules, diagnostics, and
performance strategy. User-facing documentation lives under `docs/`, but must
follow this guidance.
