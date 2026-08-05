# Micro-Governance: `navigating_documentation.md` (`navigating_documentation.md.AGENTS.md`)

This micro-governance contract governs [`docs/content/user/foundations/entrance/navigating_documentation.md`](navigating_documentation.md).

---

## 🔒 Frozen & Inviolable Content

1. **Format Policy**:
   - MUST remain a pure MyST Markdown (`.md`) page.
   - Sections for Cookbook, Master Course, Showcase, and API Documentation MUST use fluid paragraph prose rather than single/unnecessary itemized lists.

2. **Mandatory MyST Section Anchor**:
   - `(user-foundations-entrance-navigating-documentation)=`

3. **Inviolable Resource Sections & Heading Naming**:
   - **`## Quickstart Guide`**: Must link to `../../../showcase/quickstart`.
   - **`## Foundations`**: Must link to `../index` and list the 8 Foundations sections with explicit `{doc}` links.
   - **`## Tools`**: MUST be titled `## Tools` (NOT `Tools API Reference` to avoid confusion with technical API docs). Must link to `../../tools/index` and list tool sub-portals with explicit `{doc}` links.
   - **`## Cookbook`**: Must link to `../../cookbook/index` in fluid prose.
   - **`## Master Course`**: Must link to `../../../course/index` ("The Four Paths of the MolSysMT Master") in fluid prose.
   - **`## Showcase`**: Must link to `../../../showcase/index` in fluid prose.
   - **`## API Documentation`**: Must link to `../../../../api/index` for technical low-level API reference outside the User Guide.

4. **Documentation Formats Section**:
   - Explanation distinguishing conceptual Markdown (`.md`) guides from executable Jupyter Notebooks (`.ipynb`).
