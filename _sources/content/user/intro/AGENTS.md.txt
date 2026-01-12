# User Guide Introduction Agents Guide

This guide is for agents editing the **Introduction** section of the User Guide
under `docs/content/user/intro`.

## Purpose and audience

- Explain core concepts of MolSysMT to new users: what MolSysMT is, how to install it, what a molecular system is, and how forms, elements, attributes, and selections work.
- Avoid deep implementation or development details; those belong in `docs/dev` and `docs/content/developer`.

## Structure and topics

- Keep `intro/index.md` as the conceptual entry point for new users.
- Maintain and extend the existing subtopics via their toctrees:
  - `molsysmt.ipynb` / `installation.md`: overview and installation instructions.
  - `molecular_systems/index.md`: description, items, forms, elements, attributes.
  - `demo_systems.ipynb`: how to use bundled demo systems.
  - `native_forms/index.md`: native MolSysMT forms (for example, `molsysmt.MolSys`, `molsysmt.Topology`, `file:h5msm`).
  - `selection_syntaxes.ipynb`: selection expressions and examples.
  - `tools.ipynb`: high-level overview of tools.
  - `viewers.ipynb`: visualization backends (for example, nglview).
  - `supported.ipynb`: supported forms and external libraries.
  - `memory_management.ipynb`, `quantities_and_units.ipynb`, `configuration_options.ipynb`, `molsysmt_logging_user_guide.md`: advanced user topics.
- When adding new pages, ensure they fit one of these themes or clearly extend them, and integrate them into the toctree.

## Style and content guidelines

- Use concise explanations, focusing on:
  - What the concept is.
  - Why it matters for using MolSysMT.
  - Where to go next (links to Tools or Cookbook tutorials).
- Mention units and shapes where relevant (for example, how coordinates and box are represented).
- Use MyST admonitions for “API documentation” links, notes, and see-also sections when connecting to other parts of the documentation.
- For links to other documentation pages, prefer labeled sections and `{ref}` roles over file paths; follow `docs/content/developer/documentation/web/references.md`.
