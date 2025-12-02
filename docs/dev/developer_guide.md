# 🧪 Editorial and Developer Guide for MolSysMT Documentation

This document serves as the editorial and structural guide for contributing to the documentation and development of the MolSysMT project. It covers docstring conventions, tutorial structure, internal practices, and CI/testing expectations.

---

## 🤪 Project Overview

MolSysMT is a modular scientific Python library for handling molecular systems. The project is organized around three central concepts:

- **Forms**: Representations of molecular systems (e.g., `'file:pdb'`, `'openmm.Topology'`).
- **Elements**: Hierarchical structural levels (`'atom'`, `'group'`, `'molecule'`, etc.).
- **Attributes**: Accessible properties or metadata (`coordinates`, `box`, `entity_name`, etc.).


## 📋 Jupyter Tutorial Style

Tutorials live in `docs/user_guide/tools/<module>/`. Use the `add.ipynb` tutorial as reference.

### ✅ Structure

1. Title with function name
2. Italic summary in gerund (*Retrieving attribute values...*)
3. One or two-paragraph introduction
4. `:::{admonition} API documentation` block with `{func}` link
5. Incremental examples with markdown narration
6. Varied phrasing before code blocks (avoid repetition)
7. Final `seealso` block with Markdown links

### 💬 Recommended phrasing for sections

Avoid repeating "Let's see an example..." for each element. Instead, alternate between:

- "Working with `group` elements:"
- "Example at the `atom` level:"
- "We can also extract information from `molecule` elements:"
- "Displaying summary data for `entity` elements:"

---

## 🔍 Internal Conventions

- Use `@digest` decorator for all public functions unless explicitly skipped (e.g., `get_form`).
- If an attribute is not available, `get()` returns `None`.
- `get_attributes()` supports both `dictionary` and `list` outputs.
- Always distinguish clearly between **form** and **system** in documentation.
- Native MolSysMT objects store all element IDs (`atom_id`, `group_id`, `component_id`, `molecule_id`, `chain_id`, `entity_id`) as strings; converters should normalize any numeric IDs on input, and tests/docs should assume string IDs.
- Getter functions should return Python lists (or lists of lists when nested) for collections of values instead of NumPy arrays, to keep outputs consistent across forms and examples.

---

## 📂 File Organization

- Source code lives in `molsysmt/`
- Jupyter tutorials: `docs/user_guide/tools/<module>/`
- Tests: `molsysmt/tests/`
- CI configs: `.github/workflows/`

---
---

## 🤝 Contributing Workflow

### For new functions:

- Follow this guide for docstring structure and clarity.
- Include a Jupyter tutorial showing how to use the function.
- Add a corresponding unit test.
- Test locally with `pytest` before opening a PR.

### General:

- Keep functions modular and forms-independent.
- For questions, open an issue or discuss in a PR.
- Pull requests are welcome!

# Developer Guide (Updated)

This document provides conventions and rules for writing, testing, and documenting functions in MolSysMT.


## Tutorials (User Guide notebooks)

- Structure every tutorial as:
  1. Anchor + Title.
  2. One-line summary in italics (gerund).
  3. Short introduction.
  4. `API documentation` admonition.
  5. `versionadded` admonition.
  6. Narrated examples (with varied phrasing).
  7. `seealso` admonition with links to related tutorials.

- Use MyST admonition syntax in notebooks:

  ```markdown
  :::{admonition} API documentation
  ...
  :::
  ```

  ```markdown
  :::{seealso}
  ...
  :::
  ```

- Do not use reST-style admonitions inside notebooks.

## Docstring and API documentation references

- Use the high-level rules in this guide together with the detailed patterns in
  `docs/content/developer/documentation/api/docstrings.md` when writing or
  updating docstrings.
- For doctest behavior and how examples are executed, see
  `docs/content/developer/documentation/api/doctests.md`.
- Checklist: summary in gerund; sections ordered as summary, optional extended description, Parameters, single Returns, Raises, Notes, See Also, doctest `Examples`, tutorial admonition, and `.. versionadded::`. Types in lowercase, defaults in text, standard wording for common parameters (`molecular_system`, `selection`, `structure_indices`, `syntax`, `skip_digestion`, `to_form`), 0-based indices (`'all'` selects everything), units for physical quantities, deterministic minimal examples using bundled systems.

## Cross-references in documentation

- When linking between documentation pages (User Guide, Showcase, Developer docs), prefer labeled sections and `{ref}` roles instead of hard-coding file paths.
- For API objects, use `{func}` and `{class}` roles rather than linking directly to generated HTML.
- See `docs/content/developer/documentation/web/references.md` for detailed examples and patterns.

### Versionadded

- **Tutorial notebooks**: also include a block MyST admonition right below the
  first main explanation paragraph opening the tutorial and right before the
  next section or subsection (usually entitled "How this function works" or
  similar):

  ```markdown
  :::{versionadded} 1.0.0
  :::
  ```
