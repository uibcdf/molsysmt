# Documentation for the web

This section collects guidelines and examples for writing MolSysMT’s web
documentation with MyST and Sphinx. It is aimed at contributors who edit
the User Guide, Showcase, Cookbook, and developer documentation.

- Use `myst.ipynb` to see concrete examples of MyST admonitions and how to
  structure tutorial notebooks.
- Use `references.md` as the reference for cross-links between pages and
  API objects (labels, `{ref}`, `{func}`, `{class}`, etc.).

```{eval-rst}
.. toctree::
   :maxdepth: 2

   myst.ipynb
   references.md
```
