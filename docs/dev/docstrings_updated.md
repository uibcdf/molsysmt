# Docstring Guidelines (Updated)

All docstrings in MolSysMT follow the NumPy + Sphinx/MyST style.

## Structure

1. One-line summary (gerund form, e.g., "Checking whether...").
2. Extended description (optional).
3. Parameters.
4. Returns.
5. Raises (optional).
6. Notes (optional).
7. See Also (optional).
8. Examples.
9. Admonition: *Tutorial with more examples* (if relevant).
10. `.. versionadded::` (always last).

## Returns

- Always use a single `Returns` section.  
- Let Sphinx automatically generate the "Return type" field; do not add it manually.  

Examples:

```python
Returns
-------
molecular system or None
    If `in_place=False`, returns a new molecular system.  
    If `in_place=True`, returns None and modifies the input in place.
```

```python
Returns
-------
bool
    True if the container is a non-empty list or tuple and all items are valid
    molecular systems. False otherwise.
```

## Admonitions

- Use `.. admonition:: Tutorial with more examples` inside docstrings.  
- In tutorials (Jupyter notebooks), always use MyST format:

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

## Examples

- Always provide `doctest`-compatible examples using `>>>`.  
- Keep examples minimal but functional.  
- Prefer using `molsysmt.demo` or small peptide builders instead of external files.  
- Non-deterministic results must be avoided.

## Versionadded

- Place `.. versionadded:: x.y.z` **at the very end of the docstring**.  
- In notebooks, use MyST `:::{versionadded} x.y.z` right after the API doc admonition.
