# AI Assistant Agents Guide

This guide is for LLM-based assistants and tools working on or with this repository.
It complements the configuration files in `ai_assistant/GPT_devopers_definition/`
and the global rules from the root `AGENTS.md`.

## Language and repository-facing content

- All repository artifacts (code comments, docstrings, docs, guides, AGENTS files) must be written in English.
- User-facing replies in interactive sessions may follow the user’s language preferences (often Spanish), but any text that is meant to be committed to the repository must be in English.
- When in doubt, prefer English for anything that could end up stored in the repo.

## Alignment with project guides

- Follow the standards and policies described in:
  - `dev_guide.md`
  - `coding/coding_guide.md`
  - `docs/AGENTS.md` and `docs/dev/developer_guide.md`
  - `ai_assistant/GPT_devopers_definition/dev_assistant_gpt_configuration.md`
- Do not invent new style or policy rules; reuse and enforce the existing ones.

## Code changes and API conventions

- Prefer minimal, scoped changes that solve the user’s request without unnecessary refactors.
- Ensure public functions and methods use the `@digest` decorator for argument validation, unless a module explicitly documents an exception.
- Do **not** add `@digest` to private helpers or functions under `molsysmt/_private`.
- Respect established data conventions:
  - Coordinates and distances in nanometers.
  - Box as `(n_structures, 3, 3)` with lengths and angles handled as documented in `molsysmt.pbc`.
  - Time in picoseconds.
  - Charges in units of the elementary charge.

## Documentation and tests

- When adding or modifying functionality, keep docstrings, tutorials, and tests aligned:
  - Docstrings follow NumPy-style with gerund summaries and explicit units.
  - Tutorials and notebooks follow the structure described in `docs/dev/developer_guide.md`.
  - Cross-links in documentation use labeled sections and `{ref}` roles where possible, as described in `docs/content/developer/documentation/web/references.md`.
  - Tests live under `tests/` mirroring the package structure and use `pytest`.
- Prefer updating or extending existing tests over weakening assertions.

## Safety and tooling behavior

- Avoid destructive git commands or workflows (for example, `git reset --hard`, `git push --force`) in suggestions or tooling usage.
- Do not introduce new dependencies or modify packaging/CI files (such as `pyproject.toml`, `setup.cfg`, GitHub Actions) unless explicitly requested.
- Respect any sandboxing or execution constraints of the environment; do not assume network access.

## Interaction guidelines for assistants

- Treat all repository guides and AGENTS files as authoritative; read them before making structural changes.
- When uncertain about conventions in a specific area (forms, pbc, topology, etc.), inspect nearby modules and tests to infer the correct pattern.
- Prefer proposing or applying changes that are easy to review: small, well-scoped patches with clear intent.  Context: we expanded ai_assistant/AGENTS.md based on dev assistant configuration and root/coding/docs AGENTS; we must answer in Spanish, concise, summarizing new sections. No additional tool calls needed.***
