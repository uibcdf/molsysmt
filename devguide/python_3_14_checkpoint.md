# Python 3.14 paired-support checkpoint

**Role:** dated operational checkpoint, not a support declaration or release gate.
**Observed:** 2026-09-25 for the public release milestone; older sections retain their dated, narrower observations.
**Owning work:** [MolSysMT Python 3.14 proposal](pending_proposals/extend_molsysmt_python_support_to_3_14.md), `uibcdf/molsysviewer#93`, and the coordinated Conda release in `uibcdf/molsysmt#195` / `uibcdf/molsysviewer#82`.

## Public pair release — 2026-09-25

MolSysMT [0.22.4](https://github.com/uibcdf/molsysmt/releases/tag/0.22.4)
and MolSysViewer [0.23.4](https://github.com/uibcdf/molsysviewer/releases/tag/0.23.4)
are published GitHub Releases on exact tested source commits
`e28ceb9ea0de0cc86bc370e5aff1e96c4cc71c69` and
`cf427942d0b08a1c5c60f262c6a6b33f248d6f8b`. Their candidate branches
were merged into `main` only after the tags. The five MolSysMT ABI3 build-3
files and the one Viewer noarch build-5 file were promoted from staging;
their promotion actions verified the exact source and public-label SHA-256
and retained receipts. Each workflow's subsequent duplicated Conda-search
step falsely exited 1 after printing the correct public URL. Independent
queries found all six files in `uibcdf`; the defect is tracked by
`uibcdf/molsysmt#246`, `uibcdf/molsysviewer#105` and
`uibcdf/molsyssuite#48`. Do not represent those red job conclusions as green.

The decisive clean-install check is the [public-channel pair matrix](https://github.com/uibcdf/molsysmt/actions/runs/36129993869):
21/21 jobs and 20/20 installations passed across Linux x86-64/ARM, macOS
Intel/ARM, Windows x86-64 and Python 3.11–3.14. Every cell selected the exact
build numbers, checked `uibcdf` public-channel provenance and digest-bearing
Conda records, version identity, the Rust extension, bundled BCIF conversion,
PDB-text-to-Viewer integration and packaged Viewer resources. The staging
matrix remains separately green in run `36121427459` (20/20). This closes
the public *pair-installation* milestone; it does not make every optional
backend, standalone Qt platform or scientific workflow a supported 3.14
claim. MolSysSuite-wide admission remains the separate decision in
`uibcdf/molsyssuite#29`.

The Viewer npm runtime is published at 0.23.4 and its CDN asset is reachable.
The Viewer publication has an explicitly bounded pre-1.0 exception for a
visible-window Qt observation and complete hosted E2E certification
(`uibcdf/molsysviewer#100`); these are not 1.0 passes. The two Zenodo
records are now public and independently verified. MolSysMT 0.22.4 is
[version DOI 10.5281/zenodo.22959294](https://doi.org/10.5281/zenodo.22959294)
in concept family `10.5281/zenodo.1298752`; its archived file is
`uibcdf/molsysmt-0.22.4.zip` (150,833,579 bytes,
`md5:9927d9511e5946eb708254d89d427d0d`). Viewer 0.23.4 is
[version DOI 10.5281/zenodo.22959304](https://doi.org/10.5281/zenodo.22959304)
in concept family `10.5281/zenodo.18072956`; its archived file is
`uibcdf/molsysviewer-0.23.4.zip` (23,694,420 bytes,
`md5:2cfe76a5ea9ec2894964926db81c2609`). Both records are published
and identify the correct GitHub repository. These inventories are source
archives, not Conda or npm artifact inventories. The first 900-second
workflows expired before ingestion finished; the MolSysMT verifier also
had an overly strict tree-tag predicate corrected under
`uibcdf/molsysmt#247`.
The read-only reruns on 2026-09-26 passed on current `main`:
[MolSysMT run 36220716162](https://github.com/uibcdf/molsysmt/actions/runs/36220716162)
reported 0.22.4 and its DOI, and
[Viewer run 36220722008](https://github.com/uibcdf/molsysviewer/actions/runs/36220722008)
reported 0.23.4 and its DOI. These manual dispatches verify public
archives; they do not change either immutable release tag.

## Earlier source and staging checkpoint — 2026-09-24

The table and measurements below describe the earlier source/staging state.
They remain evidence for how this release was reached, not the current public
channel status.

The MolSysMT and MolSysViewer `python-3.14-support` branches declare
`>=3.11,<3.15` in their wheel metadata. That is **candidate source metadata**, not
public support: MolSysViewer requires `molsysmt>=0.22.0`, whereas the MolSysMT
source checkout still has a 0.21.x development identity. The published/staged
0.22.0/0.23.1 pair remains bounded to Python 3.11–3.13 and must complete its
own release gate without reinterpreting those immutable artifacts as 3.14
packages.

| Boundary | Evidence available | Still missing |
| --- | --- | --- |
| MolSysMT core on 3.14 | Linux installed wheel, 99 Rust exports, bundled BCIF conversion, and 641 selected installed-wheel tests with 12 workers passed. A dependency-rich source-pair environment additionally passed 99 scientific-truth cases, 865 basic cases, 475 focused form/validation cases, 39 OpenMM cases, and 371 offline-safe build cases; these selections overlap and must not be summed. The native peptide default also passed 40 extended LEaP-parity cases. The exact staged ABI3 package passed the installed-pair validator in 20/20 cells across five native platforms and Python 3.11–3.14. | Complete source suite in a metadata-consistent environment; broader staged-package scientific gates. |
| MolSysViewer core on 3.14 | The paired full Python source suite and installed MolSysMT native-path guard passed on hosted Linux, macOS, and Windows in run `35975122014`. Newer source-built pip installations passed the Viewer installed-pair integration step and full Python suite on the same three hosted platforms in run `35988170629`. Linux real Qt integration and opt-in full molecular render passed with the local UIBCDF-only Qt family. The exact staged noarch package passed the installed-pair and channel-provenance gate in all 20 cells with MolSysMT. | Broader staged-package Viewer suite and supported-platform Qt integration; coordinated release gate. |
| UIBCDF Qt 6.10.1 family | Five aligned local Linux packages work together on Python 3.14. Disposable Python 3.11–3.13 binding variants passed Conda package tests and clean-install WebEngine smokes. The revised variant-selected recipes now passed package tests and clean five-package installations on Python 3.12–3.14; Qt Positioning/WebEngine native packages were reused across minors. The 3.14 packages also passed real Viewer Qt integration and full-render tests. No canonical PySide6 was installed. | Build the revised recipes for 3.11; establish a staging matrix, cross-platform builds, and exact staged-channel Viewer Qt tests. Local variants are not uploaded release artifacts. |
| Public support claim | The lower public dependency chain, including py-mmcif, resolves on Python 3.14; the new immutable pair passed 20/20 staging installed cells. The existing 3.11–3.13 staging campaign has separate gates. | Scientific and Qt coverage where claimed, coordinated public-channel release and verification, and suite-level `admitted` decision before changing any public badge. |

The three local binding variants are intentionally **per-interpreter** Conda
artifacts. Their `.abi3.so` filenames do not make the packages universal:
their metadata includes the selected `python_abi` minor. Each Python 3.11–3.14
cell therefore needs its own tested Shiboken, Essentials, and Addons artifact
unless a separately validated ABI3 packaging contract replaces this one.

On 2026-09-24, a lean Python 3.14 source-tree collection was advanced past
NGLView, Biopython, OpenFF, and OpenMM-only tests by making their
optional-backend skips explicit. A new distribution test protects NGLView's
soft-only status; MolSysViewer's runtime manifest guard protects the same
boundary. The source-tree Rust extension built locally. Full `tests/`
collection now exits successfully with pytest-receptor reporting 10,084
collected cases and 40 deselections. Focused non-OpenMM mass/charge cases
passed with 12 workers (2 passed, 5 function-level skips); the OpenMM-only
modules skip when that backend is absent. The real imports still run when
OpenMM is installed, so a broken installed backend is not hidden. This is
collection hygiene, not a full MolSysMT suite or scientific result.

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

## Dependency-rich Python 3.14 source checks

On 2026-09-24, a bounded 12-worker `tests/` attempt in the lean Python 3.14
environment stopped after 307 seconds with 1,795 passed, 138 failed, 28
errors, and 19 skipped. It executed only 1,980 of 10,058 selected cases;
pytest-xdist overshot `--maxfail=20` while workers were active. The largest
groups involved absent optional MDAnalysis, OpenMM, Biopython, NGLView,
PDBFixer, or OpenFF, and PDB-ID downloads failed because that sandbox had no
network. This diagnostic run is not a MolSysMT full-suite result and must not
be cited as a Python 3.14 regression count.

A separate disposable environment under `build/py314-scientific-test` resolved
Python 3.14.7 with conda-forge AmberTools 26.0, OpenMM 8.6.1, MDAnalysis
2.10.0, Biopython 1.88, OpenFF Toolkit, NGLView, PDBFixer, and py-mmcif 1.1.1.
ArgDigest 0.13.0, DepDigest 0.11.0, PyUnitWizard 0.26.0, and SMonitor 0.16.0
came from `uibcdf`. The exact source branches built and installed as wheel
versions MolSysMT `0.21.0+724.gf26727c63` and MolSysViewer
`0.23.0+107.g0693bfd4`; the former's installed Rust validator passed all 99
exports. With 12 pytest workers and `--receptor=llm`, 39 OpenMM-dependent
focused cases, 475 form/validation cases, 865 `tests/basic` cases excluding
PDB-ID names, and 99 `tests/scientific_truth` cases excluding the `heavy`
marker passed. The groups overlap. This supports source compatibility on
Linux; it neither completes the full suite nor establishes a resolver-clean
Conda release pair.

The environment is not yet metadata-consistent: `pip check` reports the known
development-version mismatch (Viewer requires `molsysmt>=0.22.0`) and
requirements embedded in AmberTools' bundled Python packages. Specifically,
`ndfes`, `fetkutils`, and `edgembar` 3.6.5 require NumPy `<2`; `proprep`
1.0.0 requires NumPy `<2`, Biopython `<1.86`, and `pdb2pqr`, while
`packmol-memgen` also requires absent `pdb2pqr`. The Conda AmberTools 26.0
record itself allows NumPy `<3` and owns those bundled `egg-info` files,
so the Conda solve alone does not detect their narrower Python metadata.
The actual `tleap` executable accepted a minimal `quit` script and exited
with zero errors and warnings. Before the default-engine change below, the
installed MolSysMT wheel called `build_peptide("GG")` through its then-default
LEaP engine, using this exact environment's `tleap` executable, and returned
14 atoms in two groups. This validates that user path for a small peptide on
Linux/Python 3.14, not every AmberTools subprogram or a clean `pip check`.

AmberTools is **not a hard MolSysMT runtime dependency**: the package's Python
and Conda runtime requirements do not contain it. It is an optional external
tool used by the `tLeap` path and is included in development/test environment
specifications. On 2026-09-24, the public `build_peptide()` default was changed
to `engine="MolSysMT"` after focused native/LEaP parity tests. The native path
built `"GG"` successfully with `TLEAP_BIN` pointing to a nonexistent
executable. A separate native one-to-three-letter converter then removed the
Biopython requirement for that one-letter input; the lean 3.14 environment
passed its conversion/default-builder tests with Biopython absent. Users
can still select `engine="LEaP"` explicitly; without the executable that path
raises an actionable `RuntimeError`. The engines have separate coordinate
implementations, so the default change does not assert universal scientific
equivalence. Do not claim that LEaP is broken on Python 3.14.
The new converter has one MolSysMT-owned code table under
`molsysmt/element/group/amino_acid/codes.py`; FASTA/PIR attribute getters and
the FASTA topology adapter reuse it. The amino-acid database continues to
hold topology templates, not this code table. Seven focused conversion cases
passed with Biopython present, and the lean environment passed the native
cases while skipping only the three Biopython-comparison cases. The
dependency-rich environment also passed 38 targeted amino-acid-code,
sequence/FASTA/PIR cases,
371 `tests/build/` cases after excluding four directories with PDB-ID
downloads, and 40 opt-in LEaP-parity cases (all at 12 workers). The broader
`tests/build/` run reached 375 passes but stopped on ten network-download
failures in those four directories; this is not evidence of a native-builder
regression. The `build_peptide` docstring passed `python -m doctest`, five
representative course sequences built with the new default, the focused User
Guide notebook executed, and its two static MolSysViewer assets were
regenerated. The PDB-ID-dependent course notebooks were reviewed for API
wording but could not be re-executed in the offline sandbox.
On 2026-09-24, [conda-forge AmberTools
files](https://anaconda.org/conda-forge/ambertools/files) showed 26.0 builds
for Python 3.14 on Linux and macOS, but not Windows. The
[feedstock recipe](https://github.com/conda-forge/ambertools-feedstock/blob/main/recipe/meta.yaml)
documents its Python 3.14 patches and the lack of a Windows build. An
optional AmberTools lane must remain separate from claims about the
MolSysMT core on Windows.

## Developer environment and storage follow-up

`devtools/conda-envs/development_env.yaml` still pins Python 3.13 and asks for
the published MolSysViewer package, whose current release metadata excludes
3.14. Therefore a named `molsyssuite@uibcdf_3.14` environment should not be
created by merely changing that one Python pin: it needs an explicit decision
between an exact source-pair development installation and a future published
3.14 pair. Do not downgrade NumPy or Biopython merely to satisfy metadata of
AmberTools' bundled ancillary tools. Prefer a metadata-consistent default
development environment without AmberTools, with an opt-in LEaP/AmberTools
test lane and a dated compatibility note. If LEaP itself becomes unusable on
3.14, report that specific capability as unavailable without blocking core
MolSysMT support; its present small-peptide smoke passes.
The disposable scientific environment occupies about 3.7 GiB. The home
filesystem has sufficient space, so there is no reason to delete shared Conda
caches merely to make room for this test. `conda clean --tarballs --dry-run`,
`--packages --dry-run`, and `--index-cache --dry-run` reported no candidates
for the active Conda installation. Do not use `--force-pkgs-dirs`: it can break
environments linked to a package cache. Inventory named environments and
cache ownership before any targeted cleanup; no Conda packages or environments
were deleted during this checkpoint.

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

On 2026-09-24, the Viewer branch gained an opt-in installed-package pytest
mode that retains its fixtures while refusing imports outside the active
interpreter's `site-packages`. Both existing MolSysMT integration tests passed
against the earlier exact local Conda pair (`0.22.2`/`0.23.2`) from outside
both checkouts. The negative control, run from the Viewer checkout, exited 4
with a source-contamination error. This closes the **local test-harness**
gap; by itself it did not test the newer MolSysMT source commit as a package.
Hosted run `35988170629` checked out MolSysMT
`8ab42b58520892d54a05222b91c116b9e9114314` and MolSysViewer
`b9a8c4c9c1672d6fca6fe6c5cb71cf41f8b5b845`. Its Ubuntu, macOS, and
Windows jobs each passed the installed-pair integration step and the full
Viewer Python suite. Those packages were built from the pinned sources with
pip, not resolved from immutable Conda staging coordinates. The Viewer
source suite passed locally outside the sandbox with 12 workers:
2,082 passed, 17 skipped. An initial sandboxed attempt had 18 failures from
blocked sockets or Chromium startup; those disappeared without code changes.
These local tags and archives are not release-version decisions, remote
staging artifacts, or a cross-platform support claim.

## First remote Python 3.14 staging slice

On 2026-09-24, new **staging-only** coordinates were selected without moving
or widening the older 0.22.0/0.23.1 pair. MolSysMT source
`6bc7136093be1bcfff86d8600d00d630738ebd90` produced
`linux-64/molsysmt-0.22.3-pyabi3h03bb3b7_0.conda` in run `35990161344`.
The producer passed; an independent channel query found the exact staging URL,
`python >=3.11,<3.15`, and SHA-256
`ff86eeb73bc22440b3e805c0ad41707529a7d744f44959a195b66cde8b94a7d9`.
MolSysViewer source `0152781987219846e5cfd0250b3e160324f9b6c5`
produced `noarch/molsysviewer-0.23.3-py_0.tar.bz2` in run `35990850975`.
Its build and recipe test passed; the channel reports
`python >=3.11,<3.15` and SHA-256
`7b24b77b5bdd3dfa6cb8a7691bc23680056039dc92f05ddb8f43a60edc6993c9`.
These are technical staging candidates, not Git tags, public releases, or
release-version decisions. An exact Linux/Python 3.14 dry-run resolved both
coordinates from `uibcdf/label/staging`. At that initial point, no fresh
installed-pair cell had passed and MolSysMT had not been staged on the other
native platforms.

The hosted installed-pair workflow now offers a separate `python_max=3.14`
selection while retaining 3.13 as the historical default. Its validator
requires each package's Conda record to carry the exact UIBCDF staging
channel, artifact URL and SHA-256. Eighteen focused workflow/validator tests
passed, including non-staging and mismatched-URL rejection; the stricter
validator also passed against a real previously staged Linux/Python 3.13
environment. Run `35967239820` predates this guard and is not retroactively
credited with it. The complete `devtools/tests/` selection passed 177 tests
with 12 workers after aligning the experimental ABI3/Rattler checks with
`<3.15`; repository-wide Ruff checking and formatting passed.

The first hosted four-interpreter Linux validation, run `35991792969`,
installed the exact new pair in every cell but stopped at the new provenance
guard before the functional checks. Micromamba writes `channel` as the
abbreviated `uibcdf/label/staging`, whereas the older local Conda record
used the full channel URL. The guard now accepts both representations only
when the artifact URL, filename and SHA-256 still identify the exact staging
record. A new positive test covers the micromamba form; the public-channel
and mismatched-URL negative tests remain. This is a validator compatibility
fix, not evidence that the four installed-pair cells have passed; a focused
hosted rerun is required.

The corrected targeted Linux x86-64 run `35992241212` then passed all four
Python 3.11–3.14 installed-pair jobs and retained four explicit environment
records. Linux ARM producer run `35992422489` published its exact build-0
artifact (SHA-256
`ad948e50744e96cdc01182d911604733032a09d8dfe9963fcf634ff4ca8c8ffd`);
targeted installed-pair run `35993063086` likewise passed all four Python
jobs with four environment records. Both GitHub conclusions are `success`.
GH Run Receptor marks each targeted run `FAIL` only because its repository
rule expects all five platforms in one run; `uibcdf/gh-run-receptor#54` tracks
that profile limitation. These runs are two complete native-platform slices,
not the five-platform gate. macOS ARM and Windows build-0 artifacts were also
published in producer runs `35992422933` and `35992422896`; their installation
matrices and macOS Intel's build were still pending at that point.

Windows installed-pair run `35993616429` subsequently passed Python
3.11–3.14 in all four jobs and retained four environment records. GitHub's
conclusion is `success`; GH Run Receptor again marks only its all-platform
expectation unmet. That makes 12 installed cells across three native
platforms, without implying macOS or public-channel support.

macOS ARM installed-pair run `35993242687` then passed Python 3.11–3.14
in all four jobs and retained four environment records. Its authoritative
GitHub conclusion is `success`; the targeted-run receptor profile again
reports only that the other four platforms were not included in that run.
The staging candidate now has 16 successful installed cells across four
native platforms. macOS Intel's ABI3 build and its installed matrix remain
unverified; this is not yet the five-platform gate.

macOS Intel producer run `35992423543` subsequently succeeded from the same
pinned MolSysMT source. The staging channel independently reports
`osx-64/molsysmt-0.22.3-pyabi3h3d50071_0.conda` with SHA-256
`61c0b2868ebfda386224c2afba8ef28be35da4f01429fecf1d597053b36b88da`.
Targeted installed-pair run `35995465959` passed Python 3.11–3.14 in all
four jobs and retained four explicit environment records. Thus the exact
staging pair has passed 20/20 installed cells across all five native
platforms, in five platform-targeted runs. Each cell checked package version
and staging URL/hash provenance, MolSysMT's ABI3 path, BCIF and PDB-text
conversion, and Viewer loading/resources. This is a staging installed-pair
gate, not a single combined workflow run, a public-channel installation,
or a full Qt/scientific test-suite claim. GH Run Receptor's current
all-platform profile does not aggregate the five targeted successes
(`uibcdf/gh-run-receptor#54`); GitHub reports each run successful.

## Next gates after the public pair

1. Correct the duplicated promotion verifier so a future successful upload
   cannot finish with a false-red job (`uibcdf/molsyssuite#48`,
   `uibcdf/molsysmt#246`, `uibcdf/molsysviewer#105`). Do not mutate or
   re-upload the six already verified public artifacts to repair a badge.
2. Extend Python 3.14 evidence beyond the 20-cell *core installed-pair*
   smoke: full scientific/source gates, representative optional backends,
   supported Qt-host observations, and the separate MolSysSuite admission
   decision (`uibcdf/molsyssuite#29`). Windows core-package installation
   passed; Windows standalone Qt support is not implied. Standard
   GIL-enabled CPython 3.14 is in scope, not free-threaded 3.14t.
3. Resume the independent 1.0 tracks from
   [the MolSysMT execution ledger](release_1_0_status.md) and
   `uibcdf/molsysviewer#82`: visible-window Qt, complete hosted E2E,
   dogfooding, documentation and a new exact-commit 1.0 gate. Do not
   recertify 1.0 from the 0.22.4/0.23.4 pre-1.0 exception.

## Handoff discipline

This checkpoint is the compact orientation surface. The linked pending
proposal owns MolSysMT's analysis and acceptance criteria; the Viewer and Qt
issues own their component evidence. Update this checkpoint when a gate
changes, with the date, exact commit/artifact or run, platform, and whether
the result came from source, a local package, staging, or a public channel.
Do not turn a local clean installation into a channel claim.
