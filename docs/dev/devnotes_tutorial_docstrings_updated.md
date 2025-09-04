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
