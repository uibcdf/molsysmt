# Developer Guide (Updated)

This document provides conventions and rules for writing, testing, and documenting functions in MolSysMT.

## Style

- **Comments in code and scripts** must always be in **English**.  
- Documentation and tutorials (Markdown, Jupyter) must also be in English.  

## Docstrings

- All docstrings must follow **NumPy style** with Sphinx/MyST compatibility.
- Sections must appear in the following order when present:
  1. One-line summary (in **gerund** form, e.g., "Adding elements...").
  2. Extended description.
  3. Parameters.
  4. Returns.
  5. Raises.
  6. Notes.
  7. See Also.
  8. Examples.
  9. Admonition: *Tutorial with more examples*.
  10. `.. versionadded::` (always **at the end**).

- Use the `molsysmt.basic.add()` function as the canonical reference example.

### Returns and Return type

- Only define a single **Returns** section.  
- Use syntax like:

  ```python
  Returns
  -------
  molecular system or None
      If `in_place=False`, returns a new molecular system.  
      If `in_place=True`, returns None and modifies the input in place.
  ```

- With PyData + napoleon, Sphinx will automatically generate a separate
  **Return type** field. Do **not** add one manually.
- If the function can return multiple types conceptually different, use different lines in the Returns section:

  ```python
  Returns
  -------
  Type1
      Justification for Type1.    
  Type2
      Justification for Type2.    
  ```

### Versionadded

- **Docstrings**: always use `.. versionadded:: x.y.z` at the very end.  

### Testing the examples

- All examples inside docstrings must be written as `doctest` blocks (`>>>`) and are executed automatically by `pytest --doctest-modules`.  
- **Do not duplicate** examples in `tests/` unless additional complex checks are required (e.g., fixtures, multiple asserts, heavy inputs).  
- Unit tests in `tests/` should cover logic and edge cases not suitable for doctest format.


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

### Versionadded

- **Tutorial notebooks**: also include a block MyST admonition right below the
  first main explanation paragraph opening the tutorial and right before the
  next section or subsection (usually entitled "How this function works" or
  similar):

  ```markdown
  :::{versionadded} 1.0.0
  :::
  ```

