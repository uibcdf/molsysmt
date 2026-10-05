---
summary: Exported views retain legacy transparent-background HTML headers.
issue: uibcdf/molsysmt#199
status: resolved
opened: 2026-09-02
closed: 2026-10-05
severity: medium
verification: measured
area: [docs]
guard: devtools/tests/test_static_view_transparency.py
normative:
blocked_by: []
supersedes: []
---

# Exported views retain legacy transparent-background HTML headers

**Reported:** MolSysViewer's incoming request in uibcdf/molsysmt#199.
**Status:** resolved through a provider-generated header migration.

## What

The provider fixed embedded transparent exports in uibcdf/molsysviewer#34,
but previously exported MolSysMT documents retained their old HTML head.
On 2026-10-05, 47 of 49 transparent exports lacked the active embedded
`html { color-scheme: light dark; }` declaration.

```bash
python -m pytest devtools/tests/test_static_view_transparency.py::test_all_transparent_exports_install_embedded_scheme_before_body
```

## How

The browser's base canvas depends on the used color scheme of the embedded
document. Transparent body/HTML/WebGL alone does not select that scheme. The
fix is an executable script in the exported head, guarded by
`window.self !== window.top`, rather than a runtime-only change.

The public `MolSysView().export.html(..., background='transparent')` produced
a current template. `docs/generate_static_views/refresh_transparent_headers.py`
replaced the legacy head script in 47 documents. It verified identical body
bytes in all 49 documents and recorded hashes. Scientific payloads, controls,
runtime references and original scene producer versions were not regenerated.
The two already-correct exports needed no change.

## Why

The documentation embeds these files in both themes. Updating the shared
runtime cannot fix an HTML header retained in an exported file. A white
browser canvas under a dark page makes the visual documentation incorrect.

## What is measured and what is assumed

Measured: all 49 transparent exports pass the active-head regression guard.
Six Chromium checks execute committed heads in actual iframes: three
representative files, each in a white and a dark host. Computed scheme is
`light dark`, body background is transparent, and every screenshot pixel
matches its host (white or RGB 20/24/31).

The [header artifact](../../../devtools/data/static_view_headers_20261005.json)
records all original/current hashes, unchanged-body hashes, the provider and
browser observations. These tests isolate the reported header defect. They
do not certify scientific scene replay, browser/Qt interaction geometry or
MolSysViewer's session workflow.

## What was refuted

Replacing `viewer.js` alone does not regenerate the head. A declaration in
an inert JSON script, a comment or the body also does not install the
before-paint correction; negative controls reject these placements.

## Scope and exclusions

The transparent HTML head only. No scene recomputation, theme-container CSS
change, runtime replacement, public API change or Viewer checkout edit.

## Acceptance criteria

All affected exports install the provider correction before their body.
Migration retains their body bytes and is idempotent. The guard protects
active placement and rejects missing CSS, inert or late corrections. Actual
embedded browser screenshots qualify both host themes.

## Provenance

Linux, 2026-10-05; local MolSysViewer source and export version recorded in the
artifact. Chromium 143.0.7499.4, headless browser with actual DOM/CSS rendering.
The three existing Viewer sandbox files and its four-commit behind state were
preserved; this work does not coordinate a provider update.
