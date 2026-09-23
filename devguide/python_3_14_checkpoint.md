# Python 3.14 paired-support checkpoint

**Role:** dated operational checkpoint, not a support declaration or release gate.
**Observed:** 2026-09-23 on Linux x86-64 unless another platform is named.
**Owning work:** [MolSysMT Python 3.14 proposal](pending_proposals/extend_molsysmt_python_support_to_3_14.md), `uibcdf/molsysviewer#93`, and the coordinated Conda release in `uibcdf/molsysmt#195` / `uibcdf/molsysviewer#82`.

## Where we stand

The MolSysMT and MolSysViewer `python-3.14-support` branches declare
`>=3.11,<3.15` in their wheel metadata. That is **candidate source metadata**, not
public support: MolSysViewer requires `molsysmt>=0.22.0`, whereas the MolSysMT
source checkout still has a 0.21.x development identity. The published/staged
0.22.0/0.23.1 pair remains bounded to Python 3.11–3.13 and must complete its
own release gate without reinterpreting those immutable artifacts as 3.14
packages.

| Boundary | Evidence available | Still missing |
| --- | --- | --- |
| MolSysMT core on 3.14 | Linux installed wheel, 99 Rust exports, bundled BCIF conversion, and 641 selected installed-wheel tests with 12 workers passed. | Full scientific/source suite with representative optional backends; exact Conda candidate and installed matrix. |
| MolSysViewer core on 3.14 | The paired full Python source suite passed on hosted Linux and macOS, 2,090 tests collected per job; its Linux real Qt integration and opt-in full molecular render passed with the local UIBCDF-only Qt family. | Resolver-consistent, versioned Conda pair; installed-package gates on each claimed platform. |
| UIBCDF Qt 6.10.1 family | Five aligned local Linux packages work together on Python 3.14. On 2026-09-23, disposable Python 3.11, 3.12, and 3.13 Shiboken/Essentials/Addons variants each passed Conda package tests, an independent clean installation, imports, and local HTML loading in WebEngine under Xvfb. Qt Positioning/WebEngine native packages were reused across minors. | Commit and validate interpreter-parametric recipes and a staging matrix; cross-platform builds; exact staged-channel Viewer Qt tests. Local variants are not uploaded release artifacts. |
| Public support claim | The lower public dependency chain, including py-mmcif, resolves on Python 3.14; the existing 3.11–3.13 staging campaign has separate gates. | New immutable pair, clean channel installations, and suite-level `admitted` decision before changing any public badge. |

The three local binding variants are intentionally **per-interpreter** Conda
artifacts. Their `.abi3.so` filenames do not make the packages universal:
their metadata includes the selected `python_abi` minor. Each Python 3.11–3.14
cell therefore needs its own tested Shiboken, Essentials, and Addons artifact
unless a separately validated ABI3 packaging contract replaces this one.

## Next gates in order

1. Finish and verify the existing MolSysMT 0.22.0 / MolSysViewer 0.23.1
   staging and public-installation path for Python 3.11–3.13. The 3.14 source
   branches can advance in parallel, but must not silently widen those
   pre-existing package coordinates.
2. Parameterize the three binding recipes and their smoke tests; render and
   build the committed recipe for each Python 3.11–3.14 Linux cell. Retain
   exact artifact hashes, package-test exits, clean-solve provenance, and
   UIBCDF-only WebEngine evidence. Replace the old direct-main upload route
   with a reviewed staging-first candidate route before any upload.
3. Run MolSysMT's full Python 3.14 test and scientific-evidence gates with
   representative optional dependencies. Build an exact ABI3 Conda candidate
   and verify its extension and BCIF path after clean installation.
4. Build the aligned Qt family and exact MolSysMT/Viewer pair for every
   claimed native platform. Validate Python 3.11–3.14 clean installations,
   package provenance, Viewer resources, real Qt integration where claimed,
   and the older Python lanes. Linux/macOS are supported-platform targets;
   Windows remains experimental until it earns comparable evidence.
5. Publish only after the exact-commit and channel gates pass. Verify the
   released coordinates independently, then request the MolSysSuite Python
   support status transition. Standard GIL-enabled CPython 3.14 is in scope;
   free-threaded 3.14t is not.

## Handoff discipline

This checkpoint is the compact orientation surface. The linked pending
proposal owns MolSysMT's analysis and acceptance criteria; the Viewer and Qt
issues own their component evidence. Update this checkpoint when a gate
changes, with the date, exact commit/artifact or run, platform, and whether
the result came from source, a local package, staging, or a public channel.
Do not turn a local clean installation into a channel claim.
