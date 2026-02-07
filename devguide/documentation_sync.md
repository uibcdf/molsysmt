# Documentation Sync

`devguide/` is the canonical source of developer rules. Documentation under
`docs/content/developer` must align with these rules.

## Docstrings
Follow NumPy-style docstrings with a gerund summary, standard section order,
and explicit units. See `coding/coding_guide.md` and
`docs/content/developer/documentation/api/docstrings.md`.

## Tutorials and MyST
Tutorial notebooks must follow the structure described in
`docs/content/developer/documentation/api/docstrings.md` and use MyST admonition syntax.

## Cross-References
Use `{func}`/`{class}` roles for API objects and `{ref}` for internal links
per `docs/content/developer/documentation/web/references.md`.
