---
summary: Native NGLView conversion forwards MolSysMT validation keywords to widgets
issue: uibcdf/molsysmt#630
status: resolved
opened: 2026-11-06
closed: 2026-11-06
severity: low
verification: reproduced
area: [form, deps]
guard: tests/form/nglview_NGLWidget/test_conversion_boundary.py
normative:
blocked_by: []
supersedes: []
---

# Keeping validation inside the native NGLView adapter

**Reported:** 2026-11-06 during the optional-provider receiving under #524.

## What

The native MolSys-to-NGLWidget converter forwards `skip_digestion=True` to
`show_molsysmt`. With supported public NGLView 3.0.4, this falls back to the
MolSysMT trajectory adapter, which forwards arbitrary widget kwargs. Traitlets
then receives a MolSysMT-only keyword and emits an unrecognized-argument
DeprecationWarning. The provider's documentation says a later release will
raise this error. Ordinary NGLView 4.0.1 does not reproduce this warning.

## How

The frozen public 3.0.4/Python 3.12 receiving has 93 passing cases and 43 such
warnings. The new boundary guard elevates only this warning to an error:

```bash
python -m pytest --receptor=llm -n 12 \
  tests/form/nglview_NGLWidget/test_conversion_boundary.py
```

Before repair it exits one with one failure through native conversion,
`show_molsysmt`, NGLWidget and Traitlets. The floor profile and original XML
are recorded as `524-nglview-floor312-validation_keyword_baseline*` in the
ignored provider-review cache. This is not a frontend-rendering failure or a
claim that current 4.0.1 fails.

## Why

A validated MolSysMT delegation flag is not a third-party widget option.
Passing it creates warnings today and breaks a future strict constructor.
Removing that leak preserves the scientific data and requested selection.
The direct public adapter must also declare its optional NGLView dependency,
so provider absence has the same typed diagnostic as other supported routes.

## Acceptance criteria

- Public native conversion on supported 3.0.4 emits no validation-keyword warning
  and preserves atom/structure counts and existing topology/coordinate contracts.
- The direct converter guards the optional provider and does not run its body
  when that provider is absent.
- Actual minimum/newer finite Python/widget/HTML receiving passes; no browser or
  complete installed-package qualification is inferred.
- Publish source, this owning record and the addressable guard before closure.

## Provenance

Linux source checkout; existing Python 3.12/public support-floor overlays and
Python 3.14/default bridge. Public NGLView 3.0.4 sdist is hash-verified; the
newer 4.0.1 route uses selected verified public Conda payload files. All source,
public-artifact, preflight and native-exit boundaries remain in #524's receipt.
No environment was created or replaced and no new native backend was built.

## Resolution — 2026-11-06

Source `e5d1dd0f853cdd69da1908bdd4b60b972441bf4b` consumes MolSysMT's validation
flag locally and declares the optional NGLView dependency on the direct native
converter. The mirrored guard elevates the actual unrecognized-keyword warning
and checks the represented atom/structure counts. A second case exercises the
real dependency decorator's absent-provider diagnostic.

The strict pre-repair minimum counterexample fails once. Post-repair minimum
receiving passes 95; final complete NGLView 3.0.4/Python 3.12 and 4.0.1/Python 3.14
receiving each pass 104, including the later #631 guards/doctest, without
omissions. The validation-keyword warnings disappear on 3.0.4. Ordinary 4.0.1
never reproduced the original warning. Counts overlap.

The [portable receipt](../../../devtools/data/nglview_runtime_receiving_524_630_631_20261106.json)
retains both providers, original outcomes, explicit old-SMonitor bridge exception
and source/installed/frontend limits. Public source delivery and actual issue
closure are recorded separately. #524 remains partial for its remaining route,
actual Viewer and clean installed closure.
