# User Guide Agents Guide

This guide is for agents and contributors editing the **User Guide** under
`docs/content/user`. It refines the global rules in `docs/AGENTS.md` for
end-user documentation.

## Audience and language

- Target audience: MolSysMT users (not necessarily developers), with basic familiarity with Python and molecular simulation concepts.
- All content must be written in English.
- Use clear, direct language focused on solving users’ tasks and answering “how do I…?” and “what does this do?” questions.

## Overall structure of the User Guide

- Keep the top-level organization:
  - `Introduction` (`intro/`): concepts, installation, core ideas (molecular systems, forms, elements, selections, units, supported engines, logging).
  - `Tools` (`tools/`): per-function tutorials grouped by topic (basic, build, topology, structure, PBC, physchem, hbonds, molecular_mechanics, element, form, thirds).
  - `Cookbook` (`cookbook/`): recipes that combine several tools to achieve practical workflows.
- When adding new sections or pages, integrate them into this structure instead of creating parallel trees.
- Do not move content that belongs to the Developer Guide into the User Guide; low-level implementation details and internal conventions belong under `docs/dev` or `docs/content/developer`.

## Style and markup

- Use MyST Markdown in `.md` files and notebooks (`.ipynb`) with MyST-friendly cells for admonitions and cross-references.
- Follow the tutorial structure described in `docs/dev/devnotes_tutorial.md` but keep explanations oriented to end users:
  - Short, gerund-style summaries where they parallel function docstrings.
  - Explicit mention of units and shapes when presenting numerical results.
  - Examples that are minimal, fast to run, and reproducible.
- Use admonitions (`:::{admonition}`, `:::{tip}`, `:::{warning}`, `:::{seealso}`, `:::{versionadded}`) where they help highlight API links, caveats, or related material.

## Cross-references and navigation

- When referencing functions or classes, link to the API using `{func}` whenever possible.
- For links between User Guide pages, prefer labeled sections and `{ref}` roles over direct file paths; follow the conventions described in `docs/content/developer/documentation/web/references.md`.
- Keep navigation consistent with `docs/index.ipynb` and `docs/content/user/index.ipynb`; do not remove or repurpose the main grids and toctrees without updating all affected pages.

## Content boundaries

- Introduction pages should explain **concepts** (forms, elements, selections, units, supported formats), not internal implementation details.
- Tools pages should explain **how to use specific functions** with concrete examples and expected inputs/outputs, not internal algorithms.
- Cookbook pages should present **multi-step workflows** that combine functions and possibly external engines, referencing the relevant Tools pages for details.
