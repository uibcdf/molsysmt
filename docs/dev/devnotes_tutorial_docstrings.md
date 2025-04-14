
# Lessons Learned: Writing Docstrings and Tutorials for MolSysMT

This developer note summarizes the most important things I have learned and refined during the collaborative documentation work for the `basic` and `build` modules in MolSysMT. It is intended as both a personal reflection and a reference for maintaining consistency across docstrings and Jupyter tutorials.

---

## 🧠 General Principles Reinforced

### ✅ Docstring Formatting

I now understand that docstrings in MolSysMT **strictly follow the NumPy format**, adapted for Sphinx and MyST. The canonical structure used across functions includes the following sections, in order:

1. **Short one-line summary** using an active gerund form (`Getting`, `Setting`, `Extracting`, etc.).
2. **Multi-line description**, explaining what the function does and under what circumstances.
3. **Parameters**: 
   - Grouped and clearly typed (`int`, `str`, `list`, etc.)
   - Includes special MolSysMT-specific types like "molecular system"
   - Each parameter's default behavior is carefully documented.
4. **Returns**: 
   - Return type and behavior, including any units if relevant.
5. **Raises**: 
   - Consistently includes `NotSupportedFormError`, `ArgumentError`, `SyntaxError`.
6. **Notes**: 
   - Clarifies internal assumptions and links to reference documentation (Forms, Selection syntaxes, Attributes).
7. **See Also**: 
   - Cross-links to functions that are conceptually related.
8. **Examples**: 
   - Written in executable doctest format (with `>>>`)
   - Always include a realistic use case.
9. **User Guide Reference**: 
   - A closing `.. admonition:: User guide` block that links to the corresponding tutorial.
10. **Version**: 
    - `.. versionadded:: 1.0.0` is **always placed at the end** of the docstring.

---

## 📘 How Tutorials Are Structured

I’ve also internalized the consistent **MyST Markdown structure** for tutorial notebooks:

- Each notebook starts with an **anchor title** like `(Tutorial_FunctionName)=`
- A **short italicized summary** describes what the function does.
- The `versionadded` directive comes right after.
- A section `## How this function works` includes:
  - An API documentation block:
    ```markdown
    ```{admonition} API documentation
    Follow this link... {func}`molsysmt.module.function()`
    ```
    ```
  - A **technical paragraph** that transitions into the worked example.
- All code cells are preceded by **narrative explanations** that give context to each step.
- The notebook ends with a `seealso` block using this exact pattern:
    ```markdown
    ::::{seealso}
    [Path > to > Tutorial](relative/path.ipynb):  
    Short phrase starting with a verb like "Build", "Display", "Identify", "Remove", etc.
    ::::
    ```

---

## 🧩 Internal Vocabulary Clarified

### `element`, `item`, `form`

These are three core concepts that have to be named precisely:

- **`element`**: A component of the molecular system at a given hierarchical level:
  - One of: `'atom'`, `'group'`, `'component'`, `'molecule'`, `'chain'`, `'entity'`, `'system'`
  - Used in functions like `get()`, `select()`, and `info()` to specify the granularity.

- **`item`**: A single object in a supported form (e.g., a file, an OpenMM Topology, an MDAnalysis Universe).
  - These items are the building blocks of a **molecular system**, which can be a list of items.

- **`form`**: The name of the interface used to describe a molecular system or item (e.g., `'file:pdb'`, `'openmm.Topology'`, `'molsysmt.MolSys'`).
  - These are used in `convert()`, `get_form()`, etc.

### `selection`, `structure_indices`, and `element` (together)

Many functions rely on these three arguments to operate on specific parts of a molecular system:

- **`selection`**: Which elements to operate on (e.g., atoms, groups), defined by:
  - A list of indices (0-based)
  - A query string using MolSysMT syntax (e.g., `"atom_name in ['CA', 'CB']"`)
- **`structure_indices`**: Which frames (structures) to include; can be `'all'`, a list, or an integer.
- **`element`**: The level of granularity the operation applies to (see list above).

Combining these three allows functions like `get()`, `set()`, `select()`, `info()`, and iterators to behave flexibly across different structural levels and time frames.

---

## 📌 Language and Style Conventions

- **Use of gerunds**: All function titles and summaries use the gerund form:
  - ✅ “*Getting the attribute values*”
  - ❌ “*Get the attribute values*”
- **Avoid naming engines unless necessary**: E.g., “Uses an external engine” instead of “Uses PDBFixer.”
- **Attribute placeholders**: In format strings, always explain clearly what `{id}`, `{name}`, and `{index}` refer to, and how they map to things like `atom_id` or `group_name`.

---

## ✅ Practical Tips I’ll Apply Moving Forward

- Avoid inventing new examples unless asked — use the real example already in the notebook.
- Always confirm whether a `seealso` block is wanted and in what format.
- Ensure all narrative text in tutorials helps users understand the *why*, not just the *how*.
- Don’t forget to generate cross-references with `{func}` and not `{func}` with parentheses unless you're linking to the call form.

---

This refined understanding will help ensure that new documentation is internally consistent, user-friendly, and ready for the upcoming 1.0.0 release.

