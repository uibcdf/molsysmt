---
summary: The published API reference documents a removed private module.
issue: uibcdf/molsysmt#150
status: resolved
opened: 2026-08-13
closed: 2026-08-13
severity: medium
verification: inspected
area: [docs, api]
guard: devtools/tests/test_public_api_docs.py
normative: devguide/api_surface.md
blocked_by: []
supersedes: []
---

# The published API reference carries a `_private` branch

**Status:** open. The decision is the maintainer's: it turns on who the published
API reference is for.
**Raised:** 2026-08-08, while auditing the two UIBCDF GitHub Actions MolSysMT
invokes. The audit asked whether the Sphinx action should keep running
`sphinx-apidoc`; reading `docs/api/` to answer that turned up this separate
question.
**Scope:** `docs/api/_private/`, the `Developer` toctree in `docs/api/index.md`
and `docs/api/index_v2.md`.

## What is published today

`docs/api/index.md:94-98` declares a second toctree, captioned `Developer` and
marked `:hidden:`, whose only entry is `_private/api__private`. `index_v2.md`
repeats it. Hidden removes it from the sidebar; it does not stop the pages from
being built, published, indexed, or reached by direct link.

The branch is four tracked files and documents exactly one object:

```
docs/api/_private/api__private.rst
docs/api/_private/exceptions/api_exceptions.rst
docs/api/_private/exceptions/autosummary/molsysmt._private.smonitor.NotImplementedMethodError.rst
docs/api/_private/exceptions/autosummary/molsysmt._private.exceptions.NotImplementedMethodError.rst
```

`api_exceptions.rst` sets `currentmodule:: molsysmt._private.smonitor` and
autosummarises `NotImplementedMethodError`.

## The tension to resolve

`AGENTS.md` states "Do not expose `_private` modules in public APIs", and
[`api_surface.md`](../api_surface.md) line 19 states that modules under
`molsysmt/_private` are internal.

Neither sentence is literally about documentation, and that is the honest reading:
a rendered page is a weaker form of exposure than an importable name, and a
project may legitimately publish a developer-facing reference to its internals.
So this is not a report of a rule being broken. It is a question that has never
been decided in writing, and the published site currently answers it by accident —
with one page, hidden, about one exception.

Whatever is decided should also decide what the branch is *for*. One internal
exception class is not a developer reference to a library with an internal
digestion layer, a diagnostics catalogue, a chunked executor and a private
argument-contract package. Either those belong in it or nothing does.

## Evidence that the branch is unmaintained

Verified on 2026-08-08 against the live site (`http://www.uibcdf.org/molsysmt/`)
and the working tree:

| URL under `api/_private/` | code |
|---|---|
| `api__private.html` | 200 |
| `exceptions/api_exceptions.html` | 200 |
| `exceptions/autosummary/molsysmt._private.exceptions.NotImplementedMethodError.html` | 200 |
| `exceptions/autosummary/molsysmt._private.smonitor.NotImplementedMethodError.html` | 404 |

The page that is live documents `molsysmt._private.exceptions`, which no longer
exists:

```python
>>> import molsysmt._private.exceptions
ModuleNotFoundError: No module named 'molsysmt._private.exceptions'
```

The page that documents the module that *does* exist is not published. The site
predates the rename — `gh-pages` was last written on 2026-01-12 — so the only
`_private` documentation a reader can reach today describes a module that was
removed seven months ago.

The stale stub is still tracked in the source tree. Nothing regenerates it, since
autosummary only writes stubs for names a directive lists, and nothing deletes it:
`docs/clean_api.py` removes whole `autosummary/` directories, so it would go with
the rest if that script were ever run. Meanwhile Sphinx still reads it as a source
page, which makes it one concrete, attributable instance of both dominant warning
families measured in
[`../pending_bugs/sphinx_warning_baseline_and_api_reference_debt.md`](../pending_bugs/sphinx_warning_baseline_and_api_reference_debt.md):
an `autodoc.import_object` failure on a module that cannot be imported, and a
`toc.not_included` orphan.

## Options

1. **Remove the branch.** The published reference becomes user-facing only, which
   matches what `AGENTS.md` and `api_surface.md` say about `_private` everywhere
   else. Internals stay documented where they already are: `devguide/` and
   `docs/content/developer/`.
2. **Keep it and make it deliberate.** Write down what the developer-facing
   documented surface is, point the autosummary directives at those modules, and
   delete the stale stub. This is the largest option and it creates a maintenance
   obligation that has so far not been met by a four-file branch.
3. **Move it.** Relocate the material under `docs/content/developer/`, where a
   reader looking for internals expects it, and leave `docs/api/` for the public
   surface.

Option 1 or 3 is the smaller and more consistent answer; option 2 is only worth
taking if the developer reference is genuinely wanted for 1.0. No option should be
executed before the choice is recorded here.

## Acceptance criteria

Independent of the option chosen:

1. No published page documents a module that cannot be imported.
2. `docs/api/_private/exceptions/autosummary/molsysmt._private.exceptions.NotImplementedMethodError.rst`
   is gone from the tree.
3. A clean Sphinx build emits no `autodoc.import_object` or `toc.not_included`
   warning attributable to `docs/api/_private/`, and the warning inventory in the
   Sphinx baseline report is decremented by the amount actually removed, measured
   rather than predicted.
4. If the branch survives in any form, its intended scope is stated in
   [`api_surface.md`](../api_surface.md), and every object it lists imports.

## Related

- [`../pending_bugs/sphinx_warning_baseline_and_api_reference_debt.md`](../pending_bugs/sphinx_warning_baseline_and_api_reference_debt.md)
  — the warning inventory this branch contributes to.
- [`presentation_and_citation_surface.md`](presentation_and_citation_surface.md)
  — the other open questions about what MolSysMT publishes about itself.

## Resolution — 2026-08-13

Option 1 was selected. The four `_private` API source pages and both hidden
toctree entries were removed. `api_surface.md` now states the durable rule:
private modules are excluded from the published API reference, while internal
implementation guidance belongs in `devguide/` and
`docs/content/developer/`.

`devtools/tests/test_public_api_docs.py` prevents either an API source file
under `docs/api/_private/` or an API reference to `molsysmt._private` from
returning. The broader historical Sphinx warning population remains tracked by
uibcdf/molsysmt#144 and is not reclassified as part of this bounded fix.
