# Agent Instructions for `docs/`

These instructions apply to all files under `docs/`.

## Writing style
- Keep the friendly, action-oriented tone used in `docs/README.md`: short sentences, second-person guidance, and clear "why + how" framing.
- Prefer lists and headings over long paragraphs; each section should be scannable.
- Use accurate API names and consistent capitalization. Avoid inventing new terminology.
- When adding scientific context, include a brief rationale or citation from `bibliography.bib` when possible.

## Structural expectations
- Reuse the existing section hierarchy (`##` then `###`) and keep the page order consistent with the current table of contents.
- Place reusable assets in `_static/` and `_templates/`; do not embed large assets directly in Markdown/RST.
- For API pages, keep entries synchronized with the Python package and use the `clean_api.py` helper when regenerating content.

## Build and verification
- After substantive edits, run `make html` from `docs/` to ensure the site builds cleanly. Use `make clean` first if cached artifacts interfere.
- For Read the Docs compatibility, update `docs/requirements.yaml` when new optional dependencies are introduced.

## Porting guidance
- When adapting this documentation style to another project, copy the `docs/` layout, adjust branding in `conf.py` and landing pages, and preserve the tone outlined above.
