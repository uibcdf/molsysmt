---
summary: WindowsPath demo resources are rejected by get_form on Windows.
issue: uibcdf/molsysmt#241
status: active
opened: 2026-09-24
closed:
severity: high
verification: reproduced
area: [basic, form]
guard:
normative:
blocked_by: []
supersedes: []
---

# WindowsPath demo resources are rejected by get_form on Windows

**Reported:** 2026-09-24 by the coordinated MolSysMT/MolSysViewer Python
3.14 source-pair CI run `uibcdf/molsysviewer` Actions run `35970837689`.
**Status:** Fixed and verified on the `python-3.14-support` source branch,
but still active until the fix and guard land in `main`. The exact corrected
source pair passed its native-path guard and full MolSysViewer Python suite
on Windows in run `35975122014`.

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
- Measured: the installed native-path guard passed for PDB, H5MSM, and
  compressed BCIF in the Linux, macOS, and Windows jobs of source-pair run
  `35975122014`. The same jobs completed the full MolSysViewer Python suite.
  That run checked out MolSysMT `86dcb5d078d8cbb45c38500e452944811fc5a5bc`
  and MolSysViewer `88a6c75a08c3e3660b626c697183ef53c7297852`.

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

## Outcome to date

The branch implementation in MolSysMT
`e865b72ce20358c1bd33be318c170a91c18ff145` normalizes any native
`pathlib.Path` before the form detectors run. The addressable guard
`tests/basic/test_get_form.py::test_bundled_path_is_detected_and_converted_on_native_platform`
would fail again if Windows paths stopped being accepted or converted.
Hosted source-pair run `35975122014` passed all three Python 3.14 jobs,
including the installed guard and the full Viewer suite on Windows.
Merge the fix and guard into `main` before archiving this report or closing
the issue. This source test does not establish a published or staged Conda
package pair.
