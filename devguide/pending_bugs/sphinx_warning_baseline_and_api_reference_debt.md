# Sphinx Warning Baseline and API Reference Debt

**Status:** confirmed documentation debt; accepted as non-blocking for the 1.0
source release after the F4 structural repairs.
**Found:** 2026-07-29 during a forced full Sphinx build.
**Scope:** generated API reference, legacy User Guide pages, course markup style,
orphan pages, and notebook metadata.

## Evidence

The forced build

```bash
cd docs
sphinx-build -E -q -b html -w /tmp/molsysmt-sphinx-warnings.log . _build/html
```

completed with exit code 0 and generated the HTML site. Its warning log contained
1,223 `WARNING:` records before the bounded F4 repairs. The largest tagged
families were:

| Family | Count | Meaning |
| --- | ---: | --- |
| `myst.header` | 423 | non-consecutive heading levels; 369 are in the course |
| `toc.no_title` | 350 | notebook targets without a usable title, often repeated |
| `toc.not_included` | 114 | source pages absent from every toctree |
| `myst.xref_missing` | 78 | unresolved legacy MyST links |
| `autodoc.import_object` | 50 | stale API objects |
| `myst.directive_unknown` | 32 | unsupported directives; 13 course occurrences use `key-takeaway` |
| `docutils` | 22 | malformed or inconsistent reStructuredText |
| `toc.not_readable` | 11 | references to source documents that did not exist |
| `ref.ref` | 4 | unresolved Sphinx labels |

Autosummary also reported 42 initial import failures and 49 generation-time
failures, dominated by form pages that still name a module-level `get` adapter
which the current form does not expose.

The full log is deliberately not committed: it contains absolute environment
paths and is reproducible from the command above.

## What F4 fixed

All 11 `toc.not_readable` cases found by the forced build were corrected:

- obsolete API entries for molecular dynamics, `thirds`, and oligosaccharides;
- a removed showcase membrane page;
- stale amino-acid, hydrogen-bond, structure, NGLView, and OpenMM-reporter
  notebook names.

An incremental Sphinx build after those repairs exited 0 and reported zero
`toc.not_readable` warnings. It also reported no unresolved course cross-reference
and no warning involving either of the semantic targets introduced in Common Core
12 and 17.

The Sphinx build regenerated ten checked-in autosummary pages for native and H5MSM
forms. Those changes expose current chemical-state, bond-metadata, and
thermodynamic getters/setters instead of preserving the stale generated lists.

## The published build was worse than this baseline, until 2026-08-08

Everything above measures the build produced by the command in **Evidence**, run by
hand. Until 2026-08-08 that was not the build being published.

`uibcdf/action-sphinx-docs-to-gh-pages` ran `sphinx-apidoc -o . ../` by default, and
the documentation workflow never disabled it. Reproduced against a scratch output
directory, that step generates **153 `.rst` files** — `modules.rst`, `conftest.rst`,
and one per subpackage — into `docs/`. None of them is in any toctree, so each was an
orphan page, built, published and counted as a warning the local baseline never saw;
autodoc also imported every module in the tree to render them. The published site
carried the result: `modules.html` and `molsysmt.basic.html` were reachable on
`www.uibcdf.org/molsysmt/`, a second API reference beside the curated one under
`docs/api/`, which nobody maintained.

The workflow now passes `sphinx-apidoc: false`, and version 3.0.0 of the action also
makes it the default. `modules.html` returns 404 on the published site as of
2026-08-08.

**Consequence for this report:** the local command and the CI build now measure the
same thing, so the inventory above is finally the inventory of what readers get. Any
ratchet built per the remediation plan should be measured once more before being
frozen — the `toc.not_included` and `autodoc.import_object` families are the two this
change touches, and neither has been re-counted since.

## Why this does not block 1.0

The release contract requires the course structure to be free of references to
nonexistent documents. That condition is now satisfied dynamically by Sphinx and
statically by `validate_course.py`. The remaining warnings are real quality debt,
but they do not change runtime correctness, API availability, scientific results,
or the resolved course navigation.

Making all 156 course notebooks warning-free, rebuilding the old form reference,
and deciding which orphan pages belong in the published navigation are separate,
potentially large editorial projects. Folding them into the release candidate
would delay the source release behind pre-existing documentation cleanup without
improving its scientific contract.

This is accepted debt, not a claim that the documentation is warning-clean.

## Remediation plan

Work by family and keep a ratcheted warning inventory:

1. generate form API pages from the discovered module surface, never from stale
   hand-maintained operation lists;
2. add a documentation validator that fails on a new warning family or count
   increase while allowing the recorded baseline to decrease;
3. repair unresolved public API labels and remove duplicate source identities;
4. decide whether each orphan User Guide page belongs in a toctree or should be
   archived;
5. add titles and stable semantic labels to published notebooks;
6. replace or register `key-takeaway`, then normalize course heading levels;
7. normalize notebook cell IDs before a future `nbformat` release makes their
   absence an error.

Each step should update the baseline by category. Do not solve the problem by
globally suppressing warnings.

## Closure criteria

- a forced clean Sphinx build emits no warnings;
- generated API pages name only importable current objects;
- every published page has an intentional navigation status;
- course directives and heading levels follow the documented MyST conventions;
- notebooks validate without missing-cell-ID compatibility warnings;
- CI rejects any reintroduced warning.
