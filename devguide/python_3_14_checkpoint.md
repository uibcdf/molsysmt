# Python 3.14 paired-support checkpoint

**Role:** dated operational checkpoint, not a support declaration or release gate.
**Observed:** 2026-09-24 on Linux x86-64 unless another platform is named.
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
| MolSysMT core on 3.14 | Linux installed wheel, 99 Rust exports, bundled BCIF conversion, and 641 selected installed-wheel tests with 12 workers passed. An exact local ABI3 Conda candidate also passes the clean installed-pair validator. | Full scientific/source suite with representative optional backends; staged and cross-platform installed matrices. |
| MolSysViewer core on 3.14 | The paired full Python source suite and installed MolSysMT native-path guard passed on hosted Linux, macOS, and Windows in run `35975122014`; its Linux real Qt integration and opt-in full molecular render passed with the local UIBCDF-only Qt family. An exact local noarch candidate resolves and installs alongside the MolSysMT candidate on Linux/Python 3.14. | Remote staged-pair and installed-package gates on each claimed platform; an installed-test harness that does not inject source packages. |
| UIBCDF Qt 6.10.1 family | Five aligned local Linux packages work together on Python 3.14. Disposable Python 3.11–3.13 binding variants passed Conda package tests and clean-install WebEngine smokes. The revised variant-selected recipes now passed package tests and clean five-package installations on Python 3.12–3.14; Qt Positioning/WebEngine native packages were reused across minors. The 3.14 packages also passed real Viewer Qt integration and full-render tests. No canonical PySide6 was installed. | Build the revised recipes for 3.11; establish a staging matrix, cross-platform builds, and exact staged-channel Viewer Qt tests. Local variants are not uploaded release artifacts. |
| Public support claim | The lower public dependency chain, including py-mmcif, resolves on Python 3.14; the existing 3.11–3.13 staging campaign has separate gates. | New immutable pair, clean channel installations, and suite-level `admitted` decision before changing any public badge. |

The three local binding variants are intentionally **per-interpreter** Conda
artifacts. Their `.abi3.so` filenames do not make the packages universal:
their metadata includes the selected `python_abi` minor. Each Python 3.11–3.14
cell therefore needs its own tested Shiboken, Essentials, and Addons artifact
unless a separately validated ABI3 packaging contract replaces this one.

On 2026-09-24, a lean Python 3.14 source-tree collection was advanced past
NGLView, Biopython, and OpenFF-only tests by making their optional-backend
skips explicit. A new distribution test protects NGLView's soft-only status;
MolSysViewer's own runtime manifest guard protects the same boundary. The
source-tree Rust extension built locally. Collection still reaches tests that
need optional OpenMM, so no full MolSysMT suite result is claimed from this
minimal environment.

The first hosted three-platform Viewer source-pair attempt passed Linux and
macOS but exposed `uibcdf/molsysmt#241` on Windows: native `WindowsPath`
demo resources were rejected by `get_form()`. The `Path`-base-class fix and
native-path guard now pass on the exact installed sources on all three hosted
platforms. MolSysViewer also corrected its own `PathLike` digestion boundary
and separate Windows portability failures. Run `35975122014` checked out
MolSysMT `86dcb5d078d8cbb45c38500e452944811fc5a5bc` and MolSysViewer
`88a6c75a08c3e3660b626c697183ef53c7297852`; all three jobs passed the
guard and full Viewer Python suite. This closes the source-pair Windows
compatibility defect, but it is not a staged-channel installation or an
optional Qt-host test on Windows.

The revised Linux/Python 3.12 binding artifacts have SHA-256 values
`1faa8deecc53c65b0275c4716e27e50286f6ab5e6ca69f740e979085af8a5887`
(Shiboken),
`45a398759f04c24e196e6e2ff82388eb1161a0cc83480c85df14be358d9dfcea`
(Essentials), and
`edbe013fcac09b0e62e39d3beaa25b696d534b424414d6033c157d8ee8720dbd`
(Addons). All three finalized package records require Python
`>=3.12,<3.13.0a0` and `python_abi 3.12.* *_cp312`. The clean Conda
environment recorded four of the five UIBCDF artifacts from the indexed
local channel and Addons from its build directory; that archive is
byte-identical to the copied channel artifact. This is local-artifact
evidence, not a complete channel-provenance claim.

On 2026-09-23, the revised Linux/Python 3.13 builds passed Conda package
tests with `CPU_COUNT=12`. Their SHA-256 values are
`8a944dd7c0fb74d2978d882fe64df519adaf047e17f4176bb24708ce25b183c5`
(Shiboken),
`6f63b866862098f8874609260afdc85682b2d93301bd6a44aaa59d916db481db`
(Essentials), and
`7cf4718bae6bb9e95f1815e50cab711b7a03ac848eff86230a2c4144fcd6ef00`
(Addons). All three final package records require Python
`>=3.13,<3.14.0a0` and `python_abi 3.13.* *_cp313`. A fresh offline
environment selected Python 3.13.15, Qt 6.10.1 and all five local UIBCDF
packages without canonical PySide6. The Addons package-cache record initially
pointed at its local build directory; after an explicit reinstall from the
byte-identical indexed-channel file, all five installed records named the
local channel. The ordinary Addons and Xvfb local-HTML WebEngine smokes
passed. The Xvfb smoke required running outside the restricted sandbox because
the sandbox could not open its display. This is local-channel evidence only,
not evidence for `uibcdf/label/staging` or the public channel.

The revised Linux/Python 3.14 builds also passed Conda package tests with
`CPU_COUNT=12`. Their SHA-256 values are
`0db537f21bac4ef73e01ccfe34fc098f9e49c61f9cc71d858454c7d9747d0391`
(Shiboken),
`dee2b2dc0092c50ab1a7bbeba215b793d5c1a2d991b15efc3a0aafcb7f290c1c`
(Essentials), and
`a1d3a168f1fb39293d652be2979db6332abdc87d88f25dc01b86d809b8fcb8c2`
(Addons). Their finalized package records require Python
`>=3.14,<3.15.0a0` and `python_abi 3.14.* *_cp314`. A fresh offline
environment installed all five exact artifacts from an indexed local
channel, with matching installed-record hashes and no canonical PySide6.
Ordinary Addons and Xvfb WebEngine smokes passed. In a separate environment
with those same exact local artifacts, three real-Qt Viewer integration tests
and the opt-in full molecular render passed under Xvfb. That second
environment contains development source versions of MolSysMT and Viewer;
the result is local Qt/application evidence, not a resolver-clean,
versioned Conda pair or a staged-channel claim.

## Local Conda pair integration

On 2026-09-23, temporary **local-only** tags `0.22.1`/`0.23.2` built an ABI3
MolSysMT archive and a noarch MolSysViewer archive. A fresh Linux/Python
3.14.7 environment resolved both exact versions from an indexed local channel
with the `uibcdf/label/staging`, `uibcdf`, and `conda-forge` dependency
channels. The installed-pair validator passed version identity, Conda records,
the native extension, bundled BCIF conversion, and Viewer resources; the
separate Rust validator checked all 99 exports. Both packages were built with
`--no-test` to break the packaging cycle, so these post-install checks are
the evidence, not recipe-test results.

An additional installed Viewer PDB-text probe then exposed
`uibcdf/molsysmt#238`: `get_form` imported optional Biopython from the
one-letter amino-acid detector before reaching the PDB-text detector. The
uncorrected pair's two Viewer integration tests failed without Bio. MolSysMT
commit `639892a6f` removed that optional import using an equivalent
standard-library count; the focused regression failed before the change and
passed after it, and all 22 `test_get_form.py` cases passed.

The corrected MolSysMT archive was built with another **local-only** tag,
`0.22.2`, and has SHA-256
`d7d421c831b92fba424c665f7adb209f41e9a4f175208acfc017172d132be353`.
The unchanged MolSysViewer `0.23.2` archive has SHA-256
`ea64e225001537b059791f610954f99d9d022b1221e6788e085469f992bad712`.
The second fresh Linux/Python 3.14.7 environment resolved both exact local
files; the two installed Conda records contain the same hashes and local
channel URLs. Biopython was absent. The installed-pair and 99-export Rust
validators passed, as did the two-case no-Biopython regression against the
installed package. A direct four-atom PDB-text smoke classified the form,
converted it to `molsysmt.MolSys`, and loaded it through `MolSysView` with
the same atom count.

The installed-pair validator now includes that PDB-text-to-Viewer smoke as a
release gate. Its new unit tests pass, and running it against the uncorrected
local `0.22.1` pair fails on the absent `Bio` import; running the identical
validator against the corrected `0.22.2` pair passes. This is a tested gate
for this regression, not a claim that the full Viewer test suite passes.

The two existing Viewer integration test functions are not yet reusable as
installed-package evidence: its `tests/conftest.py` inserts the Viewer
checkout into `sys.path`, while disabling that conftest removes the
`_test_message_log` fixture they require. The direct installed smoke above
verifies the user behavior but does not substitute for an installed-test
harness. These local tags and archives are not release-version decisions,
remote staging artifacts, or a cross-platform support claim.

## Next gates in order

1. Finish and verify the existing MolSysMT 0.22.0 / MolSysViewer 0.23.1
   staging and public-installation path for Python 3.11–3.13. The 3.14 source
   branches can advance in parallel, but must not silently widen those
   pre-existing package coordinates.
2. Finish the revised binding-recipe matrix for the remaining Python 3.11
   Linux cell; the 3.12–3.14 cells passed. Retain
   exact artifact hashes, package-test exits, clean-solve provenance, and
   UIBCDF-only WebEngine evidence. Replace the old direct-main upload route
   with a reviewed staging-first candidate route before any upload.
3. Run MolSysMT's full Python 3.14 test and scientific-evidence gates with
   representative optional dependencies. Repeat the now-proven local ABI3
   and installed-pair checks on an immutable staging candidate.
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
