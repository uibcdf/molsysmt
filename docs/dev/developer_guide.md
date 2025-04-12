
# 🧪 Editorial and Developer Guide for MolSysMT Documentation

This document serves as the editorial and structural guide for contributing to the documentation and development of the MolSysMT project. It covers docstring conventions, tutorial structure, internal practices, and CI/testing expectations.

---

## 🤪 Project Overview

MolSysMT is a modular scientific Python library for handling molecular systems. The project is organized around three central concepts:

- **Forms**: Representations of molecular systems (e.g., `'file:pdb'`, `'openmm.Topology'`).
- **Elements**: Hierarchical structural levels (`'atom'`, `'group'`, `'molecule'`, etc.).
- **Attributes**: Accessible properties or metadata (`coordinates`, `box`, `entity_name`, etc.).

---

## 📘 Docstring Style Guide

Docstrings follow a NumPy + Sphinx/MyST format. Use the `add()` function as the canonical reference:
<https://www.uibcdf.org/MolSysMT/user_guide/tools/basic/add/>

### ✅ Structure for Public Functions

Each public function **must include** the following sections in this order:

- **One-line title** with a strong verb in infinitive (e.g., `Retrieve`, `Convert`, `Display`).
- `Parameters`
- `Returns`
- `Raises` (even if only `NotSupportedFormError`)
- `Notes`
- `See Also`
- `Examples`
- `.. versionadded:: x.x.x`

### 🔍 Style Details

- Use "**Retrieve**" instead of "Get" in titles and summaries.
- Use idiomatic names like `get()` for function names, but avoid "getting" in text.
- `See Also` descriptions must be concise, in infinitive (no "to"):
  - ✅ `Retrieve attribute values from a molecular system`
  - ❌ `To get the attributes of...`
- Use `:ref:` and `{func}` for all Sphinx-compatible cross-links.

---

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

---

## 📂 File Organization

- Source code lives in `molsysmt/`
- Jupyter tutorials: `docs/user_guide/tools/<module>/`
- Tests: `molsysmt/tests/`
- CI configs: `.github/workflows/`

---

## 🧪 Testing Guidelines

- Use `pytest` for all unit tests.
- Tests go in `molsysmt/tests/` using `test_<function>.py` naming.
- Use `@pytest.mark.parametrize` when testing over multiple forms.
- Track test coverage via Codecov: <https://app.codecov.io/github/uibcdf/MolSysMT>
- Validate tutorials optionally using `nbval` or `pytest + papermill`.

---

## ⚙️ Continuous Integration (CI)

- GitHub Actions is used for all testing and documentation workflows.
- Documentation is deployed to GitHub Pages using:
  <https://github.com/uibcdf/action-sphinx-docs-to-gh-pages>
- CI tests for Python 3.8 through 3.12.
- Recommended to check all notebooks before merging to main.

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

---

