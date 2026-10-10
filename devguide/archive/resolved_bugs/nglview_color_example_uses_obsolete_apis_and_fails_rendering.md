---
summary: NGLView color example uses obsolete APIs and fails rendering.
issue: uibcdf/molsysmt#361
status: resolved
opened: 2026-10-09
closed: 2026-10-09
severity: low
verification: reproduced
area: [docs, api]
guard: devtools/tests/test_public_api_docs.py::test_nglview_color_docstring_renders_without_rst_errors
normative:
blocked_by: []
supersedes: []
---

# NGLView color example uses obsolete APIs and fails rendering

**Reported:** 2026-10-09, bounded follow-up to the rendering debt in #144.
**Status:** Resolved for the public example, rendered API text and selection-aligned tutorial.

## What

A real one-page Sphinx build fails on the public `set_color_by_value` docstring:

```bash
python -m pytest devtools/tests/test_public_api_docs.py::test_nglview_color_docstring_renders_without_rst_errors \
  --receptor=llm -n12
# 1 failed: Unknown target name: "yyy".
```

Its example calls `msm.physchem.charge` and `nglview.color_by_value`; neither is
exported. Compiling its charge statement raises `SyntaxError: invalid character
U+FFFC`. It also calls the default viewer instead of explicitly requesting
NGLView and fetches a remote PDB entry for a basic local example.

## How

The original docstring has a `YYY` reference with an invalid target definition.
Its executable examples drifted from the public exports and viewer default.
The runtime function still has the expected color and normalization routes;
this report does not diagnose a failed computation from those prose defects.

## Why

Users cannot execute the example and the public API page emits a rendering
error. Correcting these existing surfaces is bounded stabilization. General
Sphinx warning cleanup remains accepted post-1.0 debt under #144.

## What is measured and what is assumed

The pre-repair rendering guard fails through Sphinx HTML, Autodoc and Napoleon,
with warning-is-error enabled. It preserves the actual warning stream instead
of matching strings or suppressing diagnostics. Two Sphinx 11 deprecation
warnings are emitted by the installed Sphinx extension; they are separate from
this API page's unknown-target error.

The initial combined render/doctest run was interrupted because the old example
starts with remote retrieval; it is not claimed as a completed failing doctest.
Compilation and export inspection independently verify the example defects.
The replacement uses bundled data and an explicitly requested NGLView widget.

## What was refuted

The default colormap name is not a runtime bug: ArgDigest resolves it to a
Matplotlib colormap before execution. Changing visualization backend behavior
or hiding Sphinx diagnostics is unnecessary for this repair.

## Scope and exclusions

Keep the function signature and runtime body unchanged. Document the implemented
atom/group levels and four representations, selection/value alignment and
normalization limits. Python tests check widget representation submission;
no browser rendering or MolSysViewer candidate qualification is claimed.

## Acceptance criteria

The actual API text renders without page diagnostics. Its public example executes
without remote access and the existing numerical-scalar/color-scheme tests pass.
Foundations, Toolbox, Cookbook and the relevant course module describe explicit
backend choice and value alignment.

## Provenance

Linux, Python 3.14.7, shared `molsyssuite@uibcdf_3.14` development environment,
Sphinx 9.1.0 and NGLView 4.0.1, 2026-10-09.

## Resolution

The public docstring uses the existing `get_charge` and `set_color_by_value`
exports, bundled local data and an explicitly selected NGLView backend. The
unsupported placeholder target and invalid Python character are removed. Its
parameters describe the implemented atom/group modes and normalization. The
function signature and executable body are unchanged, verified by AST comparison.

Seven distinct tests pass: three API guards, the public doctest and three
existing color/scalar regressions. The NGLView API guard additionally executes
the actual docstring, rejects remote retrieval, and inspects the submitted
representation to assert color-scheme reconstruction and one color per supplied
value. Empty prose or an unexecuted/stub example cannot satisfy that guard.
The rendered page has an empty diagnostics stream; expected H5MSM migration and
installed Sphinx deprecation warnings remain separately visible.

Foundations, Toolbox, the NGLView Cookbook and Common Core Module 6 describe the
backend/alignment contract. The Toolbox example now counts selected protein
groups before constructing values. Its one notebook was re-executed in the
shared Python 3.14.7 environment with no error outputs; the generated run mark
records the new code fingerprint. Initial execution was blocked by the sandbox's
local socket restriction and used a mismatched PATH launcher. The successful
retry explicitly selected the existing Python 3.14 Jupyter tools and permitted
local kernel sockets; no auxiliary environment was created. Browser rendering
and the whole-site warning inventory remain outside this bounded qualification.
