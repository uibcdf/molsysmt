# Micro-Governance: `molsysmt_Structures.md` (`molsysmt_Structures.md.AGENTS.md`)

Governs `docs/content/user/foundations/native_world/classes/molsysmt_Structures.md`.

## 🔒 Directives
- Title MUST be `# Structures` (no `molsysmt.` prefix).
- MUST preserve top anchor `(user-foundations-native-world-classes-molsysmt-structures)=`.
- Internal attributes table MUST faithfully list all frame observables (`coordinates`, `velocities`, `box`, `time`, `structure_id`, `b_factor`, `occupancy`, `alternate_location`, `temperature`, `potential_energy`, `kinetic_energy`).
- Headings MUST follow balanced 2-3 word standard without `&`.
- Includes links to existing native-query and conversion API targets; do not invent per-form API page paths.

Preserve shape-only human inspection: no validation, quantity conversion or array
rendering; an undeclared atom axis and an explicit zero-length axis are distinct.
