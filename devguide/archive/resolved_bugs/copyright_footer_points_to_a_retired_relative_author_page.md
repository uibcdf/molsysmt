---
summary: Copyright footer points to a retired relative author page
issue: uibcdf/molsysmt#761
status: resolved
opened: 2026-11-15
closed: 2026-11-15
severity: low
verification: reproduced
area: [docs]
guard: tests/documentation/test_copyright_footer.py
normative:
blocked_by: []
supersedes: []
---

# Copyright footer uses a retired relative author route

**Reported:** 2026-11-15 during actual #759 article link receiving.
**Status:** active; receive the corrected real template at root and nested depths.

## What

`docs/_templates/copyright.html` uses `contents/about/who.html`. The maintained
author page is `content/about/who.html`; moreover, the literal relative route
is resolved from each article's directory. The global author link is broken
both at the site root and inside course pages.

## How

The full built peptide article contains this footer link. The focused guard
builds three real Sphinx/PyData pages with the production template and resolves
the rendered contributor link from both the root and a nested article. The
original template fails at the root because `contents` is not `content`.

## Why

Readers cannot follow the global contributor link. Use Sphinx's `pathto` for
the maintained document target, so deployments under a path prefix retain the
same correct relative relationship. Author text, credits and other footer
links remain unchanged.

## Acceptance criteria

The actual template builds without warnings and emits one contributor link
per tested page. Both links resolve to the generated maintained author page,
remain inside the site root and avoid an absolute deployment-specific URL.
Receive the real nested course page after rebuilding the changed template.

## Provenance

Linux, existing Python 3.14.7 and frozen documentation runtime; source parent
1b3b16191 plus the separate #759/#760 corrections. The baseline guard fails
once; the earlier full-site build passes but does not establish link integrity.
No package, molecular implementation or release candidate changes.

## Resolution — 2026-11-15

The actual notebook uses the explicit capped sequence and the existing public
quartet, copy and geometric-edit tools. The returned five phi, five psi and
five omega quartets reach the declared targets, modulo the angular branch cut.
Independent NumPy angles, unchanged source coordinates, cap connectivity and
bond-length preservation are checked under nm/ps and pm/fs policies. Targets
apply to returned quartets; the lesson does not classify or predict a stable
helix. The extended-region challenge remains a declared modeling exercise.

All seven code cells execute in a fresh kernel. A dedicated generator executes
the same scientific cells and exports only this model. The saved scene is
received against calculated coordinates and atom/group axes under both unit
policies. The browser loads all 109 atoms, actual Mol* coordinates and a framed
ball-and-stick image using local assets under a /molsysmt/ deployment prefix.
The screenshot is inspected. This static scene does not close #615's distinct
cold Jupyter canvas investigation or qualify the final installed pair.

The final overlapping selected cohort, including adjacent construction/torsion
controls and #760/#761, passes 23 cases without omissions. The original four
unsupported-argument failures and authored test/preflight mistakes remain
unsuccessful evidence in the
[receipt](../../../devtools/data/peptide_course_receiving_759_761_20261115.json).
No runtime API, scientific method, dependency or native binary changes.
