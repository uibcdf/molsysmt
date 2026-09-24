---
summary: WindowsPath demo resources are rejected by get_form on Windows.
issue: uibcdf/molsysmt#241
status: active
opened: 2026-09-24
closed:
severity: high
verification: reproduced
area: [basic, forms, windows]
guard:
normative:
blocked_by: []
supersedes: []
---

# WindowsPath demo resources are rejected by get_form on Windows

**Reported:** 2026-09-24 by the coordinated MolSysMT/MolSysViewer Python
3.14 source-pair CI run `uibcdf/molsysviewer` Actions run `35970837689`.
**Status:** Active; the local source fix passes on Linux, while Windows
confirmation on the exact updated source pair is still pending.

## What

On Windows, `molsysmt.systems` returns a `pathlib.WindowsPath` for bundled
resources. Passing one to the public `molsysmt.get_form()` raises
`NotSupportedFormError` naming `pathlib.WindowsPath`. MolSysViewer's demo
catalogue passes that resource directly to `new_view()`, so its Windows
Python 3.14 source-pair run failed hundreds of downstream tests after the
installation and test collection had succeeded.

The reproducer on the affected platform is:

```python
import molsysmt as msm
msm.get_form(msm.systems["benzamidine"]["benzamidine.pdb"])
```

## How

`molsysmt/basic/get_form.py` converted only `PosixPath` to a filename string
before the string/file detectors ran. A Windows `Path` therefore reached the
class-form sweep, where no detector could claim it. The fix checks `Path`,
the base class of the native concrete path on both platforms, at that same
public boundary. This retains the previous absolute-path normalization.

## Why

Bundled demo systems are a public entry point and are consumed by the hard
MolSysViewer dependency. The failure affects Windows regardless of Python
minor; it was discovered in the 3.14 expansion because that is the first
hosted Windows source-pair full-suite run. It is not a reason to make any
optional viewer backend mandatory.

## What is measured and what is assumed

- Measured: the Windows job in run `35970837689` installed both sources and
  collected the Viewer suite, then reported `NotSupportedFormError` for
  `pathlib.WindowsPath` from `molsysmt/basic/get_form.py:198` across grouped
  setup and call failures.
- Measured: the focused native-path detection/conversion guard passes for
  PDB, H5MSM, and compressed BCIF on Linux/Python 3.14.7 after the source
  change.
- Not yet measured: the fix running on Windows. The result must come from
  a workflow that pins the corrected MolSysMT commit.

## What was refuted

- The initial Windows test-collection failure on `resource` was a separate
  development-benchmark portability bug in MolSysViewer. After it was fixed,
  the Windows suite ran and exposed this application-level defect.
- NGLView is not involved in this failure; it remains an optional backend.

## Scope and exclusions

This report covers the public `get_form()` path-normalization boundary and
its paired Viewer demo load. Other PosixPath-specific helpers and unrelated
Windows-only Viewer failures are not silently treated as resolved here.

## Acceptance criteria

- A platform-native bundled `Path` is detected and converted by MolSysMT.
- The exact corrected source pair passes the relevant Viewer demo tests on
  Windows/Python 3.14.
- The guard is
  `tests/basic/test_get_form.py::test_bundled_path_is_detected_and_converted_on_native_platform`.

## Provenance

GitHub Actions `windows-2025` runner, CPython 3.14, 2026-09-24; Viewer
source-pair run `35970837689`, pinning MolSysMT `93b8d1857`. The local
focused follow-up used Linux x86-64, Python 3.14.7, and the editable
MolSysMT `python-3.14-support` branch.
