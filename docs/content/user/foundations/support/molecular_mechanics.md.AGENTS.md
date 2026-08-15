# Micro-Governance: `molecular_mechanics.md` (molecular_mechanics.md.AGENTS.md)

Governs `docs/content/user/foundations/support/molecular_mechanics.md`.

## 📜 Editorial Rules & Layout Standards
- **Section Layout**: Must maintain 4 distinct H2 sections (`## Forcefields and Water Models`, `## Non-Bonded and Continuum Solvent Settings`, `## Constraints and Integration Parameters`, `## Energy Evaluation and Operations`).
- **Table Formatting**: Each section MUST present a 4-column left-aligned table (`Attribute / Property`, `Scope / Options`, `Description`, `Canonical Unit`).
- **Attribute / Function Naming**: Attribute keys and API functions MUST be formatted as code blocks (e.g. `` `forcefield` ``, `` `msm.molecular_mechanics.get_potential_energy` ``).
- **Physical Units**: Physical units MUST be explicitly stated using PyUnitWizard standard canonical units (`nm`, `Da`, `e`, `M`, `kJ/mol`, `kJ/(mol*nm)`).
