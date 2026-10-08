# MolSysMT 1.0 Execution Status

**Role:** operational status ledger
**Last updated:** 2026-10-08
**Plan:** [MolSysMT 1.0 Execution Plan](pending_proposals/release_1_0_execution_plan.md)
**Release checklist:** [Release Gate](release_gate.md)

## Purpose

This is the single current answer to:

- what is complete;
- what is in progress;
- what remains pending;
- what is blocked or deliberately deferred;
- what evidence permits the next stage to start.

The execution plan defines scope, order, weights, and exit criteria. Detailed
bug reports and proposals define individual contracts. This ledger records only
current execution state and evidence; it must not duplicate or redefine those
contracts.

## Final-candidate preparation — 2026-10-08

**Frozen producer:** MolSysMT **1.0.0, ABI3 build 0**, source
`6dc80725ea506f977fb5e52dfd701c2227875fa5`, remote branch
`candidate/1.0.0-build0`. The initially selected Viewer **0.24.1, noarch build 0**,
source `66ea54e45ff3b9498e5f6f668c3d519888dca7b4`, is now withdrawn by its
owner as the final candidate. The replacement is **0.24.1, build 1**, source
`ae1fb995d6a38f2df6df206d2af26fbde1531f24`, verified remote branch
`candidate/0.24.1-build1`; its file/hash are independently inspected below and
prerequisite-gate review remains pending. GitHub comparison verifies nine changed files: three workflow defaults,
one existing guard and five developer-guide records. No molecular or runtime
source changes require rebuilding the MolSysMT artifacts. The
[frozen-candidate receipt](../devtools/data/release_1_0_frozen_candidate_20261008.json)
records verified refs, local results and dispatch identities. Main may advance
with receipts while this producer stays fixed.

The [clean scientific certificate](../devtools/data/release_1_0_scientific_6dc80725e_20261008.json)
passes 54/54 cases from 47 nodes with zero omissions. Thirty local route/workflow
guards, the fourteen fast gates and Ruff pass. A fresh local Sphinx HTML build
succeeds with 782 warnings and zero nonexistent toctree references; #144 retains
the general warning debt. This compilation does not execute notebooks or publish
gh-pages. An initial scientific attempt correctly rejected the dirty tree caused
by Sphinx rewriting three generated RST stubs, despite all cases passing. After
the build, those reviewed stubs were restored and the clean certificate above
was obtained. The receipt retains both outcomes; they are overlapping checks.

Conda producer [37757683710](https://github.com/uibcdf/molsysmt/actions/runs/37757683710)
completes successfully on all four native platforms. The
[staging handoff](../devtools/data/release_1_0_staging_handoff_20261008.json)
records all four filenames/builds/URLs/SHA-256 values. Downloaded bytes, registry
hashes and original producer receipts agree. Actual version/build/upload/evidence
steps execute successfully on every platform. ABI3 metadata, canonical
distribution version 1.0.0 and eight source files match the producer, with only
Windows CRLF normalization. All four hashes were delivered to Viewer through
`codex queue`. This is file inspection, not installed-pair qualification.

The initial eight-cell source campaign
[37757713370](https://github.com/uibcdf/molsysmt/actions/runs/37757713370) and
native wheels [37757715875](https://github.com/uibcdf/molsysmt/actions/runs/37757715875)
used the withdrawn Viewer source and terminate cancelled after explicit
cancellation to avoid completing qualification against a superseded counterpart.
Preserve their original outcomes/artifacts; they do not qualify the replacement.
Four original Linux scientific certificate ZIPs emitted before cancellation
are downloaded and digest-verified; no full-suite JUnit artifact was present
in that campaign's inventory. New source qualification
[37759578359](https://github.com/uibcdf/molsysmt/actions/runs/37759578359) and
native wheels [37759580359](https://github.com/uibcdf/molsysmt/actions/runs/37759580359)
are dispatched on the same MolSysMT producer with the replacement Viewer SHA
explicitly supplied. Native qualification completes successfully: thirty jobs
pass and the PR-only job is the expected skip. Native job records confirm Rust
format/lint/tests and all four controlled installed public-smoke steps actually
execute. GH Run Receptor independently confirms the terminal result. The
eight-cell source campaign remains active; all eight original scientific ZIPs
are downloaded and digest-verified against the clean producer, all 47 nodes
and 54 passing cases with zero omissions. Three Linux full-suite cells
(Python 3.11/3.12/3.13) complete successfully; original JUnit ZIP/payload hashes,
all 26 skipped cases and native executed-step records are verified for each.
Each records 13,301 passes and no failures/errors. The remaining five cells
and full-matrix sign-off stay pending. Default peptide-parity deselection is
active; its count awaits native-log inspection because JUnit does not record
deselected nodes. Viewer's independent review verifies the same eight scientific
ZIPs and two of these Linux JUnit ZIPs; this adds confidence, not test counts.
Both sets of package identities are available;
the installed-pair matrix waits for the
owners' prerequisite-gate review and one agreed dispatch. No public tag,
Release or main-label promotion is performed.

The replacement Viewer file is `molsysviewer-0.24.1-py_1.tar.bz2`, SHA-256
`ab2d6c2a7f8c165c7dc626e277724dcddf06b211f34149de685d0839c1bfde94`,
from owner producer `37758700492`. Independent download and registry inspection
confirm 1,518,815 bytes, noarch build 1 and the staging-only label. The
[replacement receipt](../devtools/data/release_1_0_viewer_build1_staging_20261008.json)
retains its metadata. Independent GitHub inspection confirms successful
Viewer Windows `37759393730` and core-browser `37758593628` campaigns on the
exact replacement source. Their consumer-installed scope remains separate.

The Viewer owner subsequently reports **322/322** guards with zero failures/skips:
191 design, Interactions, nine-family, H5MSM, session, paging and residency cases,
plus 131 composite-loading, source-origin, box and Studio cases,
on Linux/Python 3.14.8 using the exact 1.0.0 build-0 / 0.24.1 build-1 files.
Imports originate only in `site-packages` and `pip check` passes. This updates an
existing environment from verified original files; it is **not** a clean
solver-created installation or the sixteen-cell qualification. These are
owner-reported results, not independently rerun by MolSysMT. The earlier
191-test selection is included in 322 and must not be counted again.

Viewer canonical staging CI
[37760422583](https://github.com/uibcdf/molsysviewer/actions/runs/37760422583)
identifies the replacement source and selected versions. Its required scientific
jobs remain in progress; five of six succeed at the latest inspection, with
macOS/Python 3.12 active.
The Qt job fails in its experimental scope under uibcdf/molsysviewer#109;
do not report that campaign globally green or use it to clear unfinished
scientific jobs. Agree the unique installed-pair dispatch only after these
required outcomes and MolSysMT's source/native gates have been reviewed.

The Viewer owner initially delivers `molsysviewer-0.24.1-py_0.tar.bz2` from producer
`37757179478`, SHA-256
`88ad5b7497bdfa06f16a7e9a47996edd633dd5f63534d38e0b9a0a418478ee58`.
Independent download and registry inspection confirm that hash, 1,515,134 bytes,
noarch build 0, Python 3.11–3.14 metadata and the staging-only label. The
[file receipt](../devtools/data/release_1_0_viewer_staging_20261008.json)
does not claim installed or consumer qualification. The owner later reports
2,880 local passes, 23 skips and one workflow-default failure: the source-pair
workflow still defaulted to 0.24.0 while its release plan selected 0.24.1.
This is an owner-reported preparation failure, not a demonstrated molecular
regression. Viewer preserves build 0 and its branch and prepares build 1 with
corrected defaults. Do not replace or publish those original bytes. Agree one
installed-pair dispatch after the replacement's prerequisite gates are reviewed.

The initial preparation under `uibcdf/molsysmt#334` updates release metadata
and the staged route for **MolSysMT 1.0.0, build 0**, based on main
`b9954fa5e4ba1af5956613308211b90a37880e5c`, delivered at `0a7cfdd8a`. That
checkpoint precedes the frozen producer above and does not identify an
available package or a published release. The
[preparation receipt](../devtools/data/release_1_0_candidate_preparation_20261008.json)
records its checks and remaining exact-candidate gates. The older qualification
below retains its original identities and does not qualify these new files.

Authorized coordination with the existing MolSysViewer team initially fixes its
candidate as **0.24.1, noarch build 0**, source
`66ea54e45ff3b9498e5f6f668c3d519888dca7b4`, with immutable branch
`candidate/0.24.1-build0`. Native GitHub inspection verifies that branch against
the delivered full SHA. This replaces its earlier source-only checkpoint
`0067a2c27c152a068655b8824f0d1c249a32d6b8` and includes the already closed
uibcdf/molsysviewer#149 and uibcdf/molsysviewer#177. The owner confirms the
experimental compatibility contract and delivers the independently inspected
staged file recorded above. The public 0.24.0 build-1 baseline remains
historical evidence. No installed-pair matrix is dispatched before both new
artifact identities are available and inspected.

The frozen MolSysMT source retains that initial audited routine Viewer pin and
source-gate fallback. Manual full/native qualification must supply the accepted
replacement SHA explicitly; review its diff before reusing any evidence or
changing the producer. MolSysMT freezes `candidate/1.0.0-build0` at the committed
source selecting these routes, preserves that producer as later receipts are
recorded, and builds the staged files under the existing construction/upload
authorization. Source/native execution and staged-file delivery remain separate
from the later installed-pair claim. The preparation checkpoint `0a7cfdd8a`
passes all six applicable hosted checks, including smoke; those checks used the
previous Viewer baseline and do not qualify this new source pair.

MolSysMT confirms continuity of the implemented Interactions consumption
contract: sparse roles and compound participants, analysis-version occurrence
indices, evaluated-empty coverage, explicit selections, bounded pages, units,
producer provenance, periodic images, named analyses and H5MSM 0.5 maps/remapping.
Standalone import association remains an explicit declaration. The
[API contract](interactions_api.md), [query semantics](interactions_query_semantics.md)
and symbol stability registry retain their current authority. `Interactions`,
`InteractionsDict`, detector families and the page boundary remain experimental;
1.0 metadata does not promote their stability. Page bounds apply to occurrence
and participant copies after query construction, not to universal memory usage.
Public setters invalidate coverage; raw-array edits require explicit invalidation.
No new functional provider blocker or detector requirement was reported.

The installed-pair workflow requires the operator to supply Viewer version and
build explicitly rather than silently selecting obsolete default coordinates.
Initial preparation checks pass: 17 release-tool/workflow tests with twelve
workers and pytest-receptor, 14/14 fast gates, full-package and changed-test
Ruff, changed-test formatting and citation consistency for 1.0.0. These checks
exercise the prepared working tree, not a frozen release artifact.
#250/#254 remain open for their final-candidate
obligations. #334 still requires exact source/native/scientific, documentation
and installed-consumer qualification followed by the separate publication
approval. No public 1.0 tag, Release or main-label promotion is authorized by
this preparation.

## Qualified pre-1.0 checkpoint — 2026-10-07

**Stabilization follow-up — 2026-10-08:** main commit
`eab7aeb79cc397f92a08081766f5c25792503ae8` publishes the #349 repair and
the archived #251/#252 resolutions; all three owning issues are verified closed.
The separate [scientific certificate](../devtools/data/pre_1_0_scientific_eab7aeb79_20261007.json)
passes 54/54 cases from 47 registered nodes with zero skips/errors/failures
on that clean source. Remote smoke `37734610812`, Ruff, dependency contract,
devguide, suite policy and Conda governance pass on the same source.

The completed [full matrix](https://github.com/uibcdf/molsysmt/actions/runs/37734711393)
and [native wheels](https://github.com/uibcdf/molsysmt/actions/runs/37734713996)
retain that exact source and the published Viewer SHA. The native campaign
concludes success: thirty jobs pass and the PR-only runtime job is the expected
skip. Rust controls, four platform builds, sixteen runtime cells, four NumPy
floor checks, four installed public smokes and the source round trip execute.
GH Run Receptor independently confirms that terminal conclusion. This is native
qualification of the recorded development source, not public-package delivery.
The full source matrix concludes success on all eight Linux/macOS arm64 ×
Python 3.11–3.14 combinations. GH Run Receptor independently confirms the
terminal result. Nine jobs succeed, including the controlled Viewer build;
the PR-only aggregate job is the expected skip for manual dispatch.

All eight original scientific certificate ZIPs have been downloaded and
checked against GitHub SHA-256
digests: each identifies this clean source, matches all 47 registered nodes and
passes 54 cases with zero skips/errors/failures. All eight full-suite cells
also have verified original JUnit artifacts and native job logs:

| Platform / Python versions | Passed per cell | Skipped per cell | Deselected per cell | Failures/errors |
| --- | ---: | ---: | ---: | ---: |
| Linux, Python 3.11–3.14 (four cells) | 13,301 | 26 | 40 | 0 |
| macOS arm64, Python 3.11–3.14 (four cells) | 13,300 | 27 | 40 | 0 |

The JUnit receipt retains every skipped node and reason: absent optional
Ackredit, Vina, CuPy, unyt and astropy, the installed-RDKit negative path and,
on macOS, one Linux-only test. The default peptide-parity exclusion accounts
for the forty deselected cases; these are recorded separately from JUnit.
Every cell's native job record confirms executed fast gates, scientific
evidence, Ruff, the full suite and JUnit retention. Original ZIPs and logs
remain in the task-owned `/tmp` directory recorded by the bounded receipt.
The documentation-only heads `b777029e2` and `4d6ace0d6` pass their applicable
smoke, devguide, suite-policy and Conda-governance checks. Runtime sources,
tests, workflows and packaging are unchanged from the qualified `eab7aeb79`.
These receipts qualify that development source, not a different final 1.0
commit or newly installed release artifacts.

No new package or release tag is published by this reconciliation. The central
receiving owner has accepted #237/#244 under uibcdf/molsyssuite#51 at
`3116b7d9f1fa9ba4d09b81a8f24a22b749805f9f`, frozen by `policy-v1.5.9`.
MolSysMT is `admitted` for the immutable public 0.23.0 / Viewer 0.24.0 pair;
its applicable support-library/developer-tool reviews are `adopted`. The
caller/badge and canonical guide are delivered at
`a04ec0fa3a947a7c959b7f56b09301bb37eceb90`. Both owning issues are closed and
their reports are archived with addressable guards. Exact native conformance
`37742928564` and devguide `37742932367` execute successfully on that delivery;
GH Run Receptor independently confirms their terminal conclusions, and native
steps confirm conformance, Ruff lint and formatting actually ran. The central
delivery receipt is retained under uibcdf/molsyssuite#51.
Final 1.0 candidate gates under #250/#254/#334 remain mandatory and are not
waived by either this closure or the earlier public pair.
The latest 2026-10-08 read-only board review now finds only three open 1.0
issues: #250, #254 and #334. #139/#144 retain their accepted post-1.0 debt boundaries;
they are not evidence that every declared form route or documentation warning
has been corrected.

**Issue reconciliation:** #349 is reproduced and repaired after the published
checkpoint. Its public PDB name/topology guard passes with Pandas 2.3.3 and
3.0.6; the [bounded receipt](../devtools/data/pre_1_0_issue_reconciliation_20261007.json)
retains the initial failures and compatibility outcomes. The original 0.23.0
files remain unchanged and do not contain this later repair.

The subsequent complete shared-environment Linux/Python 3.14 source suite passes
13,327 cases with two skips, no failures/errors and 1,766 warnings in 407.20 s,
using twelve workers and pytest-receptor. The two skips are absent CuPy and
the installed-RDKit negative-path branch; their nodes/reasons and JUnit digest
are retained in the bounded receipt. A separate acceptance selection passes
129 cases; counts overlap the full suite and must not be added. All 14 fast
gates, full-package Ruff, changed-file formatting and developer-guide/index
checks pass. This is editable working-source evidence with the existing native
extension and recorded sibling versions, not a new exact-installed release
campaign. The shared environment has unrelated AmberTools auxiliary dependency
conflicts; no clean `pip check` claim is made for that environment.

Explicit published consumer acceptance now exists under the closed
uibcdf/molsysviewer#114. #251/#252's delivered design/implementation reviews
are resolved with their normative contracts and guards. #250/#254 retain their
explicit exact-1.0 obligations. The central receiving decision above reconciles
#237/#244 with the independently verified public-pair evidence. Native
source/public execution and exact files retain their original identities;
administrative admission is separate from fresh 1.0 candidate qualification.

Current development routes now select the published Viewer producer
`1a4c97a58b68b69f3a836546c9e4ac6187c3efa2`. Original release/source/file receipts
retain their historical pins. #334 still owns final 1.0 candidate selection,
qualification and publication approval; no 1.0 candidate is selected here.

The selected pair is **MolSysMT 0.23.0 / MolSysViewer 0.24.0**, under the
feature freeze in `uibcdf/molsysmt#334`. The coordinated pre-1.0 publication
checkpoint is complete; the separate 1.0 stabilization review remains open.
This checkpoint prepares the next pre-1.0 release; it does not select 1.0.0.

MolSysMT's four native ABI3 **build-0** files are available in
**`uibcdf/label/staging`**, from source
`46ef28eb60a258aa77d82ff1bc39ee0d1591e3c9` and producer run
[37534744593](https://github.com/uibcdf/molsysmt/actions/runs/37534744593).
The [staging handoff receipt](../devtools/data/stabilization_023_staging_handoff_20261006.json)
owns filenames, build strings, SHA-256 values, source comparisons and validation
limits. MolSysViewer can declare **`molsysmt>=0.23.0`** for the coordinated
Interactions, H5MSM 0.5, loading and box capabilities. Experimental interaction
contracts retain their current classification.

For GitHub manual dispatch, the temporary remote branch
`candidate/0.23.0-build0` points exactly to that producer SHA. Use it as the
`ref` for `validate_conda_staging.yaml`; GitHub's dispatch endpoint requires a
branch or tag rather than the raw commit SHA. Keep this branch fixed until
installed-pair qualification and evidence verification are complete, then
remove it during candidate-reference cleanup. It is not a release tag.

Executed evidence includes 14/14 fast gates, 54 scientific cases with no skips,
26 basic doctests, 35 tests importing the actual staged Linux payload and the
successful native-wheel campaign (30 jobs plus one expected PR-only skip).
The local full suite retains its original failed restricted-network invocation
and the successful recovery of all 33 affected cases; it is not recorded as a
second complete green invocation. Details and limitations remain in the dated
checkpoints and handoff receipt below.

Source run [37534217132](https://github.com/uibcdf/molsysmt/actions/runs/37534217132)
has completed successfully in all eight cells, using the earlier controlled
Viewer source `5bb59c0e13045ee0aaf34cf336a3533d611197bf`. The definitive Viewer
candidate is now **0.24.0, build 1**, from
`1a4c97a58b68b69f3a836546c9e4ac6187c3efa2`:
`molsysviewer-0.24.0-py_1.tar.bz2`, SHA-256
`e31dfb114ab2e49f22b372992d0201455b91849f2631d0165b802069e13abeaa`.
Installed-pair run
[37541876875](https://github.com/uibcdf/molsysmt/actions/runs/37541876875)
passes **16/16 cells** on MolSysMT's original candidate. Receiving inspection
verified every required install, runtime, environment-record and retention step;
the Viewer receipt agrees with all four MolSysMT artifact digests.

Viewer's exact canonical source run
[37542642197](https://github.com/uibcdf/molsysviewer/actions/runs/37542642197)
and Windows launcher run
[37542333568](https://github.com/uibcdf/molsysviewer/actions/runs/37542333568)
are successful. The Viewer owner records 39 core browser suites and 25 notebooks
in its receiving receipt at documentation commit `3465e563`, under
`uibcdf/molsysviewer#93` and `uibcdf/molsysviewer#114`.

MolSysMT source run
[37577738386](https://github.com/uibcdf/molsysmt/actions/runs/37577738386)
has completed successfully from the fixed candidate branch with the **final
Viewer SHA**: **8/8 cells** pass. All eight downloaded scientific certificates
identify the original clean MolSysMT candidate and pass **54/54 cases** across
47 registered nodes, with zero scientific failures, errors or skips. The eight
JUnit reports each contain 13,323 cases and zero failures/errors: Linux has
13,297 passes and 26 skips per cell; macOS has 13,296 passes and 27 skips.
Recorded omissions cover optional Ackredit, Vina, CuPy, unyt and Astropy, the
installed-RDKit negative-path case, and a Linux-only test on macOS. This is the
workflow's declared test/doctest scope, not a claim that every optional backend
was exercised there. The additive `coordinated_publication_review` in the handoff
receipt retains every certificate/JUnit digest and the original observations.
The maintainer has authorized MolSysMT publication; its public package records
are now verified. Paired public installation and archival remain pending.

With the maintainer's final authorization on 2026-10-07, tag **0.23.0** and
[GitHub Release 0.23.0](https://github.com/uibcdf/molsysmt/releases/tag/0.23.0)
are published on the qualified source. The four original ABI3 build-0 files are
promoted to **`uibcdf/main`** without rebuilding. Downloaded promotion and
independent public-verification receipts agree with all original SHA-256 values
and verify each file's `main` label and solver-visible index. Successful runs:
linux-64 `37583470115`, linux-aarch64 `37583473201`, osx-arm64 `37583476153`,
win-64 `37583479224`. Their evidence and digests are retained in the receipt's
`publication_checkpoint`. MolSysViewer has received the public-provider handoff
through its existing session. Its build-1 publication is now complete, as
recorded in the coordinated checkpoint below.

The first Zenodo receipt, run `37583386427`, retains **`ingestion_pending`**.
Read-only reprobe `37583715416` now reports **`verified`** for the exact version,
repository and concept family, with version DOI **10.5281/zenodo.23205366**.
The archived source file is `uibcdf/molsysmt-0.23.0.zip` (153,784,473 bytes,
`md5:9e2aa4844c6b8ef030b92dcca6bc7bd3`). The receipt preserves both probes;
the public project-level concept DOI remains 10.5281/zenodo.1298752.
The paired 16-cell **public** installation matrix is now complete and verified,
as recorded below; both source-version archival records are also verified.

Hosted documentation run `37583385927` completes successfully on the release
source; this does not erase the previously recorded warning debt. Release Conda
route run `37583386011` now completes successfully in all four native jobs.
Its staged route skips rebuild/upload; the four separate promotion runs already
verified the original public files.

MolSysViewer [0.24.0](https://github.com/uibcdf/molsysviewer/releases/tag/0.24.0)
is public. Receiving checks resolve its tag to the original candidate
`1a4c97a58b68b69f3a836546c9e4ac6187c3efa2` and confirm successful promotion run
`37587274965`. The Viewer owner verifies the original build-1 digest,
`main` label, solver index and npm/CDN recovery run `37586395370`; publisher-only
recovery is owned by `uibcdf/molsysviewer#176`. Downloaded Zenodo receipt
`37587205154` reports **`verified`**, version DOI **10.5281/zenodo.23206053**,
source ZIP 24,560,894 bytes and `md5:7335fc5b63254d841ea0184aadfdce3f`.

Public installed-pair run
[37587631519](https://github.com/uibcdf/molsysmt/actions/runs/37587631519)
is dispatched **once** from `candidate/0.23.0-build0` on the exact MolSysMT
source, with MT 0.23.0/build 0, Viewer 0.24.0/build 1, Python 3.11–3.14,
all four platforms and `package_source=public`. It completes successfully in
**16/16 cells**, with all four required install/runtime/environment/retention
steps approved per cell. The provider downloaded all sixteen original ZIPs,
verified their GitHub SHA-256 digests and checked exact public URLs, build
filenames, Python minors and MD5/SHA-256 against original package bytes and
registry records. The receipt retains every ZIP/environment digest and the
installed identities. The Viewer owner independently verifies the same sixteen
environments and publishes its final receipt at
`fd8f499e5216df432fd5f52c67647983a935ce27`, under
`uibcdf/molsysviewer#93` and `uibcdf/molsysviewer#114`.

The additional native read-only verification run `37591619395` is queued at
this checkpoint. It will check the completed matrix without rerunning its
installations; retain its receipt after execution.
This closes the coordinated **0.23.0/0.24.0 pre-1.0 publication** checkpoint.
It does not declare 1.0, settle every experimental profile or close owning
acceptance issues without their required guard/normative reconciliation.

Use [Resume from here](#resume-from-here) for the remaining sequence. Earlier
dated observations preserve history; their pending statements do not supersede
this checkpoint.

## Scope freeze and next work — 2026-10-05

The maintainer has frozen feature scope at `d609187ae` under
`uibcdf/molsysmt#334`. The [normative scope decision](release_1_0_scope.md)
now owns admission, the finite S1–S6 stabilization queue and the preserved
post-1.0 issue inventory. Start there before taking another implementation
task. This is a scope decision, not release certification.

S1's fresh triage of #25/#30/#112 is complete in the checkpoint below. S2's
acceptance reconciliation and public validation completion are recorded below.
S3's current preparation profiles are qualified in the checkpoint below.
S4 public-claim reconciliation and S5 workflow/dependency progress are recorded
below. Obtain updated MolSysViewer feedback and complete the remaining executed
Python/provider evidence before freezing exact candidates. No additional chemistry or method
expansion is admitted implicitly. Viewer owns canvas/browser/Qt and session
presentation; its integration feedback is required, while other client
integrations remain outside the initial release gate.

The bounded native PDB policy/application is implemented through `7b51c240f`,
with its generated API view corrected in `d609187ae`. The #304 record retains
532 focused tests, the final boundary check, original-input comparisons,
storage/time observations and their limits. Broader H/terminal/group/disulfide
inference and performance qualification now remain post-1.0 in #304.
Current code may ship experimentally without implying complete receptor preparation.

Deferred individual observation editing, streaming/resumable H5MSM, specific
metal-coordination rules and longer water paths have separate owners
#335/#336/#337/#338. Compatible structure replacement, compaction, bounded
resident export and existing one/two-water methods are already implemented.

The historical 99% weighted campaign below is not a measure of current
stabilization effort. S1–S6 are not certified complete by this documentation
checkpoint; no new heavy suite, installed-candidate matrix or release artifact
is produced. Existing Python/policy obligations and exact-candidate gates remain.

## S1 stabilization checkpoint — 2026-10-05

- #30: GRO-to-MDTraj now reuses the existing native connectivity policy while
  retaining MDTraj's multi-structure coordinate/time/box reader. The original
  NGLView GRO is byte-identical to the bundled fixture. Its former 152 components
  become one under the native candidate rules. The
  [resolution record](archive/resolved_bugs/gro_mdtraj_connectivity_bypasses_native_inference.md)
  distinguishes route consistency from chemical validation.
- #112: no-site native PDB input already yields `None`; a new public PDB/MolSys/
  H5MSM guard protects it. Present sparse attributes keep empty maps and the
  requested structure axis. See the
  [absence record](archive/resolved_bugs/empty_alternate_locations_preserve_absence.md).
- #25: existing local names and source metadata remain supported. Verified
  database identity is a separate enrichment capability; the
  [remaining proposal](pending_proposals/local_molecule_names_and_external_enrichment.md)
  stays open in `Post-1.0`. Deferral is not a claim that enrichment is implemented.

The affected Python 3.14 suite passes 819 tests, including three converter
doctests, in 358.97 s. Ruff, dependency loading/routes, the 263-symbol API
registry, devguide, archive restoration, scientific-registry structure and the
maintained 156-module course validator pass. Notebook executable cells and
saved outputs were unchanged. This is scoped development evidence, not a
full release matrix or an installed-candidate check.

Sphinx HTML compilation passes in the existing Python 3.13 documentation
environment with 40 recorded warnings. The routine 3.14 environment lacks
documentation extensions; #237/S5 retains that qualification work. The legacy
`docs/content/course/devtools/validate_course.py` still diagnoses obsolete
section names; the normative route is `devtools/scripts/validate_course.py`.
It does not replace the maintained course gate or certify missing legacy headings.

On previous head `0efb14144`, remote runs 37366063932 and 37366064781 ended
with failure after GitHub could not acquire a hosted runner. Their jobs have
no runner and no executed steps; Conda governance passed. This is missing
remote evidence under #334, not a code-test failure or a gate waiver. Inspect
the applicable runs after the unskipped S1 checkpoint and recover any still
unexecuted controls before exact-candidate qualification.

S2's newer evidence follows. Keep S3–S6 within the frozen scope.

## S2 provider/consumer checkpoint — 2026-10-05

At clean provider `4d048a78d466728c2fa9a12befacc22182b71d23`, the Python 3.14
result/native/public-H5MSM selection passed 279 tests in 37.14 s. A separate
namespace/detector/codec/doctest selection passed 77 tests and failed one
sandbox network download; the exact failed 5XJH node then passed with network
access in 3.94 s. The
[dated artifact](../devtools/data/interactions_review_packet_20261005.json)
retains both outcomes, selected hashes, runtime versions and fixture hashes.

Local Viewer `eb14716f982be87f66ef8dea5218262bbabdad1d` completed four real
workloads and all nine-family/two-water-order scenarios. Ten initial/restored
structure projections match; five lifecycle analyses retain producer versions,
execution records and exported scene state through a session. Its three local
sandbox design files and Ackredit's nine edits were preserved. These checks
qualify Python data/protocol compatibility, not browser/Qt geometry, a clean
installed pair, large-system performance or the S6 matrix.

The [updated review packet](interactions_molsysviewer_review.md#s2-stabilization-review--2026-10-05)
maps #250/#251/#252/#254 acceptance to existing guards and prepares a message
for the maintainer to forward. No external message was sent. Explicit current
Viewer feedback, agreed combined-memory measurements and final candidate gates
remain open. These reports stay partial. Original class constructor/query/remap
methods needed review at this baseline; the subsequent checkpoint below clears
#252 criterion 2 with tested ArgDigest behavior, without granting an exception.

Stale active-proposal claims about missing remapping, H5MSM embedding and native
ownership are corrected. Historical experimental measurements are preserved;
#335/#336 continue to own the deferred editors and streaming/resumable writes.
No runtime API, scientific criterion, dependency or format was changed.

Remote governance, policy and devguide runs at this provider head succeeded;
Ruff 37369027830 and CI smoke 37369027887 later ended with run failure and
cancelled jobs 111961192306/111961193123. Both have no runner and no executed
steps; GitHub annotations report that no hosted runner acquired the job after
multiple attempts. This is infrastructure evidence, not failed lint/scientific
assertions. Missing execution remains #334 evidence to recover on the next
unskipped head before qualification, not a waiver. Next finish the bounded public class
validation review (now completed below); progress S3–S5 while obtaining Viewer feedback.

## S2 public validation completion — 2026-10-05

Provider `0959a0f7cf3ecf6352d0ed714afacf441563c8b6` completes ArgDigest for
construction, inspection, original/invalidated/recalculated queries, remapping
and standalone persistence. Integer counts and indices refuse booleans and
fractions before encoding; periodic vectors refuse overflow; typed evidence
decoding cannot truncate fractional codes. Record generators are preserved.
Original positional arguments/defaults remain; skip options are keyword-only
and reserved for already validated inputs. Stored cross-column/file invariants
remain active. No method, dependency or file-format extension was introduced.

The corrected broad selection passes 1,520 tests in 211.99 s. The final
source-block delegation guard passes 116 tests in 5.43 s; selections overlap.
The [dated artifact](../devtools/data/interactions_argument_validation_20261005.json)
retains initial failures, source phases, dependency versions and hashes. The
[owning report](archive/resolved_proposals/implement_experimental_sparse_interactions_results_and_queries.md#s2-acceptance-reconciliation--2026-10-05)
records the remaining criteria. #252 is partial; criterion 2 now has a guard.

Ruff, formatting, dependencies, signature/API registries, docstrings, course and
devguide checks pass. Foundations, Toolbox, Cookbook and Module 04 are updated;
course executable cells and saved outputs remain unchanged. Sphinx HTML passes
with 27 warnings in the existing Python 3.13 documentation environment; #237/S5
still owns Python 3.14 documentation-tool qualification. Nine Cookbook and five
initial Toolbox blocks execute; later contextual snippets are not one standalone
script. This is scoped development evidence, not an installed/full release matrix.

At preceding documentation head `dcccc730e`, CI smoke 37371423746 passes.
Policy/devguide/Conda checks ended with no runner or executed steps (jobs
111969243288, 111969240011, 111969242582). The policy annotation confirms hosted
runner acquisition failure. Inspect the next unskipped head and recover missing
execution under #334 before qualification. The maintainer reports Codecov's
service problem resolved; coverage publication still requires evidence from its
next applicable executed gate.

Next: S3's existing preparation/SDF/PDBQT/native profiles; then S4 documentation
claims and S5 environment/dependency policy. Obtain current Viewer feedback in
parallel through the prepared maintainer-forwarded message. No new feature is
admitted and the 1.0 tag remains conditional on S6 exact-candidate gates.

## S3 preparation/form qualification — 2026-10-05

**Contract-tested current frozen profiles**, at provider
`fe0b813d7267f4c5a0728264094441e62c910e1b`: 1,094 preparation/form cases pass
in 380.42 s, without skips. A separate native pipeline, mapped-H reinsertion,
public H5MSM mechanics-exclusion and doctest selection passes 80 cases in
38.82 s, without skips. Runtime, tests and dependency inputs remain unchanged;
this checkpoint corrects explanations rather than extending chemistry.
The [dated artifact](../devtools/data/preparation_profiles_20261005.json)
records commands, source/fixture hashes, actual producer and dependency versions,
warnings and interpretation limits.

| Included contract | Executed evidence | Remaining boundary |
| --- | --- | --- |
| Native SDF graph/charge/isotope/coordination and explicit stereo | `tests/form/file_sdf/`, including the synthetic corpus and original 5X72 stereoisomers | Vina 1IEP valence overrides and versionless 1S63 SDF remain deliberate rejections, not malformed sources. No silent RDKit fallback or complete parser parity claim. |
| Prepared PDBQT file/string/native exchange | `tests/form/file_pdbqt/`, independent MDAnalysis reading and Vina parsing | Source serial IDs align reordered output; BRANCH evidence is partial connectivity. No implicit preparation, H merging or universal torsion policy. |
| Declared template transfer and scoped context | `tests/physchem/test_chemical_template*.py`, readiness/inventory and peptide-template guards | Explicit maps/states, conservative global completeness, retained pose and unknown checks; no template authentication or readiness certificate. |
| Fixed-state H and mapped reinsertion | `tests/build/add_missing_hydrogens/test_fixed_state.py`, `test_preparation_history.py`, and `tests/build/add_terminal_atoms/test_component_hydrogen_reinsertion.py` | Explicit RDKit, one declared state/structure, retained original atom coordinates/indices; generated H geometry is local, without environmental refinement. |
| Named charges, AutoDock types and torsion candidates | Charge/type assignment guards, `tests/topology/test_get_rotatable_bonds.py` and original Vina comparisons | Neutral-amine typing and aryl–nitrile/amide torsion differences remain explicit policy evidence; parameter assignment is not full force-field preparation. |
| Bounded native inference and PDB engine policy | Candidate/application guards and `tests/form/file_pdb/test_connectivity_policy.py` | Declared edges retain precedence; inferred orders stay unknown, coverage partial, history indexed to the operation and changed analyses invalidated. Broader chemistry stays #304. |
| History, units and conservative exclusions | Native/H5MSM history guards, non-default units, native protein/pH pipeline and public mechanics-rejection tests | H5MSM retains original chemical-preparation evidence, while nonempty MolecularMechanics is rejected before file creation; #256/0.6 owns its persistence. |

The normative conversion guide now reflects implemented completion/context and
historical report storage. The PDBQT recipe links implemented assignment/torsion
tools and states the H5MSM rejection; it is registered with its page contract.
The protein/pH pipeline distinguishes its supported templates from fixed-state
ligand H and no longer claims identical provider pKa rules or missing ACE/NME H
support. Common Core 12 already describes these contracts; no executable notebook
cell or saved output changed. The maintained 156-notebook course check passes.

All 96 adapters pass structural checks and the delivery ratchet; the existing
78 unreachable declarations remain #139 debt. Sphinx HTML passes incrementally
in Python 3.13.14 with 26 warnings, without a warning naming the changed PDBQT
recipe. This does not qualify Python 3.14 documentation tools. One NumPy size-change
RuntimeWarning occurred in the broad scientific run and did not recur in fresh
selected-provider imports; S5/#237 retains its origin/installed-ABI review. Other
warnings report legacy H5MSM, pandas/provider deprecations and declared metadata
loss/protonation policies; the artifact records counts rather than hiding them.

Published DockingMT #33 consumer evidence is inspected, including the initial
prepared-input slice and later readiness/charge/H/fragment migrations. It is
historical evidence, not a fresh consumer run on this provider. That integration
does not block this bounded S3 qualification or certify scoring/preparation.
#214/#215/#304 remain partial with their scheduled post-1.0 extensions.
No runtime defect is reproduced within these tested profiles.

S3's bounded local review is complete; S4's newer checkpoint follows. Continue
with S5 dependency/Python policy; keep current Viewer feedback and all S6 source,
installed-artifact, platform and publication requirements open. The preceding
head's policy, Conda governance and devguide runs pass; smoke/Ruff remain queued
at this observation. No full-suite backlog or release gate is waived.

## S4 public presentation checkpoint — 2026-10-05

The README now identifies MolSysMT as a core molecular-system library in
MolSysSuite, qualifies experimental capabilities where claimed, removes its
broken contributor link and replaces stale form counts/full-support wording
with the maintained route contract. Package/Conda metadata, landing and About
pages agree; the existing citation abstract already states this role. No API
stability or form classification was promoted (#186/#192).

The native hero's optional-engine absence guard found #339: native solvation
implicitly delegated water-template reading to OpenMM. The correction reads
without optional inference, uses the existing general native water bond tool
and rebuilds the semantic hierarchy. It qualifies all four existing models
with OpenMM/PDBFixer imports forbidden. No new chemistry is admitted by #334.

For #199, 47 legacy transparent export heads were refreshed using a template
from MolSysViewer's public exporter. All 49 bodies are byte-identical before/
after, retaining scenes, producer versions and runtime references. Six actual
Chromium iframe/screenshot checks of three representative heads match both
host themes. They qualify head/base-canvas behavior, not scientific scene
replay, Viewer interaction geometry or session restoration. The provider's
three sandbox files and four-commit behind state were preserved.

The [dated artifact](../devtools/data/public_presentation_20261005.json)
records 48 passing tests, zero skips, the solvation doctest, commands, runtime
versions and tested hashes. The [header artifact](../devtools/data/static_view_headers_20261005.json)
retains the producer, original/current/body hashes and browser measurements.
Negative controls reject unqualified claims, broken links, unrelated suite
mentions and inert/late/missing header corrections. Expected legacy H5MSM
warnings and TIP4P-EW virtual-site-name warnings remain explicit.

Ruff, dependency loading/contract, citation and the maintained 156-module
course validator pass. Homepage executable cells and stored outputs are
unchanged. Incremental Sphinx compilation passes in Python 3.13.14 with 17
warnings; #144/#237 retain documentation warning/environment qualification.
This is scoped development evidence, not installed/exact-candidate evidence.
At published source `a0d6fc896`, CI smoke, dependency contract, devguide and
Conda governance pass. Ruff 37379969985 and policy 37379970731 execute and
fail because four new tools/tests need formatting; the earlier focused local
lint check did not cover that second requirement. The follow-up formats those
four files, verifies identical Python ASTs and runs both complete Ruff checks.
Scientific runtime code and all scene bodies are unchanged. Inspect the new
unskipped head's controls before treating this remote checkpoint as complete.

Next: S5 dependency/Python review, current Viewer feedback and all S6 gates.
No release tag or GitHub Release has been published by this checkpoint.

## S5 dependency/Python checkpoint — 2026-10-06

- #245: dependency-route coherence and mutation guards pass; the proposal is
  [resolved](archive/resolved_proposals/audit_dependency_contracts_across_packaging_environments_and_ci.md).
  This certifies static contracts, not installed binary compatibility.
- #286: the actual automatic producer at `a8f567c82` has a complete processed
  Codecov report and numeric SVG. The badge is restored with scope in README.
  The [resolution](archive/resolved_proposals/restore_current_coverage_reporting.md)
  preserves its real 11 failures and 26 skips; reporting does not clear test debt.
  No scientific suite was launched solely for coverage.
- #237: routine routes select 3.14; full source qualification now has eight
  Linux/macOS arm64 × 3.11–3.14 cells. Weekly recovery retains all four Linux
  minors and recurring macOS arm64. Wheel runtime matrices include 3.14 with
  an available Python-specific NumPy wheel floor. The debt guard rejects an
  omitted minor and weekly artifacts do not collide. Hosted/installed evidence
  and central admission remain pending; the proposal remains partial.
- #244: current focused unit and argument contracts pass; #236 is already
  resolved and #155's optimization review stays post-1.0. The integrated full
  gate and exact installed closure remain required; no exception is manufactured.

The [scoped artifact](../devtools/data/stabilization_s5_20261006.json) retains
89 passing focused cases, expected legacy-file warnings, policy source, solver
limits, old full-suite failure nodes and Codecov/XML measures separately. All
14 fast gates and applicable Ruff checks pass. Fresh Python 3.14 docs compile
with 784 recorded warnings and no missing course toctree documents; #144 retains
the warning inventory. The docs extra supplies the actual configured extensions.
Homepage executable cells and saved outputs are unchanged.

The initial S5 head `5e4106433` passes remote contract, Ruff, policy, devguide
and Conda governance. Smoke `37422022941` creates the complete Python 3.14
environment but pip rejects the old DepDigest pin's `<3.14` metadata; subsequent
tests are skipped. #237 corrects the manifest to exact published DepDigest
0.13.0 and SMonitor 0.18.0 sources and verifies isolated installation; inspect
its corrected head separately. The original failure remains visible.

Corrected provider head `ce769ffb7dc803fa514e48667e2a3e77b56911f0` executes and
passes Python 3.14 smoke `37423046917`; its package installation, dependency
validation, form/docstring/Rust controls and actual test step all pass. Remote
Ruff `37423046945`, dependency contract `37423046946`, devguide `37423046920`,
policy `37423047391` and Conda governance `37423047467` also pass. The actual
released-provider selection passes 102 scoped cases and all 14 fast gates.
This settles the first routine installation defect, not full-matrix admission.

Fresh triage reproduces four stale catalogue expectations from the old full
producer. #340 adds actual pinned Vina PDBQT file/text detection routes and
explicit SDF/PDBQT supported-table entries; the independent census is retained.
The [resolution](archive/resolved_bugs/catalogue_guards_omit_the_admitted_sdf_and_pdbqt_forms.md)
and [artifact](../devtools/data/catalogue_guards_20261006.json) retain four
initial failures and 45 passing catalogue/real-PDBQT cases without skips.
Fresh triage of the seven remaining old failure nodes with Python 3.14,
pytest-receptor and twelve workers passes the missing-RDKit absence contract and
the converter-table guard. Five caller assertions still assume reconstruction
outside the native profile accepted in #322. #341 corrects the mutation/capping
coverage claims and tests without changing placement algorithms. Its
[resolution](archive/resolved_bugs/mutation_and_terminal_repair_claims_bypass_the_bounded_native_placement_contract.md)
and [receipt](../devtools/data/bounded_repair_callers_20261006.json) preserve the
initial five failures, 87 passing repair cases, two passing public doctests,
exact missing inventories and unchanged observed/source coordinates. All runs
use `--receptor=llm -n 12`. Warnings remain recorded. At `b1fc6b3a5`, actual
Python 3.14 smoke `37425890605` and the applicable remote Ruff, devguide, policy
and Conda-governance controls pass.

The complete local Python 3.14 source suite finishes with exit 1: 13,191 passed,
43 failed, 25 errors and 14 execution skips, in 1,225.59 s with 2,152 warnings.
JUnit additionally retains seven collection skips; these are not seven more
executed tests. DNS-blocked downloads contribute long retries. A network-enabled
retry of the 68 failed/error nodes passes 35 and retains 25 failures/eight errors
in 18.35 s. Missing ParMed, PyTraj and OpenFF explain the optional-provider routes;
MOL2 currently requires ParMed explicitly. This is not a green complete suite.
The [execution receipt](../devtools/data/stabilization_s5_execution_20261006.json)
preserves original outcomes, failed/skipped nodes, log/JUnit identities and scope.

#342 corrects a stale dependency guard that patches a removed private loader
alias; real filtering and missing-library diagnostics now execute with restored
configuration. #343 corrects supported pandas 3 missing-name/membership and
read-only NumPy-export behavior without changing chemical criteria. The same
271-case selection passes without skips on pandas 3.0.6 (17.90 s) and pandas
2.3.3 (18.57 s). The receipt distinguishes initial and intermediate failures;
warnings remain visible. These selections are scoped editable-source evidence.
See the [dependency-guard resolution](archive/resolved_bugs/dependency_architecture_guard_patches_a_removed_depdigest_loader_alias.md)
and [pandas resolution](archive/resolved_bugs/native_topology_operations_fail_under_pandas_3_missing_value_and_copy_semantics.md).

The completed shared development environment now supplies ParmEd 4.3.1,
PyTraj 3.0.0.dev0 through AmberTools 26.0, OpenFF Toolkit 0.19.0, unyt 3.1.0
and Astropy 8.0.1. At clean source `5e2721691`, the 75-selector recovery
passes 109 cases without skips. The complete Python 3.14.7 source suite then
passes 13,313 cases, with two skips, no failures/errors and 1,763 warnings,
in 473.85 s. Both use twelve workers and `--receptor=llm`; their overlapping
counts must not be added. The two skips concern the installed-RDKit SMILES
branch and absent optional CuPy. The separate registered scientific gate passes
all 54 cases from 47 nodes with zero skips and a clean-source certificate.
Its maintained runner deliberately executes serially.

Fresh shared-environment Sphinx compilation exits 0 with no missing course
toctree documents, 781 warning lines and five Docutils error lines. These
existing markup/reference defects remain accepted #144 debt; successful
compilation is not a warning/error-free claim. Notebook execution is disabled,
and generated formatting rewrites were restored.

The [shared-environment receipt](../devtools/data/stabilization_s5_shared_20261006.json)
retains actual versions, commands, hashes, skips, scientific certificate and
documentation errors. The released support providers are pinned, but Viewer
is an editable sibling undergoing concurrent changes; its imported version
and installed metadata differ. These results are development evidence, without
an immutable Viewer-candidate claim. Earlier failed runs remain recorded.
All 14 fast release checks pass after the evidence/documentation update.

S6 preparation then identifies #344: the wheel smoke's manual dependency list
omits required mmcif, and controlled PyUnitWizard 0.28.1 requires ArgDigest
0.14.0 while the old pin supplied 0.13.0. Earlier successful editable execution
does not establish a coherent installed closure. The
[correction report](archive/resolved_bugs/wheel_smoke_accepts_incomplete_runtime_dependencies.md)
and [preflight](../devtools/data/wheel_dependency_preflight_20261006.json)
retain four initial failures, 37 passing corrected guards and actual rejection
of the old closure. The published ArgDigest 0.14.0 pin and installed-metadata
checks address both gaps. At clean `865ff6ec6`, the corrected complete shared
suite passes 13,313 cases with two skips and no failures/errors (404.84 s),
and the separate scientific certificate passes all 54 cases without skips.
All four installed wheel public smokes resolve and validate the real required
closure; the 3.14 smoke installs mmcif 1.2.0 from the wheel metadata.

Wheel run [37438849560](https://github.com/uibcdf/molsysmt/actions/runs/37438849560)
has 29 successful jobs, one failure and one expected pull-request-only skip.
Four builds, sixteen current-NumPy runtime cells, four NumPy-floor cells, four
public smokes and the sdist round trip pass. The global result is **failure**
because Rust formatting rejects one import ordering; Clippy, Rust tests and
cargo-deny have not executed. The local format correction passes Rust 1.97.1,
but its exact-source wheel workflow must execute before qualifying this layer.
The [execution receipt](../devtools/data/wheel_execution_20261006.json) retains
actual artifact bytes/digests and all limits. Published Viewer 0.23.4 is the
fixed smoke baseline, not the final current integration candidate. No package
is published. This is stabilization within the frozen scope.

On corrected source `5bd893c85`, wheel run
[37441629705](https://github.com/uibcdf/molsysmt/actions/runs/37441629705)
concludes **success**: thirty jobs pass and the pull-request-only profile is
the expected skip. Format, Clippy, all 81 Rust native tests and cargo-deny
execute successfully. Four wheel builds, sixteen current-NumPy runtime cells,
four floor cells, four installed public smokes and the sdist round trip pass.
The [corrected receipt](../devtools/data/wheel_corrected_execution_20261006.json)
retains original producer/artifact identities and independently hashed bytes.
#344 is resolved with its dependency-closure regression guard.

Full source run [37441978743](https://github.com/uibcdf/molsysmt/actions/runs/37441978743)
uses the same exact MolSysMT source and Viewer baseline. All eight Linux/macOS
Python 3.11–3.14 cells pass their registered 54-case scientific certificate
without skips; their full suites are still executing at this checkpoint.

S5 is still partial for full-matrix/installed admission evidence. Next obtain
Viewer feedback, agree exact provider/Viewer candidates and execute the required
eight-cell source and installed wheel/Conda pair gates for S6.
No release tag or GitHub Release is published. Configured eight-cell matrices,
solver success, focused editable tests and an accepted badge are not S6 evidence.

## Reported-defect review — 2026-10-02

Legacy H5MSM unit reads now share explicit, validated metadata across queries,
conversion, iteration and migration; conflicting or missing units fail clearly
(uibcdf/molsysmt#240). Group-free native atom metadata returns None without
inventing residues (uibcdf/molsysmt#233). The root argument-validation instruction
uses the real arg_digest boundary (uibcdf/molsysmt#231).

Formal closure also records the already-merged Windows path correction,
explicit rejection of unsupported partial-charge snapshots, verified public
Conda resolution and mmCIF conversion, and the CI trigger/backlog contract
(uibcdf/molsysmt#241, #234, #195, #200, and #185). MolecularMechanics
persistence remains post-1.0 in H5MSM 0.6.

The observed scheduled run 37008569379 at 78981d6c1 executed all three
Linux Python 3.11–3.13 suites but failed three policy tests per cell. It
still installed Viewer source 7a1522662e30575caf580a9447e3e6d80b628e07.
Routine pins and the default full-candidate fallback now use the verified
public 0.23.4 source cf427942d0b08a1c5c60f262c6a6b33f248d6f8b
(uibcdf/molsysmt#293). The corrected public pair passes the policy guard;
this is not yet a new green hosted full matrix. Explicit candidate SHA inputs
remain mandatory for the actual 1.0 qualification decision.

General adapter-delivery debt (uibcdf/molsysmt#139), documentation build debt
(uibcdf/molsysmt#144), and older reports requiring fresh reproduction stay
open; this closure does not certify them or establish release readiness.

## Resume from here

The [frozen scope](release_1_0_scope.md) governs admission. The published pre-1.0
pair is **MolSysMT 0.23.0 / MolSysViewer 0.24.0**; its files and executed evidence
are recorded in the current checkpoint above and the
[staging handoff receipt](../devtools/data/stabilization_023_staging_handoff_20261006.json).
Keep MolSysMT's original package producer and source SHA even when later commits
correct developer tooling or update this ledger.

1. Retain the completed publication evidence with the finite S1–S6 queue
   under `uibcdf/molsysmt#334`, and review the owning native/result acceptance
   issues. The 16/16 public pair, 8/8 final source matrix and verified Zenodo
   receipts are a completed pre-1.0 baseline, not automatic 1.0 sign-off.
2. Current development controlled-source pins now select the published Viewer
   baseline. Preserve historical pins at their original candidate; do not move
   qualified tags or rebuild public files merely to update development routes.
   Source matrix `37734711393` and native campaign `37734713996` are both
   successful on the recorded development source, with original artifact and
   executed-step verification. Neither is a 1.0-artifact claim.
3. Retain the completed central receiving response for #237/#244 under
   uibcdf/molsyssuite#51 and this delivery's administrative conformance. Version
   metadata and the staged route for 1.0.0 build 0 are prepared. Obtain the
   MolSysMT producer and both current staged file identities are recorded above.
   Viewer withdrew build 0 and its corrected build 1 is inspected. Verify the
   restarted exact-source/native campaigns and the Viewer prerequisite gates,
   then agree the single installed-pair dispatch against these exact files.
   #250/#254 retain their final-candidate checks and #334 owns qualification and
   publication approval. Keep feature scope frozen; extensions retain their
   post-1.0 owners. A final-candidate failure returns its affected scope to
   stabilization rather than reopening feature development.
4. Preserve original package/ZIP/environment identities, the read-only matrix
   receipt and both version DOIs. Retire the temporary candidate branch after
   all reference-dependent verification and owner reconciliation are complete;
   the qualified tags remain fixed.

The public 0.22.4/0.23.4 pair and the
[Python 3.14 checkpoint](python_3_14_checkpoint.md) remain historical installation
and development evidence. They do not select the current producer, replace its
qualification or authorize publication.

The [interaction-detection namespace proposal](pending_proposals/organize_interaction_detection_by_family_before_1_0.md)
(`uibcdf/molsysmt#250`) has been accepted for the bounded pre-1.0 migration of
hydrogen-bond methods and disulfide-candidate detection. The bounded namespace,
detector migration and persistence routes are implemented in the staged
candidate. The published pre-1.0 pair now supplies consumer and exact-candidate
qualification evidence; owning acceptance closure and 1.0 stability decisions
still require explicit reconciliation. Separately approved
experimental ionic, pi-pi, cation-pi, halogen, hydrophobic, metal-candidate and
one- and two-water hydrogen-bond families are now implemented; these are not new 1.0
requirements. Metal-specific rules and paths through more than two waters remain
extensions. The public `Interactions` contract (#251),
optional native `MolSys` attachment and H5MSM persistence (#252), and a tested
MolSysViewer integration (`uibcdf/molsysviewer#114`) are now required before
the 1.0 candidate freeze. Native attachment, local-to-source maps, declared
atom search scope, and standalone and grouped HDF5 codecs have focused tests.
Public H5MSM 0.5 round trips for named analyses and supported partial `MolSys`
combinations are contract-tested. Incremental interaction editing and bounded
public file access remain unsupported. The experimental consumer contract is
agreed; the pre-1.0 pair is qualified, while 1.0 stabilization remains open.
The [S2 review packet](interactions_molsysviewer_review.md#s2-stabilization-review--2026-10-05)
records local provider/consumer projection and session parity for all nine
families and both water orders. This supersedes the earlier two-family local
smoke, while actual canvas acceptance and installed-pair qualification remain
separate obligations.
TopoMT, PharmacophoreMT, and DockingMT integrations do not gate 1.0.

The 2026-10-01 naming/attribution checkpoint at clean provider `e21f03d99`
adds scientific/descriptive selectors, exact profiles, compatibility aliases
and detached optional Ackredit bibliography. Whole-library and suite-wide
adoption remain partial under `uibcdf/molsysmt#27`, `uibcdf/ackredit#75` and
`uibcdf/molsyssuite#68`. Real local MolSysViewer qualification passed four
scientific workloads, geometry/query checks and H5MSM/session round trips.
A new optional public-client guard also passed for original bibliography,
producer versions and absence of reader calculation credits (18 focused tests,
none skipped). [The implementation record](archive/resolved_proposals/implement_experimental_sparse_interactions_results_and_queries.md#consumer-and-attribution-checkpoint--2026-10-01)
identifies the clean provider, dirty consumer source and measurement limits.
This advances local interoperability; it is not an installed published-pair
qualification, a new browser/GPU run or the exact-candidate 1.0 release gate.

The 2026-10-01 detector checkpoint adds an experimental cation-pi API with the
attributed ProLIF 2.2.2 core definition as default and a separately named MolSysMT
proposal. Its original-detector parity, declared hydrogen conversion repair,
forms/units/scopes/PBC/persistence, executed documentation and bounded scale
measurements are recorded in
[the completed implementation report](archive/resolved_proposals/implement_cation_pi_observations_with_reusable_charge_and_plane_tools.md)
and [the benchmark guide](benchmarking/cation_pi.md).
The general SMARTS tool belongs to topology. Broader scientific comparison remains
open in uibcdf/molsysmt#271 and does not gate 1.0; no claim of superior physical
accuracy or a passed final release-candidate gate follows from this checkpoint.
The 2026-09-29 integration inspection found that H5MSM 0.4 extraction
materializes and rewrites a full `MolSys`; it cannot preserve attached
interactions and now rejects that export. Native copy, extraction, atom
addition, and structure append have bounded experimental rules. On 2026-09-29 the
scope decision advanced the full H5MSM 0.5 modular layout, with separate
chemical-state and interaction layers, onto the pre-1.0 path; the earlier
0.4.1 extension candidate was withdrawn. An explicit public
`molsysmt.h5msm` API now reads and writes the 0.5 layout and offers a
0.3/0.4-to-0.5 migration helper. Public `molsysmt.convert` now writes 0.5 by
default and reads 0.5 through the native codec; legacy adapter operations remain
for 0.3/0.4. Reading a legacy file emits an actionable warning without dropping
support. This is not release evidence. Candidate freeze awaits
remaining 0.5 form operations, schema coverage,
the required lifecycle gates, and exact-candidate MolSysViewer tests. The runnable
experimental provider handoff has already enabled `view.interactions` development;
current client evidence must still be agreed before the MolSysMT result API is
stabilized. `ChemicalStates` is now a separate
native domain; its wider release validation remains open.
H5MSM 0.5 native routes now round-trip all seven primary combinations
of topology, chemical states, and structures, preserving absent layers through
copy and pickle. Full field fidelity, general append behavior, and large-trajectory gates
remain open. Public `read` now reconstructs a partial native `MolSys` from
named interaction-only payloads, using their declared atom and structure
index domains. A present-empty interaction layer still requires `read_layers`
because it declares neither domain.
Native 0.5 write/read now also round-trips structures plus named interactions
without chemical states, with or without topology, and rejects missing
interaction-axis associations instead of guessing from matching lengths.
The public structures-only read path is guarded for coordinate-bearing and
time-only files: both become partial `MolSys` objects with absent topology and
chemical states, and the time-only case retains an unknown atom count.
The public
0.5 writer now round-trips typed bioassembly transforms, including translations
converted from angstroms to nanometers in the bundled TcTIM BinaryCIF case.
Sparse alternate locations now round-trip through the public 0.5 route on
the bundled PDB example, and structure IDs retain integer or string type.
Sparse alternate-location columns can append when both stored and incoming
blocks declare them. `MolecularMechanics` remains a minimal, experimental
native domain before 1.0. Its persistence is explicitly deferred to H5MSM
0.6 after 1.0 (`uibcdf/molsysmt#256`); H5MSM 0.5 has no mechanics layer and rejects nonempty
mechanics data before writing rather than dropping it.
The public topology-free file path can append complete frame rows and read
nonconsecutive selections,
including files with chemical states and atom-axis links. It can extend one
structure-to-state map when new state indices are supplied. Append involving
topology, interactions, other structure-axis associations, and crash recovery
are still unimplemented.

For the MolSysViewer review of `uibcdf/molsysviewer#114`, the public parity
test `tests/interactions/test_public_molsys_h5msm_workflow.py` and
`devtools/scripts/create_molsysviewer_interactions_fixture.py` now provide
synthetic native and H5MSM 0.5 examples. The fixture generator writes both a
complete `MolSys` file and an interaction-only file that loads as a partial
`MolSys`. The [review packet](archive/resolved_proposals/design_a_sparse_public_interactions_result_and_serialization_contract.md#runnable-molsysviewer-review-packet)
states the implemented query contract and current limitations. MolSysViewer has
accepted the experimental handoff and local qualification has advanced as
recorded above. The original fixture packet alone is not an exact-commit
1.0 release gate.
An expanded local selection covering H5MSM, native forms, interactions,
`MolSys` adapters, conversion, structure append, hydrogen bonds, and
disulfides passed 1,347 tests on 2026-09-29. Ruff, public API stability,
form adapter, dependency, and devguide checks also passed. This dirty-checkout
evidence must be repeated on a review commit before candidate certification.

Use at most 12 pytest workers with `--receptor=llm` for compact local
diagnostics; normal pytest verdicts remain authoritative. Use
[the GH Run Receptor guide](../GH_RUN_RECEPTOR_GUIDE.md) for hosted-run
inspection.

## Status Vocabulary

| Status | Meaning |
| --- | --- |
| `DONE` | The declared exit gate passed with recorded evidence on an identified commit. |
| `IN PROGRESS` | This is the active segment or stage; work has started but its exit gate is not complete. |
| `PENDING` | Accepted work that has not started or cannot start until an earlier dependency closes. |
| `BLOCKED` | Work cannot advance because a named external decision, defect, resource, or prerequisite is unresolved. |
| `DEFERRED` | Explicitly outside the 1.0 critical path unless new correctness evidence promotes it. |

Only one top-level segment should normally be `IN PROGRESS`. If independent
packaging work runs in parallel, record the responsible branch or collaborator
and do not merge it across an unmet integration dependency.

## Pre-1.0 public distribution milestone — 2026-09-25

**Platform policy update (2026-09-27):** Future candidates exclude macOS Intel
(`osx-64`/x86_64). The supported macOS architecture is Apple Silicon (arm64).
The active native Conda matrix is four platforms and, for Python 3.11–3.14,
16 installed-pair cells. Earlier five-platform/20-cell results below remain
valid historical evidence for the published 0.22.4/0.23.4 pair, not future
release requirements. See `uibcdf/molsyssuite#59` and `uibcdf/moli#31`.

MolSysMT 0.22.4 and MolSysViewer 0.23.4 are published GitHub Releases on
their exact tested commits. Their ABI3/noarch Conda artifacts were promoted
as six immutable files; independent public-channel queries verified each
filename and SHA-256. The [public installed-pair matrix](https://github.com/uibcdf/molsysmt/actions/runs/36129993869)
passed 20/20 across five platforms and Python 3.11–3.14, with public
provenance and runtime/BCIF/PDB-text/Viewer-resource checks. The prior
staging matrix passed 20/20 in run `36121427459`. This closes the coordinated
package-availability milestone that had blocked normal Viewer CI.

The promotion action steps and receipt uploads passed, but the final
duplicated post-promotion verifiers falsely ended red after printing each
correct public URL (`uibcdf/molsysmt#246`, `uibcdf/molsysviewer#105`,
`uibcdf/molsyssuite#48`). The public matrix is independent evidence; do not
claim those promotion jobs passed. A replacement read-only verifier passed
on GitHub for the exact public MolSysMT file in
[run 36227235698](https://github.com/uibcdf/molsysmt/actions/runs/36227235698)
and for Viewer in
[run 36227243079](https://github.com/uibcdf/molsysviewer/actions/runs/36227243079).
The original verifier's exit-1 mechanism remains unknown; the old runs remain
red and were not rerun. Both Zenodo version records are now
published and independently verified: MolSysMT 0.22.4 has version DOI
`10.5281/zenodo.22959294`, and Viewer 0.23.4 has version DOI
`10.5281/zenodo.22959304`. They arrived after the initial 900-second
polling window; MolSysMT's verifier also required a tree-tag identifier
absent from the valid record and was corrected under `uibcdf/molsysmt#247`.
This does not imply that Conda/npm artifacts were archived by Zenodo;
the records contain source ZIPs only (`uibcdf/molsyssuite#49`). Viewer
visible-window Qt and complete hosted E2E are explicit
pre-1.0 exceptions, not 1.0 sign-off (`uibcdf/molsysviewer#100`). The
MolSysSuite-wide 3.14 admission decision is separate (`uibcdf/molsyssuite#29`).

## Historical 1.0 certification baseline — not replaced by the 0.22.4 release

The F5/F6 evidence below records the earlier 1.0 workstream and its weighted
closure. Its older commit coordinates are historical 1.0-gate evidence, not
the current `main` head or the 0.22.4 tag. Publication of a pre-1.0 pair does
not close F6. The historical 99% belongs to that campaign's weighted plan;
it does not estimate the remaining scope after later implementation changes.

- **Active segment:** F — lifecycle and release candidate
- **Active stage:** F6 release sign-off and 1.0 tag
- **Historical weighted closure:** 99% of the earlier remaining-plan campaign
- **Historical development evidence:** Segments A and B passed their gates;
  the final exact-commit campaign passed the bounded two-backend oracle,
  independent scientific evidence, and all 9,774 effective application tests
  with Rust forced
- **Historical F5 repository state:** F1–F5 were closed in the earlier
  certification campaign. The recertified F5 candidate
  `38ab61f6e` passed the complete fast, smoke, documentation, wheel, and
  Linux/macOS Python 3.11--3.13 gates after the bounded pre-1.0 corrections.
  That candidate used the published ArgDigest `0.12.0`; a subsequently found
  silent alias collision is fixed upstream and raises the source dependency
  floor to the then-planned `0.12.1` patch release. PyUnitWizard was at
  `0.24.0`. Those coordinates are historical; a new 1.0 candidate must use
  and verify current published dependency floors.
  The remaining Common Core
  exception was removed in `c87a14036`: all 20 modules now use their permanent
  semantic manifest identities and the validator pins the 1–20 contract. The
  PyTraj, OpenFF, OpenMM construction, and missing-converter work that followed
  the 2026-08-07 snapshot is landed through `929d4363e`
- **Historical exact Rust campaign commit:** `6485a0c08`; this is verified
  migration evidence but was not itself a release candidate; Segment F
  lifecycle work was still open at that checkpoint
- **Historical exact Rust packaging commit:** `17be9ea50`; C2 was verified by a
  clean exact-commit `cp311-abi3` wheel and installed-extension smoke
- **Historical C3 exact evidence commit:** `f79ccb4f0`; all five native abi3
  wheels build, audit, install, execute the private-extension smoke, and upload
  successfully in GitHub Actions run `30346103646`
- **Historical C4–C7/E4 exact evidence commit:** `c4d8e9074`; five native wheels,
  15 platform/Python installed checks, three NumPy floors, three public smokes,
  the sdist round trip, and Rust quality/security gates pass in GitHub Actions
  run `30394881487`
- **Historical E3 exact evidence commit:** `692479097`; 9,585 tests passed, two were
  accepted skips, and the fast release gate passes 12/12
- **Historical F5 exact candidate:** `38ab61f6e`; fast gates passed 12/12 locally,
  full matrix run `31781216880` passed on Ubuntu and macOS with Python
  3.11--3.13, wheel run `31781218931` passed the supported Linux/macOS build
  and installed-runtime matrix (with Windows green as experimental evidence
  only), documentation run `31781220979` passed, and smoke run `31781199983`
  passed
- **Current release readiness:** no numerical completion estimate; the
  [frozen scope queue](release_1_0_scope.md) and exact-candidate evidence define
  what still needs closure
- **Normal pytest:** the authority for test results
- **pytest-receptor:** the systematic compact reporter; disagreements must be
  reported upstream immediately
- **Next action:** complete S1–S5 of the frozen scope, using the published
  0.22.4/0.23.4 pair only as an installation baseline, then run every 1.0
  release gate on one new exact candidate before
  any 1.0 tag. Its own GitHub Release and distinct Zenodo version DOI still
  need post-publication verification; the pre-1.0 pair does not close F6
- **Parallel packaging action:** Segment C and installed-wheel validation are
  closed. The separate Conda delivery track has passed staging **and public**
  20-cell, five-platform installed-pair matrices across Python 3.11–3.14.
  Future 1.0 coordinates still need their own exact-candidate gates, but
  public availability of the 0.22.4/0.23.4 pair is no longer pending
- **Parallel documentation and paper action:** with A–E and F1–F5 closed, the
  presentation surface, the documentation and the methods paper are a principal
  parallel workstream rather than a finishing touch. The framing and factual
  corrections landed as `d2b805e74`. Of the three items that required a maintainer
  decision, two are settled on 2026-08-07: Daniel Ibarrola-Sánchez is not an author
  and was removed from `CITATION.cff`, which also removes the ORCID misattributed to
  him, and the unreferenced duplicate landing page is deleted. F6 now selects the
  existing MolSysMT concept DOI, corrects every public citation surface, and separates
  the pre-tag metadata gate from post-release verification of the version DOI. The
  lifecycle is normative in `release_and_citation.md` and executable through the fast
  gate and release workflow. Only the timing of the
  Conda installation instructions remains open, in
  [Presentation and Citation Surface](pending_proposals/presentation_and_citation_surface.md).
  Public-facing code examples must be executed against the installed package
  before they are written: the 2026-07-29 audit found that none of the README's
  examples ran
- **Known independent release-gate debt:** the F6 working candidate passes the
  expanded fast release gate 13/13 on 2026-08-14, including the new citation
  metadata gate. Form-adapter delivery is green with 89/89 forms, 78 accepted
  lower-tier declarations across nine forms, 343 resolved baseline
  declarations, and no Tier-1 debt. Conversion fidelity reports 40 exhaustive
  Tier-1 edges, 441 accepted non-exhaustive edges, 29 resolved baseline edges,
  and zero new debt

The 99% figure measures only the newly defined remaining-plan exit gates. It
does not attempt to restate the much larger body of MolSysMT development,
consolidation, or Rust kernel work completed before this ledger was created.

## Historical F6 blocker assessment — 2026-08-19

The following assessment describes the 2026-08-19 candidate, not the newly
published 0.22.4/0.23.4 pair. Recheck its source pins and workflow triggers
against current `main` before carrying either item into a new 1.0 candidate.

Both are recorded here rather than tracked elsewhere because they block the tag
itself, and a release blocker with no home is how the 2026-08-17 weekly failure went
four weeks unread.

**The pinned MolSysViewer revision is stale, and `ci-full` is red because of it.**
Deferred by maintainer decision on 2026-08-19; local suites are green and the
deferral is not a disagreement about the diagnosis.

`.github/workflows/{ci-full,ci-smoke,ci-weekly,sphinx_docs_to_gh_pages}.yaml` all pin
`molsysviewer@7a1522662e30575caf580a9447e3e6d80b628e07`, dated 2026-08-13 and 26
commits behind that project's `main`. The pinned revision predates `a80270a2`,
"adopt the shared MolSysSuite unit policy", so it declares the old mass standard and
`tests/cross_repo/test_unit_policy_authority.py` fails — 3 tests, identically on
ubuntu and macOS across Python 3.11, 3.12 and 3.13, with 9 980+ passing around them.

Note that the Conda channel is irrelevant here: `devtools/controlled_sources.txt`
installs the suite projects from pinned Git revisions with `--no-deps`, precisely so
the solver cannot substitute them. Publishing a package does not move this pin.

**`ci-full.yaml` runs only on `workflow_dispatch`.** `release_gate.md` requires a
green matrix on the exact committed tag candidate, and nothing produces one
automatically. This was excluded from the scope of `uibcdf/molsysmt#171`, which
covered running the suite on push.

Both must be resolved before F6 can be signed off. Neither affects library
correctness: the fast gate is 13/13 and the full suite passes locally.

## Segment Ledger

| Segment | Weight | Status | Earned | Current evidence or reason |
| --- | ---: | --- | ---: | --- |
| A — conversion-fidelity coherence | 25% | `DONE` | 25% | 40 exhaustive Tier-1 edges, 441 accepted non-exhaustive edges, 29 resolved baseline edges, zero new debt, and all conversion/form gates pass |
| B — final Numba oracle | 10% | `DONE` | 10% | exact commit `6485a0c08` passes the 264-test bounded two-backend oracle, combined scientific and blocker gates, and the complete forced-Rust suite with 9,769 passed and 5 accepted skips; the dated artifact preserves source and binary hashes |
| C — Rust packaging | 20% | `DONE` | 20% | C1–C7 pass: permanent backend, private abi3 integration, five native wheels, Python 3.11–3.13, NumPy floors, sdist/package parity, and Rust quality/security gates |
| D — Rust-only cut | 20% | `DONE` | 20% | the runtime, dependencies, tests, controls, and GPU experiments are Numba-free; compatibility facades route to Rust, the executable zero gate passes, and the affected scientific surface passes 450 tests |
| E — scientific and ecosystem validation | 15% | `DONE` | 15% | E1–E6 pass: Rust/scientific/full-suite gates, installed-wheel matrix, maturity-weighted consumers, and runtime/thread benchmarks |
| F — lifecycle and release candidate | 10% | `IN PROGRESS` | 9% | F1–F5 are done; only F6 sign-off and the verified tag remain |
| **Total** | **100%** | **`IN PROGRESS`** | **99%** | A–E use complete segment gates; F uses the explicit stage weights below |

The detailed A–E notes below preserve the earlier certification campaign.
Their dated uses of "current" and "next" refer to that campaign, not the
present F6 handoff at the top of this file.

### Historical B4 Pause Checkpoint — Transactional Structural Growth

At the time of this pause, the uncommitted vertical defined one
structural-axis contract for
`Structures`, `StructuresDict`, `MolSys`, `append_structures()`, and
`concatenate_structures()`:

- topology-free structural sources remain valid when atom counts match;
- every materialized structural series covers the complete structure axis;
- append validates the source and target before mutation;
- `attribute_policy='intersection'` retains shared series and reports all
  discarded one-sided attributes;
- `attribute_policy='strict'` rejects one-sided attributes without modifying
  the target;
- the public API, User Guide, Common Core course, and native contract describe
  the same behavior.

Evidence before pausing:

- focused native/API gate: 51 passed;
- expanded native-form/H5MSM gate: 1,254 passed;
- warning reconstruction and public structural-growth gate: 20 passed;
- both edited User Guide notebooks parse as valid JSON;
- pytest-receptor agreed with pytest on every verdict and exit code.

That checkpoint subsequently landed. Its then-next work was the remaining
NGL adapter causes and an exact-commit Rust wheel and forced-Rust release
gate; it is not the present instruction to resume or a claim that today's
worktree contains that WIP.

The H5MSM 0.5 independent-layer design discovered during this vertical is
recorded separately in
[H5MSM 0.5 Modular Layer Contract](pending_proposals/h5msm_0_5_modular_layers.md).
It is not part of this implementation checkpoint or the default 1.0 critical
path.

### B4 NGLView Fidelity Checkpoint

The three remaining NGLView causes from the first campaign are closed in this
checkpoint:

- MolSysMT-created single-component widgets retain an isolated private topology
  snapshot instead of losing identifiers and chemical bond metadata through
  PDB;
- external, empty, coordinate-only, and multicomponent widgets do not
  implicitly acquire that snapshot or claim topology they do not contain;
- multi-structure trajectories keep their complete coordinate axis without
  retaining one-structure PDB metadata as a partial series;
- group-level hydrogen-bond rendering preserves the input pair order instead
  of relying on the canonical sorted selection result.

Evidence at landing:

- complete NGLView surface: 45 passed under forced Rust;
- broad conversion/get/compare/view/PDB/Structures surface: 746 passed under
  forced Rust;
- Ruff and `git diff --check`: pass.

The instance-level contract is recorded in
[NGLView Adapter Contract](nglview_adapter_contract.md). With this checkpoint
landed, B4 has no known targeted application root cause remaining and must move
directly to the new exact-commit campaign.

## Segment A — Conversion-Fidelity Coherence

**Canonical bug:**
[Conversion Fidelity WIP Exposes Multiple Contract Gaps](archive/resolved_bugs/conversion_fidelity_wip_contract_gaps.md)

| Stage | Status | Dependency | Closure evidence required |
| --- | --- | --- | --- |
| A1 — audit-scope contract | `DONE` | none | landed as `504df91d0`; scope API, compatibility, tests, and lifecycle docs complete |
| A2 — exhaustive native-dictionary audit | `DONE` | A1 | three evidence-backed native-to-dictionary profiles landed; 51 focused tests and the Tier-1 ratchet pass |
| A3 — independent schema/adapter repairs | `DONE` | A1–A2 stable | direct native projections and all four builder routes have evidence-backed exhaustive reports; the broad native-scope module is green |
| A4 — PDB fidelity | `DONE` | A1–A2 stable | one handler-owned normalized parser feeds file, text, and handler routes; 22 fidelity tests and the historical PDB corpus pass; 11 exhaustive profiles landed as `1f656fe9f` |
| A5 — segment integration gate | `DONE` | A1–A4 | 40/481 edges are exhaustive, 441 are accepted debt, 29 baseline edges are resolved, zero are new; adapter delivery and lifecycle gates pass |

| A2 cohort | Status | Evidence |
| --- | --- | --- |
| A2.1 — `Structures -> StructuresDict` | `DONE` | exhaustive 22-attribute contract partition, current schema-loss reporting, strict rejection, lifecycle documentation, and conservative fidelity ratchet landed as `cb123e226` |
| A2.2 — `Topology -> TopologyDict` | `DONE` | 76-attribute contract partition, 24 value-dependent loss candidates, multi-state collapse, conditional aromatic mapping, strict rejection, and lifecycle documentation landed as `4a4773986` |
| A2.3 — `MolSys -> MolSysDict` | `DONE` | composed 114-attribute contract, seven structural losses, 18 mechanical losses, state association, strict rejection, and lifecycle documentation landed as `01067f2c5` |

### Completed A1 Objective

Implement one authoritative scope contract:

1. add backward-compatible `ConversionIssue.scope`;
2. add `get_conversion_audit_scopes(source, target)`;
3. add `is_conversion_audit_exhaustive(source, target)`;
4. make the helpers authoritative for conservative static graph coverage;
5. let instance-aware reports strengthen the static result only with explicit
   evidence;
6. keep the exhaustive-pair registry empty until A2 implements and tests the
   corresponding schema traversal.

### Current A1 Non-Goals

- exhaustive schema traversal, which belongs to A2;
- independent schema and adapter fixes, which belong to A3;
- PDB identifier and strictness repairs, which belong to A4;
- implementing or repairing the complete conversion graph;
- Rust packaging or Numba deletion.

### Conversion Critical-Path Rule

A conversion blocks Segment A only when it exposes:

- shared audit or conversion infrastructure failure;
- silent corruption or incorrect success;
- atom/structure misalignment;
- an advertised Tier 1 contract violation;
- new, unclassified fidelity debt.

Known, reported non-exhaustive behavior and low-priority Tier 2/3 routes remain
visible in the baseline or backlog and may be addressed later. They must not be
silently reclassified merely to make the gate green.

### A2 Cohort Design

The native-dictionary audit is divided into three reviewable cohorts:

1. **A2.1 — `Structures -> StructuresDict`:** classify every semantic in the
   declared `molsysmt.Structures` form contract as preserved, derived, absent in
   the source instance, or lost by the current dictionary schema.
2. **A2.2 — `Topology -> TopologyDict`:** apply the same contract to stable
   topology and chemical-state semantics, including optional bond and atom
   state fields.
3. **A2.3 — `MolSys -> MolSysDict`:** compose the proven topology and
   structures audits, then add molecular-mechanics and
   structure-to-chemical-state association semantics.

`is_exhaustive` is relative to the declared public semantic contract of the
source form, not every private implementation field and not every attribute
that another form happens to expose. Derived attributes are not reported as
lost when their required information remains representable.

Each cohort requires an explicit conversion-schema manifest. The ordinary form
`attributes` mapping is not sufficient evidence: it describes query
capabilities, while conversion fidelity asks which source semantics the
specific serializer actually preserves. This distinction is already visible
in `TopologyDict`, whose capability declaration mirrors `Topology` although
the current 0.1 serializer stores a narrower payload.

The first cohort is deliberately `Structures -> StructuresDict`: its native
storage contract is bounded, and it can prove the audit machinery before the
multi-state topology model is involved. A2.1 must report current unsupported
thermodynamic and bioassembly payloads honestly; extending the dictionary
schema or converter remains an independent A3 repair.

### A2.2 Topology Profile Design

The `Topology -> TopologyDict` profile covers the 76 attributes declared by
the native topology form. It must classify them in the following groups:

1. **Direct stable inventory:** atom, group, chain, molecule, and entity
   identifiers, names, types, membership, isotope, bond endpoints, formal bond
   order, and bond relationship type written by the 0.1 converter.
2. **Derived without loss:** indices, counts, inner-bond views, bonded-atom
   views, and biomolecule counts whose complete source data remain available.
3. **State-inventory limitations:** multiple chemical states collapse to one
   resolved state; a non-default state identifier, reference-state choice, and
   completeness/evidence metadata require value-aware checks.
4. **Component limitations:** version 0.1 has no component section. Connectivity
   can reconstruct a partition, but explicit component membership and
   component IDs, names, types, completeness, and evidence are not thereby
   proven preserved.
5. **Optional atom-state limitations:** formal charge, aromaticity, radicals,
   implicit-hydrogen policy, and stereochemistry are absent from the 0.1
   payload.
6. **Optional bond-state limitations:** bond ID, fractional order, conjugation,
   stereochemistry and reference atoms, donor/acceptor direction,
   component-joining semantics, and evidence are absent.
7. **Conditional aromatic mapping:** the converter can encode an aromatic flag
   through the legacy `bond_order="aromatic"` value only when no formal bond
   order takes precedence. The audit must not call this preservation in a
   source row that carries both semantics.

Presence checks must inspect the selected native chemical state directly.
`Topology.has_attribute()` is a public query-capability helper and currently
returns true for some default or absent state metadata; using it blindly would
create false losses. Multi-state inspection must cover every stored state even
when a reference state exists, because the serializer emits only one state.

A2.2 reports current schema losses. It does not add fields to `TopologyDict`,
change component inference, or repair an independent converter defect. Those
remain focused A3 work.

### A3 Repair Partition

The nine remaining failures in the broad native-scope module are not one gate:

| Cohort | Classification | Release treatment |
| --- | --- | --- |
| unconditional preflight on ordinary `convert()` | systemic performance and layering defect | first A3 repair |
| `atom_index` and `n_atoms` not classified as structural | central attribute-policy contradiction | second A3 repair |
| missing thermodynamic series in `StructuresDict` | schema and two-way adapter gap | focused A3 repair |
| `StructuresDict -> MolSys` lacks `skip_digestion` | adapter signature defect | focused A3 repair |
| unconditional `chemical_state_id` expectation for a `None` ID | WIP test-contract error | correct the test; do not invent an ID or loss |
| native `MolSys` projections | additional exhaustive route profiles | assess after systemic repairs; not part of the dictionary-profile gate |
| `MolSys <-> MolSysBuilder` and builder-to-dictionary routes | additional exhaustive route profiles | assess after systemic repairs; do not make them block unrelated work |

The four coordinate-trajectory failures are also route-promotion requests
(`XYZ`, ASCII XYZ, DCD, and XTC), not demonstrated conversion failures. Their
selection, units, and cursor assertions execute beyond the report assertion.
They remain visible candidates for bounded Tier-1 profiles but do not join the
A3 critical path merely because they request `is_exhaustive=True`.

The PDB `evidence` and `int("fram")` symptoms belong to A4 with the rest of the
PDB fidelity causes. Moving them out of A3 prevents a PDB-specific parser
workstream from blocking independent schema repairs.

A3 order:

1. bypass preflight when no report or strictness is requested;
2. align atom-inventory attribute classification;
3. extend and round-trip the selected `StructuresDict` thermodynamic fields;
4. repair the `skip_digestion` adapter signature;
5. correct the invalid `chemical_state_id` expectation;
6. decide which remaining native projection or builder profiles are required
   for the advertised 1.0 Tier-1 surface and defer the rest explicitly.

| A3 cohort | Status | Evidence |
| --- | --- | --- |
| A3.1 — opt-in conversion preflight | `DONE` | ordinary conversion bypass, explicit-report execution, strict rejection, public doctest, and lifecycle documentation landed as `dd13cb351` |
| A3.2 — atom-inventory classification | `DONE` | shared topological/structural classification, focused policy tests, 74 consumer tests, lifecycle documentation, and course validation landed as `998abe325` |
| A3.3 — `StructuresDict` thermodynamic series | `DONE` | two-way unit-bearing series, derived total energy, ordered selection, capability queries, report preservation, lifecycle documentation, and 19 focused tests landed as `006d9e4ed` |
| A3.4 — `StructuresDict -> MolSys` signature | `DONE` | standard signatures, correct local mechanics adapter, matched selected atom axes, lifecycle documentation, and 15 form tests landed as `ab28213c0` |
| A3.5 — invalid state-ID expectation | `DONE` | WIP expectation corrected without fabricating an ID; explicit tracked regression landed as `0434b9b42` |
| A3.6 — remaining native/builder profiles | `DONE` | direct projections, complete builder contracts, builder routes, and bounded coordinate-trajectory profiles are integrated |

A3.6 is split so incomplete builder metadata cannot block or weaken direct
native projection evidence:

| A3.6 cohort | Status | Decision and closure boundary |
| --- | --- | --- |
| A3.6a — direct native projections | `DONE` | four Tier-1 profiles traverse every declared source attribute with instance-aware scope and strict-loss evidence; 37 focused tests and the 481-edge ratchet pass; landed as `c40e3154e` |
| A3.6b — complete native/builder attribute contract | `DONE` | native presence composes stored state; builder declares the exact 96-attribute topology/structures union and delivers every declaration directly; landed as `53fec7b09` and `eb07e6e28` |
| A3.6c — builder conversion profiles | `DONE` | four routes are exhaustive; selected dictionary export canonicalizes atoms, preserves structure order, reports reduced-schema loss, and reconstructs components without inventing hierarchy fallbacks; landed as `4bc1dde7b` |

Direct projection profiles may use one declared-contract traversal shared by
the four approved pairs. This is exhaustive only because it iterates every
attribute the source form declares, performs instance-aware presence checks,
and records every present attribute unsupported by the target with its
topology, structures, chemical-state, or molecular-mechanics scope. It must
not be applied to `MolSysBuilder` until the builder's declaration matches its
actual stored semantics.

A3.6b has two ordered prerequisites:

1. **A3.6b.1 — native instance presence.** Complete and test
   `Topology.has_attribute()` and `Structures.has_attribute()`, then make
   `MolSys.has_attribute()` compose those authoritative helpers rather than
   duplicate partial lists. Minimal empty objects currently report absent
   `temperature`, energy, occupancy, bioassembly, state-ID, and component
   metadata as present; reference-state semantics require an explicit
   single-state versus multi-state distinction.
2. **A3.6b.2 — builder contract.** Define `MolSysBuilder.attributes` as the
   exact union of the native topology and structures contracts (96 current
   attributes, 64 more than its present declaration), delegate missing getters
   directly to `builder.topology` or `builder.structures` without calling
   `build()`, and compose instance presence from the corrected native helpers.

The builder must not declare molecular-mechanics fields or
`structure_chemical_state_index`: it stores neither domain. A test must assert
both union equality and getter availability for every declared attribute so
the contract cannot silently drift again.

The untracked native-scope test module was not one A2 gate. It originally
exposed 13 failures across:

- the three A2 audit cohorts;
- attribute-policy classification;
- thermodynamic schema expansion;
- a `skip_digestion` adapter defect;
- ordinary-conversion preflight bypass;
- `MolSysBuilder` fidelity;
- reverse and projection routes.

Tests must be split or selected by contract rather than made green through one
cross-cutting change.

After A2, A3.1, and A3.2, the same module reports 7 failures and 6 passes. The
atom-inventory failure closed independently; the remaining failures still map
to A3.3–A3.6.

### A3.3 Design Boundary

`molsysmt.native.structures_dict.structures_parameters` already declares
`temperature`, `potential_energy`, and `kinetic_energy`. A3.3 therefore repairs
an incomplete implementation of the existing native dictionary contract; it
does not introduce a new schema or require an H5MSM version increase.

The focused repair must:

1. serialize the three materialized series from `Structures`, preserving
   quantity units and requested structure order;
2. expose them through the `StructuresDict` attribute map, getters, and
   instance-aware `has_attribute()`;
3. derive `total_energy` only when both energy series are present;
4. rebuild `Structures` with the three series and preserve repeated or
   non-monotonic `structure_indices`;
5. update the exhaustive conversion profile so these fields cease to be
   reported as losses only after the executable round trip passes;
6. keep absent optional series absent rather than synthesizing values.

A3.3 does not silently absorb the broader coordinate-free native-structures
contract. `native_structures_contract.md` says that a thermodynamic-only
representation is valid, while the current `Structures.n_structures` and parts
of `StructuresDict` still infer axes primarily from coordinates, velocities,
or box. That systemic inconsistency requires its own bounded repair and
evidence; it must not be hidden inside the dictionary adapter commit.

The untracked compact baseline was created with 62 routes already assumed
exhaustive, before executable audit profiles existed. Because it has never
landed as a release baseline, it must be regenerated once from the conservative
A1 state. Thereafter, each A2 cohort removes only the route it has earned from
accepted non-exhaustive debt. This is a correction of an aspirational initial
baseline, not permission to weaken a landed ratchet.

### Current A1 Evidence to Capture

- **Focused contract and regression tests:** 28 passed with
  `tests/_private/test_conversion_report_scopes.py` and
  `tests/conversion_truth/test_native_bond_seam_adapters.py`.
- **Combined audit observation:** 31 passed and 2 expected A2 failures. The
  former five-test ImportError root cause is closed.
- **Static audit:** reaches its report and records 481 non-exhaustive edges,
  including 62 new relative to the aspirational baseline. A2 must earn those
  exhaustive classifications; A1 does not hide them.
- **Compatibility:** existing two- and three-positional-argument
  `ConversionIssue` construction remains valid because `scope` follows `kind`
  with a `chemical_state` default.
- **Ruff:** changed Python files pass.
- **Public docstring doctest:** 1 passed.
- **Lifecycle documentation:** the existing User Guide Foundations, Toolbox,
  Cookbook, and Common Core conversion-report explanations now document issue
  scope; all four notebooks remain valid JSON.
- **Developer-guide validation and `git diff --check`:** pass.
- **Files changed for implementation:**
  `molsysmt/basic/conversion_report.py`,
  `molsysmt/_private/conversion_report.py`, and
  `tests/_private/test_conversion_report_scopes.py`.
- **Landing:** focused implementation, tests, and lifecycle documentation
  committed as `504df91d0`.

## Segment B — Final Numba Oracle

| Stage | Status |
| --- | --- |
| B1 — generated active-Numba inventory | `DONE` |
| B2 — CPU kernel-to-consumer/evidence manifest | `DONE` |
| B3 — deliberate divergence and tolerance record | `DONE` |
| B4 — final forced-Rust campaign plus bounded Numba oracle | `DONE` |
| B5 — dated, committed oracle artifact | `DONE` |

Existing Rust port and dogfooding results are prerequisites, not B-segment
completion. No new Numba capability may be added while this segment is pending.

## Segment C — Rust Packaging

| Stage | Status |
| --- | --- |
| C1 — permanent crate/module and build-backend design review | `DONE` |
| C2 — production crate relocation and private extension integration | `DONE` |
| C3 — supported Linux/macOS and experimental Windows abi3 wheel CI | `DONE` |
| C4 — Python 3.11–3.13 and supported NumPy installed-wheel tests | `DONE` |
| C5 — sdist contract | `DONE` |
| C6 — metadata, resources, entry points, typing, and lazy-discovery parity | `DONE` |
| C7 — Rust quality, security, license, and portability gates | `DONE` |

Conda publication is tracked separately and does not block C4: controlled
preinstalled sibling dependencies may be used to validate the MolSysMT wheel.
The local pilot wheel closed the C1 design question. The clean exact-commit
wheel recorded in
[C2 Rust Packaging Artifact](release_1_0_rust_packaging_c2_artifact.md)
closes C2 but does not substitute for the C3-C7 matrices.

C1 is closed by [C1 — Permanent crate/module and build-backend design
review](archive/resolved_proposals/rust_packaging_backend_design.md): keep `setuptools`, add
`setuptools-rust`, ship one private `molsysmt._rust` abi3 extension inside the official
Conda package, and do not adopt maturin or a separate `msm_rust_kernels` distribution. Two
findings became binding C3 contracts (clean-build isolation with automated wheel
inspection, and abi3 proven per target rather than assumed from the tag). The earlier
report of a PyPI resolution failure as a C4 blocker is **corrected**: neither
PyPI nor the coordinated Conda channel is a prerequisite for validating the
MolSysMT wheel itself.

C2 started only after B4 closed. Commit `17be9ea50` relocates the crate to
`rust/`, integrates it as `molsysmt._rust`, removes the obsolete separate-package
prototype, and adds an executable wheel-content validator. A clean clone of that
exact commit produced
`molsysmt-0.20.0+156.g17be9ea50-cp311-abi3-linux_x86_64.whl` with SHA256
`a7da5d72804e0df12bbeb7b32c52e55cd34633ae9f0bc3ee34bcf15e4a7ecca5`;
the installed extension exposed all 97 entries and passed a minimum-image smoke.

C4–C7 close on exact commit `c4d8e9074` and GitHub Actions run
`30394881487`. Five native wheels pass 15 platform/Python checks, three NumPy
floors, three installed public smokes, the source-distribution round trip, and
the complete Rust quality/security boundary. The exact artifact names, hashes,
scope, and non-Conda qualification are recorded in
[C4–C7 Rust Packaging Artifact](release_1_0_rust_packaging_c4_c7_artifact.md).

## Segment D — Rust-Only Cut

| Stage | Status |
| --- | --- |
| D1 — direct Rust CPU routing and dispatch removal | `DONE` |
| D2 — CPU Numba/JIT implementation deletion | `DONE` |
| D3 — GPU capability audit and Numba-CUDA deletion | `DONE` |
| D4 — dependencies, warmup, diagnostics, API, docs, and course cleanup | `DONE` |
| D5 — executable zero-Numba/Numba-CUDA/llvmlite gate | `DONE` |
| D6 — session and per-function Rayon resource controls | `DONE` |

## Segment E — Rust-Only Validation

| Stage | Status |
| --- | --- |
| E1 — Rust unit, property, error, panic, GIL, and threading tests | `DONE` |
| E2 — independent scientific-truth matrix | `DONE` |
| E3 — complete MolSysMT suite and release fast gates | `DONE` |
| E4 — installed-wheel platform/Python matrix | `DONE` |
| E5 — maturity-weighted direct-consumer smoke | `DONE` |
| E6 — cold/warm, memory, thread, and oversubscription benchmarks | `DONE` |

### E1–E2 Closure Evidence — 2026-07-28

- `cargo test --manifest-path rust/Cargo.toml --no-default-features`: 80 passed.
- `cargo clippy --manifest-path rust/Cargo.toml --no-default-features -- -D warnings`:
  pass. Deliberate fixed-size and FFI exceptions are local, documented, and do
  not rewrite hot loops solely to satisfy style.
- `python -m pytest --receptor=llm tests/basic/test_parallel_control.py tests/rust -n 4`:
  100 passed before the three boundary regressions were added.
- `tests/rust/test_threading_boundaries.py`: 3 passed, proving representative
  GIL release, simultaneous cached Rayon pools with bounded oversubscription,
  result stability, and conversion of a native panic into a contained Python
  process failure.
- `python -m pytest --receptor=llm tests/scientific_truth -n 12`: 98 passed.
- `validate_scientific_evidence.py`: 43 validated, 0 partial, 0 gaps.
- `check_rust_hot_paths.py`: 18 Rust hot-path files clean.

E1 validates the private extension through representative boundary families;
public wrappers remain the authority for typed argument validation. The
private extension is not a supported user API.

### E5 Consumer Compatibility Evidence — 2026-07-28

Consumer evidence is weighted by release maturity. MolSysViewer is a
foundational MolSysSuite component and therefore a blocking integration gate.
TopoMT and PharmacophoreMT are earlier-stage consumers: their smoke workflows
are diagnostic, and consumer-local adaptation debt does not block MolSysMT
1.0.

- MolSysViewer direct MolSysMT integration and loader smoke: 5 passed.
- TopoMT pocket, physicochemistry, and parity smoke: 7 passed.
- PharmacophoreMT import smoke: passed.
- PharmacophoreMT ER-alpha workflow: failed in consumer code because
  `complex_based.py` calls `msm.get(..., element=True)`. In MolSysMT,
  `element` selects the semantic element level and is not an attribute request.
  The consumer must request the atom element-symbol attribute through the
  current public contract. This is classified as non-blocking
  PharmacophoreMT adaptation debt.

No consumer repository was modified during this audit. TopoMT also retains a
best-effort, exception-swallowed call to the removed `msm.warmup()` in its test
configuration; that cleanup belongs to TopoMT and does not affect the passing
runtime smoke.

### E6 Runtime Benchmark Evidence — 2026-07-28

The exact clean commit `746e22c5f` was measured through the isolated,
correctness-checking Rust-only release benchmark. The machine-readable result
is `release_1_0_rust_runtime_benchmark.json`; its interpretation and
reproduction command are in
[MolSysMT 1.0 Rust Runtime Benchmark](release_1_0_rust_runtime_benchmark.md).

- first native call / best repeated call: 1.60x, with zero Numba cache files;
- incremental peak over a 27.48 MiB payload: 3.80 MiB;
- measured two/four-thread speedups: 1.93x and 3.47x;
- four concurrent calls using two Rayon threads each completed with identical
  correct results;
- the complete suite had already passed under `-n 12`, covering the
  xdist-plus-Rayon process surface.

The numbers describe one recorded host and are not cross-platform performance
guarantees. Installed-wheel identity is separately proven by the closed C4/E4
matrix.

## Parallel Conda Delivery Track

This track is required before claiming a validated package is available from
the `uibcdf` Conda channel, but it is not part of the technical critical path
for the 1.0 source/tag, scientific validation, or manuscript:

1. Resolve the lower dependency chain for Python 3.11–3.14: demonstrated for
   the technical staging candidates, not yet a final release freeze.
2. Build and test an exact MolSysMT ABI3 package on each of five native Conda
   platforms, alongside the MolSysViewer noarch package: **done in staging**
   for technical coordinates MolSysMT `0.22.3` build 0 and MolSysViewer
   `0.23.3` build 0, from pinned source commits.
3. Install that exact pair from staging in fresh Python 3.11–3.14 environments
   without checkout leakage: **20/20 cells passed** on 2026-09-24 in five
   platform-targeted runs. Each cell verified package versions, staging
   URL/SHA-256 provenance, native code, BCIF/PDB-text conversion, and Viewer
   loading/resources. See [the Python 3.14 paired checkpoint](python_3_14_checkpoint.md)
   for the source/artifact hashes and run IDs. This is a major intermediate
   1.0 distribution milestone, not a public release or a full product gate.
4. Still open: choose final coordinated release coordinates and resolve the
   earlier 3.11–3.13 candidate path explicitly; run the exact-commit scientific,
   Viewer, documentation, Qt-where-claimed, and release gates; publish both
   packages without a dependency-cycle exception; verify fresh installations
   from the **public** channel and the resulting release/archival records.

The separate MolSysViewer 3.11–3.13 staging-enabled hosted gates advanced on
2026-09-24. Its Documentation notebooks run `36016496850` passed every
notebook on Viewer source commit `7c4e0cd9` against the staged MolSysMT
0.22.0 dependency. The Qt pipeline passed in `CI` run `36017021764`, but all
six Python matrix jobs failed on missing test-environment requirements after
resolving the dependency pair; the Viewer branch has local fixes awaiting a
hosted rerun. `CI_e2e` run `36016496630` never entered the browser tests:
Playwright's redundant Chromium archive extraction timed out, and the Viewer
workflow now selects the Chrome already used by its E2E harness. These results
are neither a green Viewer release gate nor a test of the newer 20-cell
3.14 package matrix. The diagnosis and next run belong to
`uibcdf/molsysviewer#88`.

The next Viewer runs narrowed, but did not close, this gap: `CI`
`36019810641` passed Qt and four of six Python matrix jobs; the other two
exposed a Node 26 JS-tool incompatibility and a fast-close WebSocket test
race. `CI_e2e` `36019810581` ran real Chrome and passed its first 22
scenarios before a PNG-download timeout. That scenario passed locally on the
source pair, but the local aggregate then stopped at scenario 25 because
this host cannot navigate command-line Chrome to the render-worker localhost
page. Thus neither hosted nor local E2E is 37/37. The proposed evidence-lane
redesign is uibcdf/molsysviewer#100; it does not waive the Viewer release
gate or change the 20-cell installed-pair result.

The next local source-pair pass separated browser evidence from the managed
server-GPU worker: MolSysViewer's 36 portable E2E scenarios all passed with
Chrome 149 and WebGL2. Hosted `CI_e2e` is configured to run that explicit
portable lane but has not yet been rerun. The independent `remote-session`
GPU lane remains failing locally because its Chrome process does not navigate
to the worker's loopback page; a CDP-navigation attempt also timed out and
was reverted. This is tracked by uibcdf/molsysviewer#100 and deferred until
after the coordinated pre-1.0 MolSysMT/MolSysViewer package publication. Do
not convert 36/36 portable into a full 37/37 or a 1.0 sign-off.

The next staging-enabled Viewer `CI` run `36034111547` passed Qt but its
six Python jobs stopped at one stale repository test that selected the
old E2E workflow step name. Viewer corrected the guard to select the actual
portable command, with 24 focused local tests passing. The staging-enabled
Viewer rerun `36036802158` on commit `2594f1a2` passed all seven jobs (six
Python matrix cells and Qt), confirming branch CI with staged MolSysMT. The
hosted portable `CI_e2e` rerun `36038233512` repeated the prior failure at
scenario 23/36: `remote-client-rendering` timed out waiting for the PNG
download, although it passed in the local 36/36 portable run. Do not count
this as hosted E2E success or rerun the unchanged test; #100 tracks the
deferred evidence-lane decision. The public-channel `main` gate and managed
server-GPU lane remain separate. This does not change the installed-pair
20/20 evidence.

The 20-cell result does not promote the technical `0.22.3`/`0.23.3` coordinates
into a release decision or alter the independent F6 sign-off. Windows passed
the core installation gate but remains experimental as a product-support
platform; optional Qt-host coverage has its own boundary.

### Next immutable candidate — 2026-09-24

The `python-3.14-support` branches now include the latest `main` commits of
both repositories. Select fresh coordinates MolSysMT `0.22.4` ABI3 build 0
and MolSysViewer `0.23.4` noarch build 0: neither version existed in the
Anaconda release registry (HTTP 404 for both), so the older technical staged
files are not repurposed. The committed route plans select staging. Release
events for these versions will not rebuild the files; exact SHA-256 promotion
to `main` has its own workflow and requires a successful full 20-cell pair
run. The five-platform promotion has not yet been exercised on GitHub.

MolSysViewer's prior 7/7 staged CI run pinned MolSysMT `0.22.0`, not the
newer technical `0.22.3` or this planned `0.22.4` candidate. Its three
manual hosted gates now take an explicit MolSysMT version input; they must be
rerun against `0.22.4` after its staging build. At candidate selection,
neither new version had been uploaded; build-0 staging is recorded below. The
hosted E2E PNG timeout remains an open defect under uibcdf/molsysviewer#100.

The maintainers now accept a narrowly scoped pre-1.0 exception for that
`0.22.4`/`0.23.4` package candidate: Viewer hosted portable E2E run
`36038233512` failed at scenario 23/36, while local portable E2E passed
36/36 and the separate server-GPU lane is unvalidated. This is permission to
advance the paired package publication once its other exact-commit gates
pass, **not** a hosted E2E pass, a full 37/37 result, or a 1.0 sign-off.
uibcdf/molsysviewer#100 stays open and the 1.0 release gate is unchanged.

The local MolSysMT source-pair suite now passes **10,225 tests with 11 known
skips**, using 12 workers and explicit paths for this MolSysMT branch, this
MolSysViewer branch and the released SMonitor `0.16.0` tag. The first attempt
accidentally imported the editable main checkout and was discarded as invalid
evidence. The corrected run exposed the already-tracked warning round-trip
defect in uibcdf/molsysmt#236; a consumer-side args-only path and
`smonitor>=0.16.0` floor close it locally while uibcdf/smonitor#21 remains
open. The suite also exposed an obsolete fixed water count in the native
peptide overlap test; it now checks the initial contact count against the
removed waters and that no contacts remain, without requiring optional
`tleap`. The release metadata was first prepared for `0.22.4` on 2026-09-24
and refreshed to the intended 2026-09-25 publication date after the local
date changed. The build-0 artifacts recorded below have not
passed the final exact-commit gates; if publication moves to another date,
update citation metadata and revalidate the resulting candidate before tagging.
MolSysSuite authorized the two transition issues (`uibcdf/molsysmt#237` and
`uibcdf/molsysviewer#93`) in `policy-v1.4.11` on 2026-09-24. Both candidate
callers now pin that release, their synchronized suite guides identify the
same effective snapshot, and the exact central repository checker passes
locally for both. `authorized` requires Python 3.14 metadata and CI, but the
canonical README badge remains at the publicly admitted 3.11–3.13 range until
the coordinated release and independent channel installations permit central
`admitted` status. The 3.14 package contract remains in the candidates; no
public-channel or suite-wide 3.14 claim follows from authorization alone.
Any later source change requires new exact-commit gates; the final
installed-pair and other release gates remain open.
The new policy's Ruff 0.16.5 formatting gate exposed three older files in
the Conda release route and its tests; they were formatted without changing
behavior. Repository-wide Ruff lint and format checks now pass, the two
focused release-route test modules pass 8/8, and the fast release gate remains
13/13.
The earlier exact-source-pair run `36061167557` passed Linux and macOS/Python
3.14 but failed Windows in Viewer's release-route test: Windows resolved
`bash -n` to the WSL launcher, although the promoted script is hosted only on
Ubuntu. Both repositories now retain the promotion identity assertions on
Windows and check Bash syntax on POSIX, with an explicit Ubuntu-runner guard.
This test correction still requires an exact-new-commit hosted Windows rerun;
the failed run is not counted as a passing 3.14 gate.
The corrected source-pair run `36062983964` subsequently passed Linux,
macOS and Windows/Python 3.14. Technical staging build 0 produced all five
native MolSysMT ABI3 files (`36063170604`) and the paired Viewer noarch file
(`36064255601`); the installed-pair run `36065287565` passed all 20 cells
(five platforms times Python 3.11–3.14). Viewer CI against staged MolSysMT
passed all seven jobs in `36064424260`, and its notebooks passed in
`36064424563`. The first MolSysMT full-CI run `36063386092` exposed a
different dependency floor error: its controlled ArgDigest commit predates
the catalog exception fix needed with SMonitor 0.16.0, so the same ten
error-contract tests failed in each of its six cells. Published ArgDigest
0.13.0 (exact tag commit
`9880fa7b990fd0987ff0de715b665eb9e11c11b2`) has that fix and passes
the 27 affected local contract tests with the released SMonitor 0.16.0 tag.
The complete local MolSysMT suite with those exact dependency sources passed
10,225 tests with 11 skips; the matching Viewer suite passed 2,112 tests
with 14 skips, both using 12 workers.
Both component candidates now require ArgDigest 0.13.0 and the controlled CI
pin names its exact release source. A new early CI check rejects controlled
source pins whose installed versions violate the declared runtime floor.
Build-0 staging and its passing 20-cell run are diagnostic only for this
corrected contract; build 1 must supersede each staged file and receive fresh
exact-commit gates before promotion. A local
Sphinx build on the source pair completed without missing-toctree warnings;
it still reported 744 unrelated/baselined warnings. The hosted Pages workflow
was not dispatched from the candidate branch because it would deploy public
documentation and currently pins an older Viewer source.
The build-1 Conda producers (`36102277287`, five of five ABI3 platforms;
`36102277047`, one noarch package) passed, and the corrected Python 3.14
source-pair workflow `36102309036` passed all three operating systems. The
exact-commit Rust-wheel gate `36102309653` built its artifacts but failed its
three installed-public-smoke cells: that job independently checked out old
PyUnitWizard and other sibling SHAs, then crashed on the missing
`configure.has_active_policy()` API. The function is present in PyUnitWizard
0.25.0 but not 0.24.0. Both component metadata floors and their Conda recipes
now require 0.25.0, and the wheel smoke consumes the single controlled-source
manifest plus an exact Viewer SHA input. The build-1 full CI `36102308805`
passed 7/7, and the exact installed-pair run `36105020606` passed 20/20;
they are diagnostic evidence only because the metadata floor and wheel
workflow changed afterward. Build 2 and all exact-commit gates must be rerun
before promotion. Local dependency-contract experiment
`uibcdf/molsysmt#245` now audits `pyproject.toml` against both recipes,
runtime environments, the hard/soft form registry, and source-consuming CI
jobs. Its first pass found the missing `py-mmcif` Rattler dependency,
unbounded environment floors, and a benchmark job without its controlled
siblings; these were corrected. Nine mutation/integration tests and the
expanded local fast gate 14/14 pass. The obsolete requirements broadcaster
and its inventory were retired; the active source manifest was relocated to
`devtools/controlled_sources.txt` with every workflow consumer updated.
The next exact-source attempt produced all five MolSysMT staging build-2
artifacts (`36111977722`) and the MolSysViewer noarch build-2 artifact
(`36111980483`); the Viewer Python 3.14 source pair passed three operating
systems (`36112007408`). MolSysMT full CI (`36112007337`) and the installed
Rust-wheel smoke (`36112007478`) correctly rejected the controlled
PyUnitWizard source pin: although commit `c69192ec` has the needed API, it
builds as `0.24.0+35`, below the new runtime floor `>=0.25.0`. The source
manifest now pins exact PyUnitWizard `0.26.0` tag commit `026be28d`, which
contains the API and declares Python 3.14 support. The dependency auditor,
23 focused tests, and the fast release gate 14/14 pass locally after this
correction. Build-2 artifacts and their earlier gates remain diagnostic;
the corrected commit still requires fresh exact-source gates and a new
staging build number before promotion.

## Segment F — Lifecycle and Release Candidate

| Stage | Weight | Status | Earned |
| --- | ---: | --- | ---: |
| F1 — Four Paths numbering and structural validation | 1% | `DONE` — 20 + 4x34 notebooks, semantic manifest identities and no validator exception at `c87a14036` | 1% |
| F2 — applicable Common Core and changed-behavior notebook execution | 2% | `DONE` — 40/40 pass from clean kernels at `2f6fd59d1` | 2% |
| F3 — function support-tier and pending-guide hygiene | 1% | `DONE` — 117 Tier 1, 56 Tier 3, seven outside-contract; completed records archived | 1% |
| F4 — User Guide, Cookbook, API, demos, and course lifecycle closure | 2% | `DONE` | 2% |
| F5 — clean exact-commit fast, full, wheel, and documentation gates | 3% | `DONE` — exact commit `38ab61f6e` passes every declared F5 gate | 3% |
| F6 — 1.0 release candidate and tag | 1% | `IN PROGRESS` — citation metadata and governance are prepared; exact final gates, tag, GitHub Release, and Zenodo version verification remain | 0% |
| **Segment F total** | **10%** | **`IN PROGRESS`** | **9%** |

## Deferred Work

These remain `DEFERRED` unless a correctness defect promotes them:

- additional native format parsers;
- Arrow and optional-column memory experiments;
- additional interaction families and reactive chemical-state expansion beyond
  the accepted 1.0 interaction result and persistence scope;
- speculative Rust GPU work and fused multi-observable kernels;
- broad Tier 2 and Tier 3 adapter expansion;
- nonessential post-threshold micro-optimization;
- paper extensions that alter no release contract.

## Update Procedure

Update this ledger whenever a stage changes status:

1. change only the affected stage and segment rows;
2. record the exact command, result, and commit in the execution log;
3. add earned weight only when the applicable segment or explicit F-stage exit
   gate passes; never count the F total again after summing its stages;
4. name blockers explicitly; never hide them inside `PENDING`;
5. preserve accepted omissions and deferred work;
6. identify the next active stage;
7. run `python devtools/scripts/validate_devguide.py`;
8. include the ledger update with the stage-closing commit.

If evidence was produced on a dirty tree, label it development evidence. Replace
it with exact-commit evidence before marking a release gate `DONE`.

## Execution Log

| Date | Segment/stage | Transition | Evidence | Commit |
| --- | --- | --- | --- | --- |
| 2026-07-26 | Overall plan | status ledger created | planning and repository audit; no implementation gate claimed | dirty WIP at `7ab96e791` |
| 2026-07-26 | A / A1 | `PENDING` → `IN PROGRESS` | 38-failure diagnosis and four-stage resolution plan accepted | dirty WIP at `7ab96e791` |
| 2026-07-26 | A1 implementation | remains `IN PROGRESS` pending landing | 28 focused passes; 1 doctest; combined audit surface 31 passed / 2 A2 failures; Ruff, notebook JSON, and devguide green | dirty WIP based at `7ab96e791` |
| 2026-07-26 | A1 | `IN PROGRESS` → `DONE` | scope contract, regression tests, and lifecycle documentation landed | `504df91d0` |
| 2026-07-26 | A2 design | `PENDING` → `IN PROGRESS` | conservative registry exposes 62 aspirational exhaustive routes requiring evidence-backed cohorting | dirty WIP after `504df91d0` |
| 2026-07-26 | A2 design audit | remains `IN PROGRESS` | 118 canonical attributes inspected; form capability maps and serialized-schema fidelity are distinct; focused module reports 13 independent root causes; A2 split into three native-to-dictionary cohorts | dirty WIP after `504df91d0` |
| 2026-07-26 | A2.1 | `IN PROGRESS` → `DONE` | 38 focused tests; 1 exhaustive and 480 accepted non-exhaustive Tier-1 edges; zero new debt; Ruff, lifecycle notebooks, and developer-guide validation pass | `cb123e226` |
| 2026-07-26 | A2.2 | `PENDING` → `IN PROGRESS` | topology serialization-boundary audit selected as the next cohort | dirty WIP after `cb123e226` |
| 2026-07-26 | A2.2 design audit | remains `IN PROGRESS` | 76 declared topology attributes partitioned into stable, derived, state-inventory, component, optional atom/bond, and conditional aromatic semantics | dirty WIP after `cb123e226` |
| 2026-07-26 | A2.2 | `IN PROGRESS` → `DONE` | 44 focused tests; 2 exhaustive and 479 accepted non-exhaustive Tier-1 edges; zero new debt; Ruff, lifecycle notebooks, and developer-guide validation pass | `4a4773986` |
| 2026-07-26 | A2.3 | `PENDING` → `IN PROGRESS` | composed native MolSys audit selected as the next cohort | dirty WIP after `4a4773986` |
| 2026-07-26 | A2.3 | `IN PROGRESS` → `DONE` | 51 focused tests; 3 exhaustive and 478 accepted non-exhaustive Tier-1 edges; zero new debt; broad native-scope module reduced to 9 independent failures | `01067f2c5` |
| 2026-07-26 | A2 | `IN PROGRESS` → `DONE` | all three native dictionary cohorts landed with explicit complete-source contracts | `cb123e226`, `4a4773986`, `01067f2c5` |
| 2026-07-26 | A3 | `PENDING` → `IN PROGRESS` | remaining independent schema, attribute-policy, adapter, and preflight repairs selected for classification | dirty WIP after `01067f2c5` |
| 2026-07-26 | A3 classification | remains `IN PROGRESS` | 9 broad native-scope failures split into 5 focused repairs and optional route promotion; 4 coordinate failures classified as profile requests; PDB-specific symptoms assigned to A4 | dirty WIP after `01067f2c5` |
| 2026-07-26 | A3.1 | `IN PROGRESS` → `DONE` | 54 focused tests and public doctest pass; ordinary conversion no longer constructs an unused preflight; broad native-scope module reduced to 8 independent failures | `dd13cb351` |
| 2026-07-26 | A3.2 | `PENDING` → `IN PROGRESS` | atom inventory classification selected as the next systemic repair | dirty WIP after `dd13cb351` |
| 2026-07-26 | A3.2 | `IN PROGRESS` → `DONE` | 74 consumer tests pass across attribute policy, compare, iterator, get, and StructuresDict round-trip; broad native-scope module reduced from 8 to 7 independent failures; Ruff, notebook JSON, and course validation pass | `998abe325` |
| 2026-07-26 | A3.3 design audit | `PENDING` → `IN PROGRESS` | thermodynamic keys already belong to the declared StructuresDict contract; missing two-way adapters, getters, capabilities, selection, and audit-profile preservation identified; coordinate-free native contract explicitly kept separate | dirty WIP after `998abe325` |
| 2026-07-26 | A3.3 | `IN PROGRESS` → `DONE` | optional temperature and energy series preserve units and arbitrary requested order in both directions; total energy remains derived; broad native-scope module reduced from 7 to 6 failures | `006d9e4ed` |
| 2026-07-26 | A3.4 | `PENDING` → `DONE` | standard adapter signatures, correct local mechanics dispatch, and matching selected topology/structure atom axes; 15 form tests pass | `ab28213c0` |
| 2026-07-26 | A3.5 | `PENDING` → `DONE` | absent optional state ID no longer expected as a loss; production unchanged; 15 contract tests pass and broad module reduced to 5 route-profile failures | `0434b9b42` plus corrected untracked WIP test |
| 2026-07-26 | A3.6 design audit | `PENDING` → `IN PROGRESS` | four direct native projections accepted as Tier 1; builder profiles held behind a complete builder attribute-contract audit | dirty WIP after `0434b9b42` |
| 2026-07-26 | A3.6a | `IN PROGRESS` → `DONE` | 37 focused tests; four direct profiles accepted; exhaustive coverage 3 → 7 and accepted debt 478 → 474 with zero new or unresolved baseline drift; lifecycle documentation and course validation pass | `c40e3154e` |
| 2026-07-26 | A3.6b | `PENDING` → `IN PROGRESS` | complete builder attribute contract selected as the prerequisite to any builder-profile promise | dirty WIP after `c40e3154e` |
| 2026-07-26 | A3.6b design audit | remains `IN PROGRESS` | builder declares 32 of 96 stored native attributes; 64 missing; empty native forms demonstrably return false-positive presence for optional thermodynamic, occupancy, bioassembly, state-ID, and component fields; reference-state semantics require separate review; native presence repair ordered before builder delegation | dirty WIP after `c40e3154e` |
| 2026-07-26 | A3.6b.1 | `IN PROGRESS` → `DONE` | native `Topology`, `Structures`, and composed `MolSys` presence contracts now distinguish declared capability from instance state; 1,601 broad consumers and 70 focused tests pass | `53fec7b09` |
| 2026-07-26 | A3.6b.2 | `IN PROGRESS` → `DONE` | builder declares the exact 96-attribute stored union, all declarations have direct getters, representative chemistry and thermodynamic reads do not materialize `MolSys`, 185 consumer tests pass, and five lifecycle notebooks execute successfully | `eb07e6e28` |
| 2026-07-26 | A3.6c | `PENDING` → `IN PROGRESS` | the broad native-scope module now has exactly three independent failures, all caused by missing exhaustive builder conversion profiles; conversion ratchet remains 7 exhaustive, 474 accepted debt, and zero drift | dirty WIP after `eb07e6e28` |
| 2026-07-26 | A3.6c | `IN PROGRESS` → `DONE` | four builder routes promoted with distinct evidence; atom selection and structure ordering fixed; isotope and derived-component seams repaired; 13 broad-scope, 88 builder/dictionary, and 49 convert tests pass; five lifecycle notebooks execute; coverage 7 → 11 and accepted debt 474 → 470 with zero drift | `4bc1dde7b` |
| 2026-07-26 | A3 | `IN PROGRESS` → `DONE` | all independent native schema, adapter, presence, projection, and builder-profile repairs are landed; PDB-specific work remains isolated in A4 | `dd13cb351` through `4bc1dde7b` |
| 2026-07-26 | A4 design audit | `PENDING` → `IN PROGRESS` | 21 PDB failures reduced to five shared causes; duplicate parsing between the handler and native adapters identified as the architectural root | dirty WIP after `18136a95d` |
| 2026-07-26 | A4 | `IN PROGRESS` → `DONE` | handler-owned normalized content now governs file, text, and handler input; canonical alternate sites, explicit chemistry, bioassemblies, canonical writing, payload-aware reports, 22 PDB tests, 139 historical/integration tests, and 60 convert tests pass; exhaustive coverage 11 → 22 with zero new debt | `1f656fe9f` |
| 2026-07-26 | A5 | `PENDING` → `IN PROGRESS` | Segment A integration gate selected; known external-form attribute-delivery debt remains explicit and PDB adapters themselves pass | dirty WIP after `1f656fe9f` |
| 2026-07-26 | A5 / Segment A | `IN PROGRESS` → `DONE` | isolated committed-snapshot reconstruction passes 85 tests; form adapters 89/89; exhaustive conversion coverage 22 → 37; accepted debt 470 → 444; zero new debt; Ruff, dependencies, devguide, course, demos, resources, scientific evidence, Rust hot paths, and public smoke pass; the only aggregate-gate red is independent F3 function-tier hygiene | `9660f6e79` |
| 2026-07-26 | B / B1 | `PENDING` → `IN PROGRESS` | Segment A dependency closed; generated active-Numba runtime inventory selected as the next oracle stage | dirty WIP after `9660f6e79` |
| 2026-07-26 | B1 | `IN PROGRESS` → `DONE` | AST inventory freezes 48 direct Numba/llvmlite imports, 108 CPU JIT callables, 52 CUDA JIT callables across 13 CUDA-coupled modules, and 46 direct consumers; broader runtime, dependency, test, tool, build, experiment, and documentation surfaces are recorded; three ratchet tests, Ruff, YAML parsing, and the live audit pass; smoke CI rejects new guarded coupling | `de2ccf988` plus the immediate nested-`try` traversal correction |
| 2026-07-26 | B2 | `PENDING` → `IN PROGRESS` | B1 baseline landed; CPU kernel-to-Rust-consumer-evidence classification selected | dirty WIP after `de2ccf988` |
| 2026-07-26 | B2 | `IN PROGRESS` → `DONE` | generated manifest maps all 108 CPU JIT callables across 15 families: 87 direct Rust dispatchers, one alias, and 20 explicitly absorbed helpers; every family names consumers, parity tests, and independent scientific or property evidence; 264 Rust tests and 82 selected scientific-truth tests pass; the live and isolated-environment audits, six ratchet tests, Ruff, CI YAML, and devguide validation pass | `863c77fb7` |
| 2026-07-26 | B3 | `PENDING` → `IN PROGRESS` | complete B2 map landed; deliberate numerical and behavioral divergence extraction selected as the next oracle gate | dirty WIP after `863c77fb7` |
| 2026-07-26 | B3 | `IN PROGRESS` → `DONE` | all 14 parity modules have accepted policies; 77 closeness sites declare both tolerances; 63 formerly implicit `rtol=1e-5` comparisons remain green with explicit strict contracts; eight deliberate divergences and four must-match contracts have executable evidence; 274 Rust/validator tests and 82 selected scientific-truth tests pass; zero provisional decisions remain | `b4b6bae25` |
| 2026-07-26 | B4 | `PENDING` → `IN PROGRESS` | closed B3 contract landed; reproducible final two-backend campaign selected | dirty WIP after `b4b6bae25` |
| 2026-07-26 | B4 strategy refinement | remains `IN PROGRESS` | the release runtime receives the complete forced-Rust suite; Numba is limited to the bounded oracle surface and failed-node attribution because it will not ship in 1.0 | `481271204` |
| 2026-07-26 | B4 checkpoint | `IN PROGRESS` → `BLOCKED` | exact source and wheel hashes recorded; forced-Rust smoke 15/15, Rust oracle 264 passed with three documented skips, and 82 scientific tests pass; complete forced-Rust suite reaches 9,361 passed but has 36 failed and 342 errors in 11 non-Rust root causes; all 378 unsuccessful node IDs reproduce with forced Numba; B4 requires a new green exact-commit run after the active WIP is landed | `481271204`; see `release_1_0_rust_campaign_checkpoint.md` |
| 2026-07-26 | B4 blocker reduction | remains `BLOCKED` | native bioassembly translations remove the 342-error PDB cascade; `MolSys` now delivers `structure_index`; H5MSM preserves optional structural and thermodynamic series, repeated structure order, partial-layer semantics, and multi-state inventory queries; the relevant H5MSM/report gate passes 1,074 tests and the known targeted residual is six root causes | `30d12a7c9`, `64ac440de`, `7cf7d7206` |
| 2026-07-26 | C1 packaging design review | `PENDING` → `DONE` | `python -m pip wheel . --no-deps` on branch `packaging/rust-c1-spike` produced `molsysmt-0.20.0+149.gcb3341fd5.dirty-cp311-abi3-linux_x86_64.whl` carrying `molsysmt/_rust.abi3.so`, `py.typed`, 292 `molsysmt.data` files, the `molsysviewer.addons` entry point and a versioningit Git version; the extension built under CPython 3.13 loaded in a clean 3.12 virtualenv, exposed 97 kernels and returned the correct minimum-image distance; development evidence from a dirty tree, accepted for the design question only; C keeps 0% earned weight | `87317ba76` (branch, not merged) |
| 2026-07-28 | B4 NGLView blocker reduction | remains `BLOCKED` pending exact campaign | optional topology snapshots preserve MolSysMT-origin IDs and chemical bond metadata without granting fictitious topology to generic widgets; multi-structure conversion drops partial PDB metadata; group-level hydrogen bonds preserve pair order; 45 NGLView and 746 broad consumer tests pass under forced Rust | NGLView fidelity checkpoint following `6f527bb44` |
| 2026-07-28 | B4 final exact campaign | `BLOCKED` → `DONE` | clean source archive and exact Rust wheel rebuilt from `6485a0c08`; bounded oracle passes 264 tests with 3 documented skips; combined migration/scientific gate passes 501 tests with 3 skips; complete forced-Rust suite passes 9,769 tests with 5 accepted skips and zero unsuccessful outcomes | `6485a0c08`; `release_1_0_final_numba_oracle_artifact.md` |
| 2026-07-28 | B5 oracle artifact | `PENDING` → `DONE` | dated artifact preserves the exact commit, environment, commands, source archive hash, wheel hash, installed-extension hash, bounded two-backend result, independent evidence, and complete application result | `release_1_0_final_numba_oracle_artifact.md` |
| 2026-07-28 | C2 production Rust integration | `PENDING` → `DONE` | crate relocated to `rust/`; private `molsysmt._rust` integrated through setuptools-rust; separate-package traps removed; 80 Rust and 270 Python tests pass with 3 documented skips; exact-commit Linux wheel is `cp311-abi3`, passes automated content validation, installs non-editably, exposes 97 entries, and computes the minimum image correctly | `17be9ea50`; `release_1_0_rust_packaging_c2_artifact.md` |
| 2026-07-28 | C3 multiplatform wheel CI implementation | remains `IN PROGRESS` | five native targets, pinned Rust/cibuildwheel configuration, strict abi3/content inspection, isolated installed-extension smoke, and artifact retention implemented; 12 contract tests, 80 Rust tests, Ruff, dependency validation, and local C2-wheel smoke pass; remote five-target run pending; pre-existing rustfmt debt assigned to C7 | `30b86cdf2`; `release_1_0_rust_packaging_c3_checkpoint.md` |
| 2026-07-28 | C3 exact-commit remote matrix | `IN PROGRESS` → `DONE` | GitHub Actions run `30346103646` passes Linux x86_64/aarch64, macOS x86_64/arm64, and Windows x86_64; every `cp311-abi3` wheel passes build/audit, non-editable installed-extension validation, 97-export and minimum-image smoke, and artifact upload; exact wheel hashes and runner images are preserved | `f79ccb4f0`; `release_1_0_rust_packaging_c3_checkpoint.md` |
| 2026-07-28 | C4 installed-wheel matrix | `PENDING` → `IN PROGRESS` | C3 portability dependency closed; Python 3.11–3.13 and supported NumPy installed-wheel execution selected as the active packaging gate | after `f79ccb4f0` |
| 2026-07-28 | D1–D5 / Segment D | `PENDING` → `DONE` | production routing is Rust-only; CPU JIT, CUDA, incomplete Taichi experiments, runtime controls, dependencies, JIT warm-up API, diagnostics, and migration parity tests are removed; low-level compatibility paths remain Rust-backed; the executable zero gate passes; 122 focused and 450 broad affected tests pass, with one separate network-dependent test excluded | dirty implementation; `release_1_0_rust_only_cut_artifact.md` |
| 2026-07-28 | D6 Rayon controls | `PENDING` → `DONE` | session defaults and function-local overrides resolve to reusable Rayon pools; nested overrides remain local; 1/2/4-thread execution is directly observable; 165 affected tests pass; representative release-build speedups at four threads are 2.99× distances, 3.54× centers, 3.51× radius of gyration, and 2.73× RMSF | dirty implementation; resolved bug record and `performance_and_jit.md` |
| 2026-07-28 | WIP integration | dirty tree → clean `main` | release gates, function-tier policy, conversion-fidelity records, and native dictionary extraction landed in three focused commits; fast gate 12/12 and 107 conversion-truth tests pass | `83a573f09`, `8579b8e7a`, `0a9353ffc` |
| 2026-07-28 | Conda scheduling | critical-path prerequisite → parallel delivery track | coordinated sibling and MolSysMT Conda publication may proceed during manuscript writing/review; local installed-wheel evidence remains in C/E, while channel availability blocks only the Conda delivery claim | maintainer decision recorded in the execution plan and Conda coordination report |
| 2026-07-28 | E1–E2 | `PENDING` → `DONE` | 80 Rust unit/property tests, Clippy with warnings denied, 103 Python Rust/control/boundary tests, 98 scientific-truth tests, 43/0/0 evidence registry, and 18-file hot-path lint pass; representative GIL release, concurrent Rayon pools, bounded oversubscription, and panic containment are executable regressions | stage-closing Rust validation commit |
| 2026-07-28 | E3 | `IN PROGRESS` → `DONE` | complete Rust-only suite passes 9,585 tests with two accepted skips under `-n 12`; fast release gate passes 12/12; Ruff passes across package, tests, devtools, and root conftest | `692479097` |
| 2026-07-28 | E5 | `PENDING` → `DONE` | maturity-weighted consumer audit: MolSysViewer passes 5/5 as the blocking foundational consumer; TopoMT passes 7/7; PharmacophoreMT imports but its ER-alpha workflow exposes a consumer-local obsolete `element=True` call, recorded as non-blocking adaptation debt | status-ledger commit following `9fbb95569` |
| 2026-07-28 | E6 | `IN PROGRESS` → `DONE` | exact clean-commit Rust-only benchmark records first/repeated calls, memory, raw 1/2/4-thread samples, bounded nested concurrency, native-extension hash, scientific checks, and zero JIT-cache creation | `746e22c5f`; `release_1_0_rust_runtime_benchmark.{md,json}` |
| 2026-07-28 | Minimal installed-runtime defect | discovered → `DONE` | optional forms remain visible but detectors whose mapped soft dependency is absent no longer execute; the missing OpenMM mapping is restored; 449 basic tests and local non-editable smoke without OpenMM pass | `c4d8e9074`; `archive/resolved_bugs/optional_form_detection_broke_minimal_install.md` |
| 2026-07-28 | C4–C7 / E4 / Segments C and E | `IN PROGRESS` → `DONE` | exact run passes five native abi3 wheels, 15 platform/Python checks, three NumPy floors, three installed public smokes, sdist round trip, exact 99-export validation, and Rust formatting, Clippy, tests, advisory, dependency, and license gates | `c4d8e9074`; run `30394881487`; `release_1_0_rust_packaging_c4_c7_artifact.md` |
| 2026-07-28 | F1 status correction | `PENDING` → `DONE` | commit history and the live validator confirm that F1 had already landed: 156 notebooks, core 1–20, four paths 21–54, complete toctrees, unique semantic labels, and a matching manifest; the two remaining editorial references and Sphinx confirmation belong to later lifecycle stages | `f5d96218b`; `python devtools/scripts/validate_course.py` |
| 2026-07-28 | F / F2 | `PENDING` → `IN PROGRESS` | F1 historical evidence recovered; existing notebook-execution evidence must be audited before scheduling new execution or edits | after `03a170442` |
| 2026-07-28 | F2 execution audit checkpoint | remains `IN PROGRESS` | required union reconstructed as 37 notebooks; in-memory clean-kernel run passes 14/26 deterministic notebooks, exposes 12 failures requiring ownership classification, and defers 11 network/interactive notebooks; no notebook outputs or content were modified | `release_1_0_f2_notebook_execution_checkpoint.md` |
| 2026-07-28 | F2 correction pass | remains `IN PROGRESS`, ready to land | all 26 deterministic and all 11 network/headless notebooks pass from clean kernels; seven bounded library-contract corrections have regression coverage; affected User Guide notebooks execute; formal closure awaits validation, landing, and exact-commit 37/37 rerun | dirty worktree based on `2340d1eff`; `release_1_0_f2_notebook_execution_checkpoint.md` |
| 2026-07-29 | F2 exact-commit closure | `IN PROGRESS` → `DONE`; F3 becomes active | final scope expands from 37 to 40 because Scalability corrections affect all four Paths; the complete Common Core plus notebooks 28, 29, 47, 48, and 49 of every Path pass from fresh kernels with no persisted outputs | `2f6fd59d1`; `release_1_0_f2_notebook_execution_checkpoint.md` |
| 2026-07-29 | F3 support-tier and lifecycle reconciliation | `IN PROGRESS` → `DONE`; F4 becomes active | function tiers derive from the exhaustive API stability registry and validate as 117 Tier 1, 56 Tier 3, and seven outside-contract; nine completed/superseded proposals and one historical audit leave the pending queue; normative links and resolution records are updated | `release_1_0_f3_support_and_lifecycle_checkpoint.md`; documentation-only work based on `fd19f9196` |
| 2026-07-29 | F4 documentation lifecycle | `IN PROGRESS` → `DONE`; F5 becomes active | final course narrative references use stable semantic targets; the numbering report and Rust migration residue are archived; the missing dihedral broadcast regression passes on vacuum and periodic paths; checked-in autosummary surfaces are refreshed; 11 stale toctree targets are repaired; Sphinx builds successfully and the remaining warning families are measured as accepted documentation debt | `672f8f065`; `release_1_0_f4_documentation_lifecycle_checkpoint.md` |
| 2026-07-29 | Segment F progress accounting | no stage transition; weighted closure 90% → 96% | the fixed 10% Segment F budget is partitioned across six independently gated stages; completed F1–F4 earn 6%, while F5 and F6 retain the remaining 4%; no technical exit criterion or release requirement changes | maintainer-approved accounting update after `075cb0432` |
| 2026-07-29 | Atom-axis `add()` WIP integration | dirty pre-F5 worktree → clean candidate base; no stage transition | native and public addition share one atom-axis contract; MolSys mutation is transactional; adapters, multiple-source dispatch, scalar returns, lifecycle documentation, and regressions are synchronized; 30 focused and 554 expanded tests pass, two notebooks execute, Ruff passes, and the fast gate passes 12/12 | `2865c3122`; `release_1_0_atom_axis_add_checkpoint.md` |
| 2026-07-29 | Atom-axis `add()` semantic follow-up | F5 remains active; bounded audit inserted before its expensive exact-commit matrix | multi-source selection/cardinality, whole-call transaction scope, one-sided atom-aligned data, structure metadata and energy validity, coordinate-free structures, adapter parity, diagnostics, and memory are recorded with phases and acceptance criteria; no behavior or weighted progress changed | `87ccfc289`; `pending_proposals/atom_axis_add_semantic_audit.md` |
| 2026-07-28 | Developer-guide coherence pass | no stage transition | post-migration documentation debt cleared: four Numba-era bug reports and four Numba-era proposals archived with resolution notes after verifying each against the Rust runtime; one stale duplicate report removed; the three Numba migration documents relabelled as historical evidence; snapshot sentences that still called Segment C open corrected; `pending_bugs` and `pending_proposals` indexes rewritten; 11 broken intra-guide links repaired; devguide validation and the fast gate pass 12/12; code, tests, and notebooks untouched, with the residue recorded in `archive/resolved_proposals/rust_migration_documentation_and_test_residue.md` | `2340d1eff` |
| 2026-07-29 | Presentation surface | no stage transition | the README and documentation landing pages described MolSysMT as middleware between other libraries and advertised the removed Numba/CUDA architecture; `docs/content/about/what.md` disowned the library's own native capability. Reframed with the molecular system as subject. Verified against the installed package: seven `to=` calls should be `to_form=`, the sequence and dihedral examples raise, and the cross-library showcase raises `NotImplementedConversionError` because no route to `MDAnalysis.Universe` exists. The tier table showed about eleven Tier 1 forms where the live registry reports 75 of 89, and claimed any Tier 1 pair converts. The Conda recipe had an empty summary. Every example now executes; ruff, devguide, course, and fast gate 12/12 pass | `d2b805e74`; `pending_proposals/readme_positioning_and_1_0_refresh.md` |
| 2026-07-29 | Documentation and paper track | critical-path work → named parallel track | with A–E and F1–F4 closed, presentation, documentation and the methods paper become a principal parallel workstream; the three items the positioning pass could not close are specified with acceptance criteria | `pending_proposals/presentation_and_citation_surface.md` |
| 2026-08-03 | Topology vocabulary, DCD backend noise and the course gate | three reports → `DONE`; no stage transition | `get_covalent_chains` is renamed `get_covalent_paths`: `chain` is an element of a molecular system while the function walks the covalent graph returning paths, and `get_covalent_blocks` was already named to avoid the same collision with `component`. No deprecation cycle, the policy starts at 1.0.0. `get_dihedral_quartets(with_blocks=True)` raised on every real system by pushing ragged block sets through `np.array`; on T4 lysozyme 158 of 161 phi quartets split in two and 3 do not, and those 3 are the prolines. Module 13 of the Common Core taught `get_covalent_blocks` as the way to obtain components, contradicting its own tutorial, and the quickstart placed four topology functions in `molsysmt.structure`. MDTraj's DCD reader printed to the C standard output on every open and every read with no way to disable it; suppressed behind `configure.silence_backend_stdout`, 26 lines to 0, and recorded as evidence in the native-parser proposals rather than as a reason to write one. `validate_course.py` was red with 20 errors because it asserted a Common Core module count and a label scheme the section has not settled; both deferred explicitly, gate green at 155 notebooks | `dfa57c073`; `647694061`; `1541f8775`; `acd4404c7`; `archive/resolved_bugs/dihedral_quartets_with_blocks_raises_on_ragged_blocks.md`; `pending_bugs/course_gate_red_after_common_core_renumbering.md` |
| 2026-08-03 | Structure axis of a composite molecular system | two reports → `DONE`; no stage transition | a molecular system spread over complementary items had no structure axis of its own, so `where_is_attribute` broke its tie between providers that are not interchangeable. `msm.get([h5msm, dcd], n_structures=True)` returned 20 while `msm.get([dcd, h5msm], n_structures=True)` returned 1, `msm.convert` on the second order discarded nineteen structures with no diagnostic, and `get` returned `time` of length 1 beside `coordinates` of length 20 for one system. The axis is now the largest structure count among the items carrying structural data, order-independent; only items spanning it may deliver a structural attribute, with the existing last-matching-item tie-break applying among those; an item holding zero or one structure below the axis is a reference conformation whose series are dropped with the new `StructuralAttributeOffAxisWarning` (`MSM-WARN-STRUCT-006`); and two items each holding more than one structure, of different lengths, raise `StructuralInconsistencyError` naming `molsysmt.concatenate_structures`. This completes on the structure axis the consistency contract already enforced on the atom axis by `_private/molecular_system_validation.py:144-151`, and the asymmetry between raising on atoms and warning on structures is deliberate: `[pdb, xtc]` is one structure beside a trajectory and must keep working. `convert` needed its own intervention because it never resolved attributes through `where_is_attribute`. The `Iterator` defects closed with it, including an unguarded `append` that yielded zero items without error depending on keyword order, and an H5MSM reader indexing an empty `structures/id` dataset. 7913 tests pass; the only failure is a pre-existing third-party `openff.toolkit` import error reproducible without MolSysMT | `2de6b4d6d`; `archive/resolved_bugs/structural_attribute_resolution_ignores_the_structure_axis.md`; `archive/resolved_bugs/iterator_without_explicit_attributes_fails_for_partial_forms.md` |
| 2026-08-03 | `msm.info()` table styling in the built documentation | reported → `DONE`; no stage transition | compiled pages rendered `msm.info()` flat while the notebooks stayed striped. `info()` returns a `Styler`, which emits no HTML class, so it was styled only by MyST-NB's class-agnostic pandas rule — dropped in v1.4.0, the dark-mode rework — while pydata-sphinx-theme reaches notebook tables solely through `table.dataframe`. `info()` now tags the table `dataframe`, the class `DataFrame.to_html()` emits, which restores striping in both themes and removes a dark-mode fallback that painted the output as an inverted light box. Verified on a rebuilt page: all 8 tables of `info.ipynb` emit the class under `.bd-content` → `div.cell_output`, with the striping now coming from the theme alone. A CSS override and pinning `myst-nb<1.4` were both rejected as patches; a stable `Styler` uuid was rejected because no library-side value is both stable and unique — 5 of 62 notebooks hold two identical tables by design. `docs/execute_notebooks.py` keys staleness off notebooks, never the library, so the remaining 61 need an explicit force | `d92d4fe76`; `archive/resolved_bugs/docs_styler_zebra_striping_lost_with_myst_nb_1_4.md` |
| 2026-07-31 | `MolSys → ViewerJSON` deep-copy defect | reported → `DONE`; no stage transition | the conversion read two fresh, local, discarded intermediates through the deep-copying default of `ViewerJSON.to_dict()`, spending about 93% of its time in 1,350,867 `deepcopy` calls; reading them with `copy=False` takes the reported 62-atom × 5,000-structure case from 1.67 s to 0.32 s. Neither intermediate aliases the source, so the copy protected nothing: a non-aliasing regression test mutates the returned payload and asserts the source `MolSys` and a second conversion are untouched, and it stays green with `copy=True` restored while the timing regresses to 1.58 s. The `ViewerJSON` identity conversion was audited and deliberately left deep-copying: it is unreachable from this chain. 508 viewer, form, view and cross-repo tests and Ruff pass | `b63a2f6c5`; `archive/resolved_bugs/viewer_json_conversion_deep_copies_twice.md` |
| 2026-08-07 | Fast release gate | `FAIL` (11/12) → `PASS` (12/12); no stage transition | the developer-guide gate had been red since the documentation queues were reorganized: `devguide/README.md` still linked the deleted `docs/README.md`, and `forms_and_conversions.md` and `pending_proposals/docs/README.md` both linked a proposal that `ae29169e8` had archived. The archiving was correct — the *Multiple items into one* section of `convert.ipynb` now composes a PSF topology with a DCD trajectory and states that the multi-structure item dictates the structure axis — but its two referrers were never updated, and the empty `devguide/docs/` tree was left behind. This ledger's previous claim that the gate passed 12/12 was measured before that reorganization | see the commit closing this row |
| 2026-08-07 | `file:prmtop → molsysmt.MolSys` | reported → `DONE`; no stage transition | the converter imported a `to_molsysmt_Structures` sibling that never existed in the form package. The name was unused — the body builds an empty `Structures()` because a prmtop carries topology only — but the import runs at call time, so the library's central form was unreachable from an entire input format, and MolSysViewer failed the same way. Conversions register in `_convert_to` as function objects and their inner imports are function-local, so the catalogue proves only that `to_*.py` imports; nothing calls every registered edge. The sweep that found it is now `tests/form/test_converter_imports_resolve.py`, carrying the two remaining cases as a baseline that cannot grow, and the conversion is guarded by `tests/form/file_prmtop/test_to_molsysmt_MolSys.py`. 115 supported, conversion-truth and form tests pass; fast gate 12/12; Ruff clean | see the commit closing this row |
| 2026-08-07 | Presentation and citation surface | two of three items `PENDING` → `DONE`; no stage transition | maintainer decisions taken and applied. Daniel Ibarrola-Sánchez is not an author: removing him from `CITATION.cff` also removes the ORCID that file attributed to him but which belongs to Diego Prada-Gracia, and the record now agrees with `.zenodo.json` on the same two authors and with the README, which acknowledges his contributions to MolSysMT's early development. The unreferenced duplicate landing page `docs/content/user/index_v2.ipynb` is deleted with its two `nbconvert` artifacts, verified to have no inbound reference from any page; three further orphans of the same `_v2` experiment are recorded in the proposal. The DOI, version, title and date are decided but deferred: `CITATION.cff` is a placeholder until 1.0 closes, and the update is now a line in the release-gate sign-off so it cannot drift again as it did for two years. Item 3, the timing of the Conda installation instructions, stays open | see the commit closing this row |
| 2026-08-07 | Atom-axis `add()` semantic audit | Phases 1-3 `PENDING` → `DONE`; Phase 4 open; no stage transition | Phase 1 audited the contract read-only and measured every claim with a probe. It found the scope far narrower than assumed — only `molsysmt.MolSys` and `molsysmt.Structures` implement `add()`, and the dispatcher selects on the target form — and it found most of audit question 1 unreachable, because digestion rejects a list of independent molecular systems before the target × source loop can run. Two of the audit's own premises were wrong: adding a topology-only source does not drop the coordinates, it fails first with an `ArgumentLengthError` naming an argument the caller never passed; and the one list that survives digestion is a composite system, which `add` iterated as independent sources, contradicting the composite contract. Phase 2 landed the regression matrix with the decisions as `xfail(strict=True)`, which is also how a cross-cutting defect surfaced: a test asserting `add()` honours `attribute_policy` passed against a function with no such parameter, filed as `pending_bugs/public_functions_silently_ignore_unknown_keywords.md`. Phase 3 implemented D1-D7 and the four defects: the target's box prevails with `IncompatibleBoxWarning` (MSM-WARN-STRUCT-007), `temperature` and the energies are dropped while `structure_id`, `time` and `time_step` survive, `attribute_policy` gains `intersection`/`strict`, bioassemblies merge on the chain axis with `BioassemblyIdentifierCollisionWarning` (MSM-WARN-STRUCT-008), `alternate_location` merges with remapped atom indices, `atoms_ff` follows the policy, and `add()` is one-to-one with the loop deleted. 40 add tests pass with no pending markers; 886 basic, native and element tests pass; the contract is now in `native_structures_contract.md` | see the commit closing this row |
| 2026-08-07 | Atom-axis `add()` semantic audit | Phase 4 `PENDING` → `DONE`; proposal archived; no stage transition | the lifecycle closed and all ten acceptance criteria hold, so the proposal and its Phase 1 findings moved to `archive/resolved_proposals/`. `molsysmt.basic.add` documents `attribute_policy` and the four Notes that changed; the User Guide page gained two sections and a warning admonition, written against a real case rather than an illustrative one — T4 lysozyme from a PDB carries B factors and a unit cell, a built peptide carries neither, so one addition exercises the drop and both new diagnostics — and the notebook was re-executed so its printed outputs are measured. Common Core modules 17 and 18 needed no correction: they already use one target and one source. Writing the documentation surfaced a diagnostic defect of its own, a doubled period in the `strict` rejection message, fixed at both call sites. Two coverage gaps found while walking the criteria were closed rather than waived: `velocities` joined the one-sided parametrisation, and a string selection over an assembled composite source is now pinned. 43 add tests pass; Ruff, dependencies, devguide and course gates green; fast release gate 12/12 | see the commit closing this row |
| 2026-08-07 | Public argument contract | reported → `DONE`; no stage transition | a typo in a keyword argument was silent in 22 of the 26 public callables and uncatalogued in the other four: `structure_indeces` for `structure_indices` returned all 5,000 structures of a trajectory instead of the three requested, with a well-formed result and no diagnostic. The cause was a binding step making a policy decision — ArgDigest discarded any keyword outside the signature before the layer designed to judge it could see it — which left it more permissive than Python itself, and left MolSysMT's own `STRICTNESS='warn'` policy unreachable for those 22. Fixed upstream in ArgDigest 0.10.0 by adding the missing axis, the function argument contract, and declared here with three configuration lines, one domain pointing at the attribute catalogue, and two contract modules; the 19 closed signatures are protected with no declaration at all. Two claims in the original triage were wrong and are corrected in the archived report: `contains` and `is_composed_of` implement deliberate no-criterion branches, so no `requires_any_of` rule was declared. Reading those bodies found a real defect instead — `get_label` declares `**kwargs` and never reads it. `molsysmt.basic.convert` keeps the permissive default because its domain resolves from `to_form` at call time; the gap is recorded and pinned by a test. ~8300 tests pass with the policy at `error`, plus 1296 MolSysViewer tests with nothing declared on its side; Ruff clean; fast release gate 12/12 | see the commit closing this row; `archive/resolved_bugs/public_functions_silently_ignore_unknown_keywords.md` |
| 2026-08-07 | Cross-repo test drift | reported → `DONE`; no stage transition | two tests in `tests/molsysviewer_molsysmt/` read `MolSysView._message_history`, a private attribute MolSysViewer replaced with a narrower `_shape_history` and a `scene_history` model, so the suite carried two known failures — and a suite with known failures stops detecting new ones, which blocks the F5 exact-commit gate. Both tests already intercepted `apply_system_edit` and recorded the edited molecular system, then ignored it to inspect the message the viewer built from it. That was the defect the refactor exposed: what the facade owes the viewer is an edited system handed to `apply_system_edit`, and how the viewer serializes it afterwards is not this side's business. They now assert on the recorded system. Renaming the attribute to `_shape_history` was deliberately not done: it is not the same thing, so the tests would have passed asserting something else. 115 cross-repo tests pass and the MolSysMT suite is clean | see the commit closing this row; `archive/resolved_bugs/cross_repo_test_reads_a_removed_molsysviewer_attribute.md` |
| 2026-08-12 | Pre-F5 adapter and course consolidation | no stage transition; candidate base ready | comparison now treats incompatible shapes as unequal; OpenFF unit adapters coexist safely; PyTraj trajectory conversion preserves its supported contract; OpenMM simulations are built only from complete inputs and initialize from the selected structure; every registered converter module resolves; conversion fidelity advances to 40 exhaustive / 441 accepted / 29 resolved with zero new debt; the Common Core is fixed at 20 modules and all labels match permanent manifest identities with no validator exception. The fast gate passes 12/12, Ruff is clean, form adapters pass 89/89 with 78 accepted lower-tier declarations, and the course contract passes 156/156 notebooks | `3fb639010` through `c87a14036` |
| 2026-08-12 | F5 exact-commit release gates | `IN PROGRESS` → `DONE`; weighted closure 96% → 99%; F6 becomes active | exact commit `8faf62785` passes the fast gate 12/12; full matrix run `31589594289` passes Ubuntu and macOS on Python 3.11--3.13; wheel run `31589594286` passes supported Linux/macOS builds, abi3 Python/NumPy compatibility, installed public smoke, sdist, Rust quality and security, with Windows green as experimental evidence; documentation run `31589594273` and smoke run `31589594438` pass. Packaging defect #145 and clean-source CI defect #146 satisfy their acceptance criteria and are archived | `8faf62785`; `archive/resolved_bugs/built_wheels_omit_the_dynamic_form_catalogue.md`; `archive/resolved_bugs/ci_shadows_the_installed_rust_extension_with_the_source_checkout.md` |
| 2026-08-13 | Bounded pre-1.0 corrections | F5 `DONE` → `IN PROGRESS`; weighted closure 99% → 96% | the declared selection syntaxes become an executable directional contract, large molecular strings no longer enter unbounded filename tokenization, and the stale `_private` API branch is removed from the published reference. Focused and expanded guards pass; a new exact-commit release campaign is required before F5 can close again | `d5b066a35`; uibcdf/molsysmt#148, #149, #150 |
| 2026-08-13 | Generated form-function identity | reported → `DONE`; no stage or weighted-progress transition | nine `exec()`-based getter modules created 2,162 distinct decorated functions without `__module__`, so ArgDigest received `None.<name>`, caller-specific contracts could not identify them, and diagnostics named no resolvable origin. Each generator now seeds `__name__` before decoration; exact module identity, structured diagnostics, and future generators are guarded. The passport decision remains independent and untouched | `5412489c9`; uibcdf/molsysmt#152 |
| 2026-08-13 | Retired ArgDigest passport dependency | reported → `DONE`; no stage or weighted-progress transition | the only `ValidatedPayload` issuance path and its paired trusted-array branch were unreachable: 13,319 distinct decorated callables and the instrumented full suite produced no caller under `molsysmt.lib.*`. Both branches, the import, and the obsolete sandbox are removed without replacement; active rules use ordinary digestion or explicit caller-owned `skip_digestion=True`. The complete 372-test private-digester surface passes against both the pre-removal ArgDigest tree and `refactor/remove-the-passport` with `argdigest.core.contract` absent; fast release gate 12/12 | `2eca46926`; uibcdf/molsysmt#153; `tests/_private/argdigest/test_no_validated_payload.py` |
| 2026-08-13 | Pre-1.0 scope freeze | no stage or weighted-progress transition; F5 remains active | uibcdf/molsysmt#151 remains a post-1.0 expert-interface proposal: automatic detection is already bounded and safe, no post-fix end-to-end speedup has been measured, and adding a public signature plus unresolved heterogeneous-list semantics would expand rather than stabilize the candidate. No further implementation item is admitted before the exact-commit campaign | `pending_proposals/add_an_explicit_source_form_hint_to_convert.md`; checkpoint commit following `2eca46926` |
| 2026-08-13 | Boundary-digestion re-audit | uibcdf/molsysmt#147 withdrawn; no stage or weighted-progress transition | instrumentation distinguishes 21 ordinarily digested calls from 568 fast-path calls in the representative viewer action: all 510 form-level `has_attribute` calls already use `skip_digestion=True`, perform zero molecular-system assessments, and forcing the bypass changes 46.62 ms to 46.82 ms. The original 29 ms diagnosis is refuted. The two real findings are separated into uibcdf/molsysviewer#32, where operation-local inventory reuse measures 46.71 ms → 26.62 ms, and post-1.0 uibcdf/molsysmt#154, where one direct public predicate performs four assessments | `archive/withdrawn_bugs/boundary_digestion_on_internal_predicates.md`; checkpoint commit before F5 |
| 2026-08-14 | F5 controlled sibling alignment | remains `IN PROGRESS`; no weighted-progress transition | public metadata advances to ArgDigest `>=0.12.0` and PyUnitWizard `>=0.24.0`; controlled workflows pin their immutable release commits and the already-tested MolSysViewer commit; a clean Python 3.13 Conda environment resolves ArgDigest 0.12.0, PyUnitWizard 0.24.0, SMonitor 0.12.0, and DepDigest 0.10.1 from channels and imports them from `site-packages`; 17 focused workflow, receptor, and fast-path tests pass | candidate-preparation commit following `eca56ef1d` |
| 2026-08-14 | F5 exact-commit recertification | `IN PROGRESS` → `DONE`; weighted closure 96% → 99%; F6 becomes active | exact commit `38ab61f6e` passes the fast gate 12/12; smoke `31781199983` and documentation `31781220979` pass; wheel run `31781218931` passes 28 jobs covering supported Linux/macOS artifacts, installed Python 3.11--3.13 checks, NumPy floors, sdist and Rust quality, with Windows retained only as non-blocking experimental evidence; full matrix `31781216880` passes all six Ubuntu/macOS Python 3.11--3.13 cells | `38ab61f6e`; post-gate status checkpoint |
| 2026-08-14 | F6 citation and preservation preparation | remains `IN PROGRESS`; weighted closure stays 99% | the existing MolSysMT concept family `10.5281/zenodo.1298752` is verified through its 0.12.0 record; every current public surface uses that concept DOI; `CITATION.cff` and `.zenodo.json` agree; the old MolModMT DOI is removed; release preparation, offline validation, and post-release Zenodo verification are executable and documented for reuse across MolSysSuite; four focused tests, Ruff, devguide, and the expanded fast gate 13/13 pass; exact final commit gates, tag, GitHub Release, and 1.0.0 version DOI remain | dirty F6 candidate based on `503612269`; `release_and_citation.md` |
| 2026-08-14 | Public MolSysSuite alias contract | uibcdf/molsysmt#157 `OPEN` → `DONE`; no stage or weighted-progress transition | `molsysmt.attribute.get_argument_aliases()` exposes schema-versioned defensive-copy plain data for attribute synonyms and explicit element-dependent short names; MolSysMT derives its own caller-scoped ArgDigest tables from that source; MolSysViewer removes both private imports while preserving its `viewer`, `Region`, and `Whole` behavior. The User Guide and Common Core module 8 reflect the alias contract and both notebooks execute. 119 MolSysMT tests, 23 focused MolSysViewer tests, Ruff, dependency/devguide/course/API validation, and the fast release gate 13/13 pass; MolSysViewer's full suite has 1609 passes, four accepted skips, and one unrelated pre-existing documentation failure from deprecated `add_label()` usage | closing commit for uibcdf/molsysmt#157; `archive/resolved_proposals/public_alias_contract_for_molsyssuite_consumers.md` |
| 2026-08-14 | Alias-collision downstream guard | ArgDigest runtime fixed; no weighted-progress transition | ArgDigest now rejects alias-plus-canonical and multi-alias target collisions before normalization can discard a value. MolSysMT pins the public `get()` boundary, raises its wheel and Conda floor from `>=0.12.0` to the planned patch `>=0.12.1`, and records that the exact release candidate needs recertification after publication rather than accepting the known-bad release | downstream closure for ArgDigest commit `c46cd01`; `tests/attribute/test_argument_aliases.py` |
| 2026-08-19 | Public documentation audit & standardization pass | remains `IN PROGRESS`; blockers made explicit 2026-09-02 | Foundations, Tools (topology, structure, physchem, pbc, mm, nglview, openmm, tleap), Cookbook (all 9 recipes standardized with MolSysViewer static views), Showcase (all 6 notebooks compiled with matplotlib PNG display data, zebra tables, collapsible notes, and reconstructed NGLView representations/CDN configs), and Course (all 4 paths synchronized) pass with clean Sphinx HTML builds (`make -C docs html`) and Ruff. The `About` positioning and index were already rewritten in `d2b805e74`, and its citation lifecycle was prepared in `d35dc33b1`; final sign-off remains open for two named reasons: the Conda installation claim does not hold on supported Python 3.13 (uibcdf/molsysmt#195), and the exact 1.0 citation remains part of F6 release publication | `3bee6f054`, `d2b805e74`, `d35dc33b1`; uibcdf/molsysmt#195; `release_and_citation.md` |
| 2026-09-02 | Stable API docstring integrity | uibcdf/molsysmt#187 `OPEN` → `DONE`; no stage or weighted-progress transition | the validator now rejects empty descriptions, parameter-name restatements, the generated return placeholder, and non-informative `object` parameter types on the stable surface; 205 parameter entries across 60 stable functions now carry concrete types and operational descriptions; mutation guards pass 10 tests, all 27 affected doctests pass, Ruff is clean, and the fast release gate passes 13/13. Scientific-evidence execution and devguide-guard relevance remain open as uibcdf/molsysmt#196 and uibcdf/molsysmt#197 | `350a7e866`; `archive/resolved_bugs/validators_that_check_form_instead_of_intent_admit_conforming_emptiness.md` |
| 2026-09-04 | Native Conda ABI3 publication | uibcdf/molsysmt#202 `OPEN` → `DONE`; no stage or weighted-progress transition | the shared action no longer renders each recipe twice, and MolSysMT now builds one CEP 20 ABI3 artifact on each native platform instead of recompiling for every supported Python minor. Five platform artifacts execute under all fifteen platform/Python 3.11--3.13 cells; production run `33849332945` publishes all five build-2 artifacts to staging in 19:56, with independently verified ABI3 channel metadata. Production staging/release selects the proven ABI3 recipe, while the coordinated installation gate remains 5 × 3 | `e5820d479`; uibcdf/molsysmt#202; `archive/resolved_proposals/build_one_abi3_conda_artifact_per_native_platform.md` |
| 2026-09-19 | Scientific evidence execution | uibcdf/molsysmt#196 `OPEN` → `DONE`; no stage or weighted-progress transition | the fast validator now certifies registry structure without claiming that pytest ran; the separate heavy gate executes exactly all 47 registered nodes, rejects collection failures and skips, and emits a commit- and environment-bound JSON certificate. The current registry produces 54 parametrized cases, all passing with zero skips; workflow-contract and Scientific Truth validation pass 119 tests, the complete suite passes 10,211 with 11 unrelated dependency skips, and the fast gate remains 13/13. `ci-full` and `ci-weekly` retain one clean-source certificate per matrix cell | closing commit for uibcdf/molsysmt#196; `archive/resolved_bugs/scientific_evidence_registry_accepts_tests_that_were_never_executed.md` |
| 2026-09-19 | Form extraction dispatch | uibcdf/molsysmt#210 `OPEN` → `DONE`; no stage or weighted-progress transition | all 89 form adapters now accept the extraction dispatcher contract with no debt exception; both mechanics forms preserve global settings and subset their conditional per-atom force-field axis; three-letter sequences extract residue positions while retaining the group-indexed converter contract; invalid axes and positions raise catalog errors instead of Python signature/index errors. The adapter census passes 263 tests with two accepted PyTraj skips, the complete suite passes 10,217 with 11 accepted dependency/environment skips under 12 workers, Ruff is clean on every changed Python file, and the fast gate remains 13/13 | closing commit for uibcdf/molsysmt#210; `archive/resolved_bugs/three_forms_declare_an_extract_the_dispatcher_cannot_call.md` |
| 2026-09-19 | Test-suite runtime proposal | uibcdf/molsysmt#122 one-line fixture request → measured profiling proposal; no stage or weighted-progress transition | an accidental serial run reached only 3,793/10,228 executed nodes in 760.75 seconds before interruption, while the documented `-n 12 --dist loadfile` mode completed all 10,228 in 377.90 seconds. The proposal now requires cold/warm profiles, node/module cost attribution, preservation of executed scientific and contract evidence, mutable-fixture isolation, and separate wall-time versus aggregate-work measurements before optimizing | `pending_proposals/profile_and_reduce_test_suite_runtime_without_weakening_coverage.md` |
| 2026-09-19 | Shared guard governance | uibcdf/molsysmt#197 `OPEN` → `BLOCKED` by uibcdf/molsyssuite#26; no stage or weighted-progress transition | the originating MolSysMT defect exposed incompatible guard semantics across all six wave-1 repositories. MolSysSuite now owns the shared addressability, reviewer-relevance, pytest/non-pytest, migration, and rollout decision; #197 is narrowed to MolSysMT's eventual implementation and must not create a competing local policy | central record in uibcdf/molsyssuite#26; `pending_bugs/devguide_closure_accepts_guards_unrelated_to_the_reported_defect.md` |

## S6 source recovery and delivered Viewer candidate — 2026-10-06

The source matrix `37441978743` at `5bd893c85` finishes **failure**: Linux
and macOS Python 3.11 pass; the other six cells each fail only
`tests/basic/test_copy.py::test_copy_1`. Matching undefined chain types become
numeric NaN arrays under pandas 3, and the comparison's numeric branch reports
inequality even for self-comparison. #345 owns the reproduced defect.
All eight registered scientific certificates pass 54 cases with zero skips.
The [recovery receipt](../devtools/data/stabilization_s6_source_recovery_20261006.json)
preserves exact counts, warnings, omissions and original log identities.
Ordinary full-suite omissions are 26 Linux/27 macOS skips and 40 deselections
per cell; the next workflow retains complete JUnit to inspect their reasons.

The correction passes the same 61 compare/copy cases under pandas 2.3.3 and
3.0.6, and the comparison doctest. Public metadata equality now accepts matching
missing numeric entries while rejecting a populated entry in their place.
Ruff passes; the tutorial and course explanations are synchronized. The new
source matrix must execute before treating this correction as full qualification.

The Viewer team delivers stable source
`c046fca173f501c6e259761ef8f3d6b1825f17e8`, tested against MolSysMT
`5e2721691b6a3c175406a8e4c0926dfb7b160671`. It reports Python 3.14 counts
of 2,819/2,792/2,793 passed and 27/54/53 skipped on Linux/macOS/Windows,
with no failures, plus all 39 core browser suites and 17 interaction calculation
forms. Those are consumer observations, not our re-execution. GitHub confirms
the source SHA, and inspection confirms its later `e71eaf63` change is
documentation only. Routine Viewer source routes and upcoming exact-source
inputs select `c046fca...`; their dependency contract audit passes.

This makes a fixed current Viewer candidate available for staging preparation.
It does not qualify the newer corrected MolSysMT pair, Conda-installed files,
Windows artifact compatibility or publication. Preserve both immutable
producer identities and build/file digests in the upcoming installed-pair
gates. Release tag and GitHub Release approval remain separate.

## Next version checkpoint: 0.23.0 — 2026-10-06

The maintainer selects **0.23.0**, rather than 1.0.0, for the next pre-1.0
package checkpoint. The [frozen scope](release_1_0_scope.md#pre-10-version-checkpoint)
continues to admit stabilization fixes and required qualification only.
Use this version to validate packages and the MolSysViewer integration; decide
on 1.0.0 after reviewing that evidence and the remaining acceptance criteria.

Existing source/wheel receipts retain their original producer identities and
development versions. They do not certify packages labelled 0.23.0. No new tag,
release or staging upload is performed by this decision, and citation metadata
still describes the published 0.22.4 release. The exact 0.23.0 producer and the
paired Viewer package version remain to be selected before staging.

## Corrected current source pair — 2026-10-06

MolSysMT `bb4781c5ae0b725d0c904cfd8bae1f44a1b13123` and delivered Viewer
`c046fca173f501c6e259761ef8f3d6b1825f17e8` pass source run
[37449282864](https://github.com/uibcdf/molsysmt/actions/runs/37449282864):
all eight Linux/macOS Python 3.11–3.14 full cells succeed. Each Linux cell
passes 13,290 cases with 26 skips; each macOS cell passes 13,289 with 27 skips.
Every cell has 40 deselections, retained separately from JUnit, and all eight
scientific certificates pass 54 cases without skips. #345 is resolved with its
[missing-metadata regression guard](../tests/basic/compare/test_compare_extended.py)
and [archived diagnosis](archive/resolved_bugs/comparison_rejects_identical_undefined_metadata_under_pandas_3.md).
The original failed source matrix remains recorded.

Wheel run [37449284817](https://github.com/uibcdf/molsysmt/actions/runs/37449284817)
passes all thirty applicable jobs, with one expected PR-only skip. Rust quality
checks and 81 native tests, four wheel builds, sixteen current-NumPy runtime
cells, four NumPy-floor cells, four public installed smokes and the sdist
round trip pass. The
[pair receipt](../devtools/data/stabilization_s6_pair_20261006.json)
retains official results, five artifact/file identities and independently
hashed bytes, eight JUnit results and their skipped nodes/reasons.

This completes the corrected source/wheel checkpoint. These artifacts carry
development version `0.22.4+217.gbb4781c5a`, not 0.23.0. Select and qualify
the actual 0.23.0 package candidate and paired Viewer package version next.
Conda-installed pair, consumer-owned installed/browser/session acceptance,
exact documentation and publication gates remain. No public release is inferred.

The committed Conda route and MolSysMT dispatch defaults now select 0.23.0,
with exact-file promotion after the installed-pair gate. The guarded route
rejects a different version. This prepares the next operation without uploading
packages or changing the published citation metadata. The new Viewer package
version still needs its owner's decision; its historical 0.23.4 dispatch default
is not a selection for this new pair. Pass the agreed versions explicitly.
The five existing route/promotion guards pass in the shared Python 3.14
environment (twelve workers, receptor `llm`, 3.98 s); Ruff, developer-guide
validation and whitespace checks pass. This is scoped route validation,
not another full-suite or installed-package qualification.


## Coordinated interaction query vocabulary — 2026-10-06

uibcdf/molsysmt#346 implements the approved provider counterpart of
uibcdf/molsysviewer#168: `involving_selection`, `within_selection`,
`across_selection_boundary`, and the separate `between_selections` operation.
Legacy query values and `between` remain compatible. Scientific calculation
scope and H5MSM/InteractionsDict schemas are unchanged; the
[normative contract](interactions_query_semantics.md) defines the migration boundary.
The [provider report](archive/resolved_proposals/coordinate_explicit_interactions_selection_query_names.md)
records 1,474 passing scoped tests, eight passing doctests and executed public
examples. Consumer migration remains Viewer-owned. Prior full source/wheel
qualification retains its original producer; it does not certify this new source
or a 0.23.0 artifact. The exact-candidate gates under #334 remain pending.


### Maintainer clarification: use only explicit query names — 2026-10-06

The maintainer withdraws the initial compatibility spellings in #346 before
public adoption. The canonical query names and `between_selections` are the only
supported query API; detector and persisted scientific scope remain unchanged.
The current Viewer checkout still passes `incident` by default, and its existing
real-consumer attribution/session regression fails at that query call. Keep the
regression intact and qualify it again after uibcdf/molsysviewer#168 migrates the
consumer. Prior source-pair evidence does not certify this revised provider API;
the new provider contract and the migration requirement must accompany its source
handoff. No format bump or release publication is implied.


## Released support providers for the next checkpoint — 2026-10-06

The maintainer reports the public SMonitor 0.19.0 and ArgDigest 0.15.0 releases;
the GitHub release records are verified as published, non-draft releases.
`devtools/controlled_sources.txt` now fixes their exact release commits:

- SMonitor 0.19.0: `f604b940ab281df4554869fdd24f796ea6d42c27`.
- ArgDigest 0.15.0: `57447cc4ec1f7ce85078f8a939892efd075bc919`.

The shared Python 3.14.7 environment already contains SMonitor 0.19.0 and
ArgDigest 0.15.0+1.g5c6711e; the latter's runtime source has no changes from the
release tag. Existing argument-digestion, exception/warning, catalog, cross-provider,
interaction-query and dependency-audit guards pass **776 tests in 20.33 s**,
with zero failures/errors/skips and three historical H5MSM migration warnings:

```bash
python -m pytest tests/_private/argdigest tests/_private/smonitor \
  tests/_private/test_smonitor_catalog_integrity.py \
  tests/cross_repo/test_smonitor_contracts.py \
  tests/cross_repo/test_diagnostics_noise.py \
  tests/interactions/test_argument_validation.py \
  tests/interactions/test_public_molsys_h5msm_workflow.py \
  devtools/tests/test_audit_dependency_contract.py \
  -n 12 --dist loadfile --receptor=llm
```

The dependency audit and **14/14 fast gates** also pass. The
[bounded receipt](../devtools/data/support_provider_releases_20261006.json)
retains the pins, actual development versions, scope and JUnit hash under #334.
Public floors remain `argdigest>=0.13.0` and `smonitor>=0.16.0`; source qualification
and minimum supported versions are separate contracts. No new restricted-capture
or explicit-digestion feature is adopted by this pin update. That provider
coordination remains uibcdf/molsyssuite#106. These checks do not qualify exact
installed release artifacts or the full provider/Viewer pair, and do not change
the pending Viewer query migration in uibcdf/molsysviewer#168.


## Selected pre-1.0 package pair — 2026-10-06

The maintainer selects **MolSysMT 0.23.0 / MolSysViewer 0.24.0**. The agreed
Viewer source is `5bb59c0e13045ee0aaf34cf336a3533d611197bf`; routine source
pins and the installed-pair workflow now use this source and version. The
committed Conda route remains staged. Build defaults are zero; the actual
Viewer build coordinate must be read from its producer receipt.

The real Viewer attribution/session regression that previously failed on the
withdrawn `incident` query now passes, together with public MolSys/H5MSM and
named-analysis persistence tests: **35 passed, zero failures/errors/skips**.
Release preparation and dependency-route guards pass **25 tests**. The first
route check caught four stale workflow copies of the old Viewer SHA; the
corrected pin passes the dependency audit and **14/14 fast gates**. The
[candidate preparation receipt](../devtools/data/stabilization_023_candidate_preparation_20261006.json)
retains scope, JUnit digests, initial failure and remaining qualification.

The local Sphinx HTML build succeeds. It reports **784 warnings**, matching
the earlier S5 build count, with zero course references to nonexistent
toctree documents. The warning debt remains tracked by uibcdf/molsysmt#144;
a successful build is not a warning-free documentation claim.

Viewer source CI [37530734789](https://github.com/uibcdf/molsysviewer/actions/runs/37530734789)
has completed successfully on Linux, macOS and Windows at
`a48478fcab579095ed6eb7ab2a3620cc8fb3a8df`. Git inspection confirms that the
selected 5bb59c0e source adds documentation/evidence only. This distinction
does not imply an exact-5bb CI execution. The two experimental Qt failures
reported by the Viewer team remain owned by uibcdf/molsysviewer#109.

The standard release preparation tool updates candidate citation surfaces to
0.23.0, dated 2026-10-06. This prepares metadata; it does not publish the
version. Read-only registry preflight found neither selected version present;
that observation must be refreshed before producing or uploading artifacts.
Four untracked Viewer sandbox artifacts are preserved and excluded from the
committed source identity. The Viewer Conda recipe derives its version from
the ephemeral tag. Its committed release plan still selects historical
0.23.4 and needs its owner's 0.24.0 update before its package producer runs.

Full exact-candidate source/native gates and the sixteen installed-pair cells
remain required. Filenames, SHA-256 values and availability on
`uibcdf/label/staging` must be obtained from actual producer files. No public
tag, GitHub Release, registry upload or promotion is performed by this
preparation. Installed/browser/session acceptance remains Viewer-owned under
uibcdf/molsysviewer#93 and uibcdf/molsysviewer#114.

The prepared source candidate is
`46ef28eb60a258aa77d82ff1bc39ee0d1591e3c9`. Its clean-source scientific
certificate passes **54/54 cases for 47 registered nodes**, with zero
failures/errors/skips. All **26 basic doctests** pass with network access;
the first sandbox attempt failed two RCSB-download examples on DNS resolution
and is retained in the receipt. Source matrix
[37534217132](https://github.com/uibcdf/molsysmt/actions/runs/37534217132)
and native wheel matrix
[37534219155](https://github.com/uibcdf/molsysmt/actions/runs/37534219155)
are dispatched against this exact commit and the selected Viewer source.
They remain in progress; the larger local editable-source suite is also
running. Later evidence-only commits do not reselect that producer or qualify
unfinished gates.

The maintainer explicitly authorizes building and uploading the four ABI3
Conda files for **0.23.0, build 0**, from that exact candidate. A fresh
read-only registry preflight confirms that neither selected version is yet
present. Staging producer
[37534744593](https://github.com/uibcdf/molsysmt/actions/runs/37534744593)
is dispatched for `linux-64`, `linux-aarch64`, `osx-arm64` and `win-64`, targeting
`uibcdf/label/staging`. Dispatch is not production or upload verification;
no package file identity is reported before inspecting actual bytes. The
public tag, GitHub Release and main-label promotion remain separate gates.


### Staging files ready for the Viewer handoff — 2026-10-06

Producer 37534744593 completes successfully on all four native platforms.
**MolSysMT 0.23.0, build 0**, from
`46ef28eb60a258aa77d82ff1bc39ee0d1591e3c9`, is available on
`uibcdf/label/staging`. The
[handoff receipt](../devtools/data/stabilization_023_staging_handoff_20261006.json)
records every filename, build string and SHA-256. Producer receipts, registry
metadata and hashes computed from downloaded bytes agree. ABI3 metadata and
seven core source files are verified against the original candidate; Windows
checkout CRLF is the only source-text normalization needed.

MolSysViewer can declare **`molsysmt>=0.23.0`** for the agreed Interactions,
H5MSM 0.5 and coordinated loading/box capabilities. This selects the first
candidate package delivering the current coordinated contract. It does not
declare the experimental interaction contract stabilized or waive installed
consumer qualification.

Importing both MolSysMT and its Rust extension from the actual extracted Linux
Conda payload reports version 0.23.0. Public H5MSM/MolSys, named interactions
and the real Viewer attribution/session regression pass **35 tests** using
that payload in the shared Python 3.14 environment. This is artifact runtime
evidence with shared dependencies; the clean sixteen-cell installed pair
remains required.

The standalone ABI3 validator rejected the correct Python range because it
still expected `<3.14`. uibcdf/molsysmt#347 corrects the tool to compare against
the public project range and adds guards; **13 tests** pass. No package bytes,
build coordinates or producer are changed. The subsequent **14/14 fast gates**
pass. Native wheel run 37534219155 passes thirty jobs with one expected PR-only
skip.

The larger local run records **13,561 passed, 16 failed, 17 errors and two
skipped**, with all 33 unsuccessful cases affected by sandbox DNS restrictions.
Repeating those exact cases with network access on unchanged runtime source
passes **33/33**. Combined outcomes are 13,594 passes and two skips; the receipt
retains the original unsuccessful invocation rather than claiming a second
complete green run. The two omissions are the RDKit-absent alternative test
in an environment with RDKit and the unavailable optional CuPy form.

The eight-cell exact-source matrix is still running. MolSysViewer must provide
its exact 0.24.0 staging file/build/hash before the sixteen-cell installed pair
can run. Public tagging, Release publication and promotion remain pending;
the available files support the next consumer qualification step.
