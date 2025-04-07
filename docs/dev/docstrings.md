# Docstring Style Guide for MolSysMT

This guide defines the conventions for writing docstrings in the MolSysMT
project. All public-facing functions, methods, and classes must include
docstrings that follow the structure and style described below.

MolSysMT uses **Sphinx** with the **MyST parser**, allowing docstrings to be
written in **Markdown-compatible syntax** while supporting cross-references and
other Sphinx directives.

---

## ✍️ Format Overview

- Follow the **NumPy-style** docstring format
- Use **Sphinx reST directives** (`:ref:`, `:func:`, `.. versionadded::`, etc.)
- Write with **MyST compatibility** in mind
- Use **English, in technical and clear tone**

---

## 📐 Structure of a Docstring

### 1. One-line Summary
- Start with a short sentence in **gerund form** (e.g. "Adding elements...")
- Use third-person, present tense

**Example:**
```python
"""
Adding elements of a molecular system into another molecular system.
"""
```

### 2. Extended Description
- A few sentences describing behavior, requirements, and edge cases.
- Include conditions, interactions between arguments, or assumptions.

### 3. Parameters
- Each parameter must include:
  - name
  - type (lowercase, e.g. `str`, `tuple`, `molecular system`)
  - optional: default value in description (not in signature)
  - clear explanation of its use

**Example:**
```python
selection : tuple, list, numpy.ndarray or str, default 'all'
    Selection of atoms to which this method applies. It can be a list/array
    of atom indices or a string selection expression.
```

### 4. Returns (if applicable)
- Describe return type and meaning

### 5. Raises
- List exceptions the function may raise, with conditions.

### 6. Version Added
```python
.. versionadded:: 0.1.0
```

### 7. Notes
- Add clarifications, implementation notes, or links to other docs
```python
:ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>`
```

### 8. See Also
- List related functions with `:func:` links

### 9. Examples
- Include at least one `doctest`-style example using `>>>`
- Keep realistic and minimal

### 10. Optional: User Guide link
- Use Sphinx's `.. admonition::` directive

```python
.. admonition:: User guide

   Follow this link for a tutorial on how to work with this function:
   :ref:`User Guide > Tools > Basic > Add <Tutorial_Add>`.
```

---

## 📘 MyST and Sphinx Tips

- You can use Markdown formatting inside docstrings (e.g. `**bold**`, lists, etc.)
- Avoid using raw `.rst` when not needed
- Triple backticks for code blocks are OK in `.md`, but docstrings must still use triple quotes `"""` in code
- Cross-references (`:ref:`, `:func:`) work as in `.rst`

---

## 🧪 Checklist for Reviewing a Docstring

- [ ] One-line summary is present and clear
- [ ] Extended description explains use cases or constraints
- [ ] All parameters are documented with type and default
- [ ] Errors (`Raises`) are listed if applicable
- [ ] Version added is included
- [ ] Example is present and valid
- [ ] Relevant links and cross-references are used

---

For a real example, see [`molsysmt.basic.add()`](https://www.uibcdf.org/molsysmt/contents/user/tools/basic/add.html).

Happy documenting! ✍️

