# Sub-Portal Governance: `tools/form/` (`AGENTS.md`)

This document defines the normative governance rules and consensus template for all documentation units under `docs/content/user/tools/form/` (including `class/`, `file/`, and `string/`).

---

## 🧭 Scope & Purpose

Houses documentation units for all representation forms supported by MolSysMT, detailing their technical identity, supported attribute portfolios, implemented adapter operations, and conversion matrices.

---

## 📐 Canonical Form Notebook Structure & Inviolable Cell Sequence

Every Form notebook (`<form_name>.ipynb`) must strictly adhere to the following 6-cell structure:

1. **Cell 1 (Code, metadata `{"tags": ["remove-input"]}`)**:
   Warning suppression block:
   ```python
   # This cell is removed with the tag: "remove-input"
   # As such, it will not be shown in documentation
   import warnings
   warnings.filterwarnings('ignore')
   ```

2. **Cell 2 (Markdown - Header & Metadata Block)**:
   - Target anchor `(Tutorial_Form_<normalized_form_id>)=`
   - Clean H1 title `# <Form Clean Name>` (e.g., `# MolSys`, `# Topology`, `# PDB`)
   - One-line italic summary: `*<Concise description of the form>*`
   - Technical metadata bullet points:
     - `- **Technical Form Name:** \`<form_name>\``
     - `- **Form Type:** \`class\` | \`file\` | \`string\``
     - `- **Origin / Library:** <Library or Native Specification>`
   - `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation admonition:
     ```myst
     :::{admonition} API documentation
     :class: dropdown

     - Python class / format reference: {class}`...` or format spec
     - Form adapter module: {mod}`molsysmt.form.<form_module>`
     :::
     ```
   - H2 Section `## Overview`: Conceptual summary explaining the data model, purpose, and role of this form within MolSysMT.

3. **Cell 3 (Markdown - Supported Attributes)**:
   - H2 Section `## Supported attributes`
   - Concise introductory sentence stating the total number of supported attributes.
   - **Single unified Markdown table** categorizing all supported attributes by Domain/Level (Topological, Structural, Mechanical).
   - **Rule:** No code cells or execution examples in this section.

4. **Cell 4 (Markdown - Implemented Operations)**:
   - H2 Section `## Implemented operations`
   - Introductory sentence pointing to `{mod}`molsysmt.form.<form_module>``.
   - Table with columns:
     - `Function / Module`: Exact function or submodule name linked to its API reference via Sphinx/MyST (`{func}` or `{mod}`).
     - `Description`: Clear explanation of the operation performed on this form.
   - Collapsible note:
     ```myst
     :::{note}
     :class: dropdown

     Each form adapter in MolSysMT implements only the specific functions that are meaningful for its data model.
     :::
     ```

5. **Cell 5 (Markdown - Supported Conversions)**:
   - H2 Section `## Supported conversions`
   - Introductory sentence pointing to direct conversion routines in `{mod}`molsysmt.form.<form_module>``.
   - Table with columns:
     - `Target Form`: Target form name (e.g., `openmm.Topology`, `file:pdb`, `string:pdb_text`).
     - `Form Type`: `class` | `file` | `string`.
     - `API Documentation`: Direct Sphinx/MyST link to the converter function `{func}`~molsysmt.form.<source>.to_<target>.to_<target>``.

6. **Cell 6 (Markdown - Related Tools & References)**:
   - Collapsible `{seealso}` dropdown:
     ```myst
     :::{seealso}
     :class: dropdown

     **Foundations & Object Architecture:**
     - <Links to relevant user foundations documents>

     **Form Tools & Conversions:**
     - {ref}`Convert <Tutorial_Convert>`: Converting between any molecular system representations with {func}`molsysmt.basic.convert`.
     - {ref}`Get attributes <Tutorial_Form_Get_attributes>`: Querying all supported attributes for any form with {func}`molsysmt.form.get_attributes`.
     - {ref}`Has attribute <Tutorial_Form_Has_attribute>`: Testing attribute availability for a form with {func}`molsysmt.form.has_attribute`.
     :::
     ```

---

## 🔒 Micro-Governance Pairing Rule

- Every single notebook under `docs/content/user/tools/form/` must have a paired `<notebook_name>.ipynb.AGENTS.md` file specifying its exact cell layout, attributes portfolio, adapter functions, and conversion targets.
