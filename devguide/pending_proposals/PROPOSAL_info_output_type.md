# PROPOSAL: `output_type` for `molsysmt.basic.info()`

## Problem Statement

`molsysmt.basic.info()` currently returns a Pandas `Styler` unconditionally.
This is convenient in notebooks, but it makes some workflows less ergonomic:

- programmatic access often wants a plain `DataFrame`
- serialization or API composition may prefer a `dict`
- downstream libraries may want explicit control over display vs data

## Proposed Solution

Add a new public argument:

```python
output_type="styler"
```

Supported values:

- `"styler"`
- `"dataframe"`
- `"dict"`

## Intended Semantics

- `output_type="styler"`
  - current behavior
  - return `df(...).style.hide(axis="index")`
- `output_type="dataframe"`
  - return the underlying Pandas `DataFrame`
- `output_type="dict"`
  - return a JSON-friendly record structure such as
    `list[dict[str, Any]]` or an equivalent stable mapping

## Why This Matters

- preserves the notebook-friendly default
- improves interoperability for API wrappers such as `MolSysView.info(...)`
- avoids forcing consumers to unwrap a `Styler` just to access the data

## Compatibility

This should be backward compatible if the default remains the current styled
table output.

## Suggested Default

Keep:

```python
output_type="styler"
```

so that existing notebook usage remains unchanged.
