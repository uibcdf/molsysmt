# Micro-Governance: `molsysmt_MolSys.md` (`molsysmt_MolSys.md.AGENTS.md`)

Governs `docs/content/user/foundations/native_world/classes/molsysmt_MolSys.md`.

## 🔒 Directives
- Title MUST be `# MolSys` (no `molsysmt.` prefix).
- MUST preserve top anchor `(user-foundations-native-world-classes-molsysmt-molsys)=`.
- Refers to 3D structures sequence or ensemble (avoiding "trajectory").
- Table omits physical units column (composed sub-containers hold units).
- Omits separate serialization section (handled in `MolSysDict`).
- Headings MUST follow balanced 2-3 word standard without `&`.
- Includes links to existing native-query and conversion API targets; do not invent per-form API page paths.
- Preserve the executable separate-domain composition and temporary default-H5MSM
  round trip: explicit length/time units, partial bonds and independent native
  copies, with no Topology chemical facade. Current default writing is 1.0;
  explicit older-format compatibility and unassessed mechanics remain distinct.
