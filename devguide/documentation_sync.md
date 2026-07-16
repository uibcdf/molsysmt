# Documentation Lifecycle and Synchronization

Documentation is part of the implementation contract. A public behavior change
is incomplete until its code, tests, docstring, web documentation, and relevant
course material agree.

## Surfaces

- API docstrings follow
  `docs/content/developer/documentation/api/docstrings.md`.
- MyST pages and cross-references follow the material under
  `docs/content/developer/documentation/web/`, especially `references.md`.
- User documentation lives under `docs/content/user/` in Foundations, Tools,
  and Cookbook.
- The Four Paths course lives under `docs/content/course/`.
- Developer contracts live here in `devguide/`; they must not duplicate
  user-facing tutorials or generated API reference.

## Lifecycle checklist

For a public API or behavior change:

1. update NumPy-style docstrings and deterministic doctest examples;
2. update behavioral tests and failure-path tests;
3. update the relevant User Guide and Cookbook pages;
4. locate every affected course notebook and update or verify it;
5. update developer contracts only when architecture or policy changes;
6. validate links, execute applicable notebooks/doctests, and build docs;
7. record deliberate omissions with an owner and acceptance criterion.

Text search is useful for discovery but is not verification. Notebook code and
outputs can be stale even when links resolve.

## Duplication policy

- Docstrings define callable arguments, returns, raises, and minimal examples.
- User pages teach supported workflows.
- Course notebooks teach sequenced scientific use cases.
- Developer guides define architecture, maintenance rules, and evidence.
- Proposals and archives never override an implemented contract.

Link to the authoritative surface instead of copying large tables or signatures.

## Current limitation

The repository does not yet have a machine-readable mapping from public symbols
to their User Guide, Cookbook, and course consumers. The lifecycle rule is
therefore only partially enforceable. See
`pending_proposals/documentation_lifecycle_manifest.md`.
