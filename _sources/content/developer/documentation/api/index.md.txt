# API documentation guidelines

This section collects guidelines for documenting MolSysMT’s public API and for
testing examples embedded in docstrings.

- `docstrings.md` describes the structure, style, and required sections for
  docstrings on functions, methods, classes, modules, and attributes.
- `doctests.md` explains how we use `pytest --doctest-modules` to keep all
  `Examples` up to date and executable.

Docstrings are written in NumPy style with Sphinx roles (such as `:ref:` and
`:func:`), while the surrounding documentation uses MyST and the cross-linking
patterns described in `docs/content/developer/documentation/web/`.

```{eval-rst}
.. toctree::
   :maxdepth: 2

   docstrings.md
   doctests.md
```
