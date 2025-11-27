# MolSysMT Documentation Guide

MolSysMT’s documentation is written with [Sphinx](https://www.sphinx-doc.org/en/master/) and organized to be easy to reuse in
other projects that want the same tone, structure, and developer experience. This guide summarizes how to build the docs,
explains the layout of the repository, and notes the conventions that give the site its voice.

## Build the docs locally

1. Create and activate a conda environment with Sphinx and the Read the Docs theme:
   ```bash
   conda install sphinx sphinx_rtd_theme
   ```
2. From this `docs/` directory, build the HTML site:
   ```bash
   make html
   ```
3. Open `_build/html/index.html` in a browser to preview the site. The `make clean` target removes previous builds.

MolSysMT ships a [Read the Docs configuration](../.readthedocs.yaml) so the online build matches local output. If you add
optional dependencies that are needed for `autodoc`, list them in `docs/requirements.yaml`.

## Directory overview

- `content/`: Source pages for user guides, tutorials, and conceptual explanations.
- `api/` and `old_api/`: Auto-generated API references; the `clean_api.py` script keeps entries tidy.
- `_templates/` and `_static/`: Custom theme assets and layout overrides that create the MolSysMT visual style.
- `_bibtex/` and `bibliography.bib`: Citation management for scientific references.
- `dev/` and `sandbox/` notebooks: Experimental material used to prototype sections before promotion to `content/`.

## Writing style and tone

- Prefer short, direct sentences written in the second person (“you”) that guide the reader through each action.
- Lead with the “why” before the “how” when introducing new concepts, and follow with minimal, reproducible code examples.
- Use Markdown-style lists and headings to keep pages scannable; avoid long blocks of text.
- Keep terminology consistent with the API (function and class names should match exactly, including capitalization).
- When referencing scientific context, include brief rationale or citations from `bibliography.bib` where appropriate.

For details on MyST usage (admonitions, tutorial structure, cross-references,
and API roles), see the developer documentation under
`docs/content/developer/documentation/web/` (especially `myst.ipynb` and
`references.md`).***

## Reusing this structure in another project

To export MolSysMT’s documentation style to a new codebase:

1. Copy the `docs/` directory as a starting point, including `_templates/`, `_static/`, and the `Makefile`.
2. Replace MolSysMT-specific names in `conf.py`, `index.ipynb`, and `content/` landing pages with the new project’s branding.
3. Update `api/` generation scripts to point to the new Python package while preserving the existing section order and headings.
4. Keep the writing conventions above so new sections feel consistent, and use the same heading hierarchy (`##`, then `###`).
5. Validate the migrated docs locally with `make html` and, if using Read the Docs, connect the repository with the provided
   `.readthedocs.yaml` template as a baseline.

By keeping these guidelines in mind, contributors can extend MolSysMT’s documentation—or replicate it elsewhere—without losing
the clear, welcoming tone readers expect.
