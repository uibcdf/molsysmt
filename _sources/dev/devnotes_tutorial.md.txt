

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


## ✅ Practical Tips I’ll Apply Moving Forward

- Always confirm whether a `seealso` block is wanted and in what format.
- Ensure all narrative text in tutorials helps users understand the *why*, not just the *how*.
- Don’t forget to generate cross-references with `{func}` and not `{func}` with parentheses unless you're linking to the call form.
- For links between documentation pages, prefer labeled sections and `{ref}` roles over direct file paths; see `docs/content/developer/documentation/web/references.md` for examples.

# Dev Notes: Tutorial & Docstrings (Updated)

This note complements the Developer Guide and Docstring Guidelines with specific advice for tutorial notebooks.

## General structure of tutorials

- Always start with an **anchor** and a **title**:

  ```markdown
  (Tutorial_FunctionName)=
  # Function Name
  ```

- Follow with a one-line summary in *italics* and **gerund form**.
- Add a short introduction in prose.
- Insert the `API documentation` admonition:

  ```markdown
  :::{admonition} API documentation
  Follow this link for details on arguments, raised errors, and return values: {func}`molsysmt.basic.function_name`.
  :::
  ```

- Add a `versionadded` block:

  ```markdown
  :::{versionadded} 1.0.0
  :::
  ```

- Proceed with narrated examples, alternating phrasing:
  - "We start with..."
  - "In contrast..."
  - "Another case is..."
  - "Finally..."

- Close with a `seealso` block linking to related tutorials.

## Admonitions

- All admonitions in tutorials must use MyST syntax (`:::{...}`).  
- Valid admonitions: `admonition`, `tip`, `warning`, `seealso`, `versionadded`.

## Examples and testing

- Examples in tutorials should mirror or complement those in docstrings.  
- Use simple demo systems to keep runtime low.  
- Avoid duplication: examples in docstrings are already tested by `pytest --doctest-modules`. Tutorials may expand with longer narrative or combined workflows.
