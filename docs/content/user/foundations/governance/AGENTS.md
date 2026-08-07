# Section: Governance Directives (`AGENTS.md`)

This guide governs all content under `docs/content/user/foundations/governance/`.

## 🧭 Subdirectory Purpose & Scope
Cover constitutional rules, physical units (PyUnitWizard & fast-track conversion), argument digestion (@digest & ValidatedPayload passports), public API lifecycle standards, dependency management (molsysmt._depdigest & soft dependencies), global package configuration (molsysmt.configure), numeric precision/data standards, and reliability diagnostics with SMonitor.

## 📄 Pages List & Paired Micro-`AGENTS.md` Files
- `index.md` ➔ `index.AGENTS.md`: Group landing page with `toctree`.
- `quantities_and_units.md` ➔ `quantities_and_units.md.AGENTS.md`: Physical units and PyUnitWizard fast-track rules.
- `argument_digestion.md` ➔ `argument_digestion.md.AGENTS.md`: Argument digestion, @digest decorator, and ValidatedPayload passports.
- `public_api_and_lifecycle.md` ➔ `public_api_and_lifecycle.md.AGENTS.md`: Public vs _private boundaries, lifecycle integrity, and deprecation policy.
- `dependency_management.md` ➔ `dependency_management.md.AGENTS.md`: Hard vs Soft dependencies, molsysmt._depdigest, and lazy imports.
- `configuration_options.md` ➔ `configuration_options.md.AGENTS.md`: Global package configuration options (molsysmt.configure).
- `precision_and_types.md` ➔ `precision_and_types.md.AGENTS.md`: Numeric precision standards (float32/float64) and string ID normalization.
- `smonitor_and_telemetry.md` ➔ `smonitor_and_telemetry.md.AGENTS.md`: Diagnostic monitoring, memory pressure warnings, and SMonitor integration.

## 📐 Foundations Editorial & Style Standards
- **Conceptual Scope**: Pages in `foundations/` explain conceptual architecture, design principles, and governance standards. They do NOT document specific function API signatures, nor do they include `tools/` artifacts such as `:::{versionadded}`, top italic gerund summaries (`*Doing...*`), or API function `{seealso}` boxes.
- **Published Table Formatting Standard**: All tables MUST expand to full line width (`class="table"`, `width: 100%`), feature zebra striping, and have all headers and cells left-aligned (`text-align: left`).
- **Concise Section Titles**: Headings (`H2`, `H3`) must be brief, crisp, and direct (typically 2 to 4 words).
- **Nested Toctree Chaining**: References to index pages in `toctree` directives MUST use relative index paths without `.md` extensions (e.g. `governance/index`).
