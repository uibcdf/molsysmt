---
summary: Form tutorial API roles render as unlinked code despite a warning-free build
issue: uibcdf/molsysmt#727
status: partial
opened: 2026-11-12
closed:
severity: medium
verification: reproduced
area: [docs]
guard:
normative:
blocked_by: []
supersedes: []
---

# Receiving actual form implementation links

## What

Native form tutorials use Python func/mod roles for adapter objects that have
no indexed Sphinx API target. Full strict HTML can finish with zero warnings
while those references render as unlinked code. Actual compiled MolSys,
Topology and Structures operation/conversion tables show this defect. Link
inspection that considers only existing hrefs cannot detect missing intended
links, even when every link it sees resolves.

## How

Complete HTML on 1b98c2b1d and targeted MolSys receiving on 2bf21835f finish
with zero warnings. Inspect actual article tables: their implementation and
converter references have code.xref elements without enclosing anchors.
The source objects exist; their existence is different from a rendered link.
The bounded #725/#726 article proof remains valid for its 130/16 actual local
destinations, not for unlinked intended API references.

## Why

Users cannot follow the advertised API/implementation references. A good guard
must check the intended references, not accept an empty/partial set merely
because the existing links resolve. This is owning documentation/indexing debt,
not a demonstrated Sphinx provider bug or a scientific/runtime failure.

## Partial correction and acceptance

The MolSys tutorial now replaces all 57 role occurrences with clearly labelled
links to immutable published owning source/docstrings. Every operation/module
and registered conversion route must retain its real source destination; this
is not a new placeholder API page. Keep general user APIs linked to indexed
Sphinx targets. Runtime attribute/delivery, H-count semantics and bond ownership
retain #726's separate guards. Actual HTML must contain every intended source
link and no unlinked adapter role; source/reference existence alone is insufficient.

Topology and Structures retain this unlinked-reference debt; the wider form
inventory is not yet audited. Continue per-form review before claiming full
closure, respecting live route limits, source identities, supported signatures,
conversion declarations and notebook code/output preservation. No shared guide,
provider, dependency floor, scientific algorithm or release is changed.

## Evidence and next action

Private before-DOM counts, exact role/source map and corrected source/HTML
receiving belong to the #725/#726 combined receipt. Its declaration-only source
checks do not claim installed/provider execution for every optional converter.
Close this issue only after the remaining intended form references are audited
and repaired or explicitly scoped with an owned disposition.


## Received MolSys increment — 2026-11-12

Clean 115ebe335 receives the final native MolSys article with zero warnings,
57 intended reference occurrences and 55 distinct real published source files.
The actual DOM has 14 operation and 40 converter links, no unlinked Python
roles and all 16 existing local destinations. Earlier three foundation articles
remain unchanged. Five source/semantic controls pass. The earlier strong guard
also exposes six undocumented converter routes, now corrected under #726.
See the [combined receipt](../../../devtools/data/native_domain_documentation_receiving_725_726_20261112.json).
Topology and Structures still need intended-link correction, and the wider
form scope remains unaudited. This report therefore stays partial.


## Topology and Structures source receiving — 2026-11-12

The next owner baseline has two failures and twelve passing controls. The
Topology failure concerns missing complete source links; Structures first
fails its route-set check because its MolSys embedding route is omitted.
The prior source-object existence check passes during this baseline, showing
why existence alone cannot establish link delivery. Earlier native MolSys
references and domain/availability controls remain received.

Topology now has explicit published-source references while preserving its
38 declarations, seventeen registered converters, unavailable hooks, chemical
separation and executable inventory example. Structures retains 22 declarations
and adds the already implemented MolSys embedding to list all seven converters;
that route does not invent Topology or ChemicalStates. Both notebooks preserve
all code, outputs, cell order and non-source metadata. General axis descriptions
use structures. Their 52 final reference occurrences cover the existing 51
roles plus the formerly omitted converter.

The existing MolSys and Topology guards now reuse one private test-only source
checker; it requires the reviewed operation inventory, every runtime-registered
converter, actual defining function/line and no unlinked adapter role in source.
An explicit non-default HTML guard separately requires every expected href in
the actual article and validates local destinations. This introduces no public
runtime API or provider dependency.

Fourteen corrected controls pass. The first expanded cohort has fourteen
passes and two test-draft failures: its coordinate edit passes a quantity as
the positional indices argument. ArgDigest correctly refuses it. Preserve that
draft and use the documented value keyword, retaining the intended geometry,
unit, order and independence assertions. The initial provisional pass sentence
was incorrect and is corrected before publication. Final expanded and actual
HTML receiving follow before claiming these checks or links delivered.

A complete source notebook census finds 94 pages/1,832 func/mod role occurrences
under the form-tool root. These include indexed generic user APIs; syntax alone
is not a rendered failure. Literal-file feasibility is similarly bounded: aliases
and generic API spelling can require different resolution, so its unknowns are
not declared missing implementations. Other form-reference scope remains owned
here, with real source/HTML matching still required before broader acceptance.


## Expanded source cohort received — 2026-11-12

The corrected sixteen-case cohort passes with unchanged selected inputs. Both
unit policies preserve the original coordinate/time values and selected source
axis order, keep topology/chemical states absent and detach coordinate edits.
The two initial test-draft rejections and their erroneous provisional note are
retained separately; neither is a product or provider failure. Actual HTML
receiving is still pending at this checkpoint.


## Native article delivery and remaining inventory — 2026-11-12

Clean e308832d8 passes strict targeted compilation of Topology/Structures with
zero warnings. The explicit three-case HTML guard passes on frozen before/after
article bytes: every native article has all intended hrefs, matching operation
and converter counts, valid local destinations and no unlinked Python role.
Across MolSys/Topology/Structures this receives 109 reference occurrences and
103 distinct published source files. Complete native GitHub trees previously
received at their immutable commits prove every current linked file's bytes.
The cohort retains the earlier passed MolSys scope and 38/22 Topology/Structures
attribute declarations. No optional converter is executed merely by linking it.

The complete syntax census is followed by a source-SHA-matched audit of the
retained full site at 1b98c2b1d. Ninety-one articles still match that source;
83 contain 1,575 unlinked Python-role nodes. The three changed native pages
are not attributed to the old full-site source and have separate current
receiving above. These counts include Python-role nodes in actual articles;
indexed generic form APIs are not blindly declared broken from source syntax.
This is a dated cached-article observation, not an installed/current-public-site
or optional-provider qualification. It bounds the remaining work and keeps
#727 partial rather than treating three corrected forms as a complete audit.

The [owner receipt](../../../devtools/data/native_form_reference_receiving_727_20261112.json)
retains source/HTML identity, baseline and test-draft failures, wider page rows,
notebook preservation and resource limits. Helpers are private and reusable
within tests; no runtime API, dependency floor or scientific model is added.


## Final native guard and common checks — 2026-11-12

The final private checker also requires the correct destinations within each
operation/conversion table rather than accepting the full href set anywhere
in the article. Sixteen source/semantic cases and three explicit rendered
cases pass after that refinement; the actual article bytes stay unchanged.
All fifteen common fast gates pass at their documented checkpoint, followed by
whole-repository Ruff lint/format on the final helper. Ten own terminal units
are retired/already collected with MainPID-zero checks; no foreign process is
signalled. The receipt distinguishes that staged source/test scope from a new
full scientific or installed verdict. #727 remains partial for the broader
source-matched cached article inventory.


## Native dictionary source correction — 2026-11-12

The next bounded increment covers MolSysDict, TopologyDict, StructuresDict and
MolecularMechanicsDict. Their 53 intended implementation references point to
53 files independently matched against the complete published 97ff11e1d tree.
MolSysDict now lists its actual 98 declarations; TopologyDict lists 78 and its
formerly omitted MolSys converter, for four registered routes. Both wrapper
pages now include their existing independent-copy operation. The other two
ordinary-dictionary forms retain 20/21 declarations and seven/two routes.

Descriptions distinguish versioned wrappers from in-memory arrays/quantities,
stable inventory from legacy chemical declarations, instance availability from
form-level declaration, and real operations from unavailable compatibility
hooks. StructuresDict subset extraction, add/merge and iteration are explicitly
unavailable in those hooks; its coordinate setter and append route remain
available. Empty mechanical/count-only topology conversions are not described
as chemical reconstruction. MolecularMechanicsDict has no coordinate axis.
Notebook code, outputs, metadata, six-cell order and anchors remain intact.

The initial test prototype has eight failures and sixteen passes; two failures
incorrectly require a particular count phrase. The corrected count check
accepts either wording while requiring the actual set and number. Its baseline
has six substantive documentation failures and eighteen passes. Corrected
source receiving passes 24 cases; six existing dictionary suites pass 55
runtime cases. Original attempts remain separate. A source-proof draft also
compares the API query identifier to a local tree object; correcting that
identifier check retains the independently verified file blobs. No library
implementation changes in this increment. Actual HTML delivery is still to be
received before claiming this four-page increment complete.


## Native dictionary HTML receiving — 2026-11-12

Clean `bdcd326ae` compiles the four corrected pages with zero warnings and
unchanged source inputs. All seven actual native-article guards pass, checking
intended link occurrences, correct table destinations, absence of unlinked
Python roles and local targets. The new four-page increment delivers 53
references; the seven reviewed pages now deliver 162 references to 156 matched
published source files. Its [receipt](../../../devtools/data/native_dictionary_form_reference_receiving_727_20261112.json)
retains failed drafts, source/reference hashes, code/output preservation,
resource limits and terminal status. Seven task-owned terminal services are
retired/already collected; no foreign process is signalled.

The unchanged-source/HTML wider census now receives 87 cached articles. Of
these, 79 retain 1,517 unlinked Python-role nodes. The seven changed native
pages have separate current receiving, not relabelled old HTML. Continue the
remaining native and external families without closing #727 prematurely.
The complete intake finds 647 issues, 93 open, no open PRs and new #728;
its bounded ProtOr API study is tracked separately. No additional scientific,
complete-source, installed, platform or publication qualification is claimed.

Fifteen common fast gates, generated-index verification and whole-repository
Ruff checking/format verification pass with unchanged checked inputs. Board/queue
reconciliation also passes after classifying #728. These fast controls do not
execute the separate complete-source or installed qualification routes.


## Remaining flagged native articles: source correction — 2026-11-12

The next bounded increment covers MolSysBuilder, MolecularMechanics, ViewerJSON
and GROFileHandler, the remaining native notebook articles flagged in the
cached census. It supplies 52 intended references to 48 independently matched
published files at ebded7917. The Builder table now includes both omitted
assignments, for 98 declarations; MolecularMechanics includes atom positions
and counts, for 21. ViewerJSON retains 18 declarations and its graphics
identity/extraction limits; GRO retains 62 declarations and its resident,
whole-handler and unavailable-hook boundaries. All three/two/two/five
registered routes remain. The mechanical container's unavailable add/structure
hooks are no longer described as supported operations; merge/drop/report limits
and experimental parameter scope remain explicit. No runtime implementation
changes. Code, outputs, metadata, anchors and cell order are preserved.

The baseline has six documentation failures and 26 passes. Corrected source
receiving passes 32 cases. The first existing-runtime cohort has 68 passes and
six failures in an old GRO documentation guard: it locates rows by the dotted
Sphinx spelling, which the new actual source links replace. Its locator now
accepts the exact published-source path as well; all independent-copy,
unsupported-operation, iterator, nonmutation and quantity assertions remain.
The failed attempt stays recorded. Actual HTML receiving and final checks
remain due before claiming this increment delivered.


## Remaining flagged native articles: HTML received — 2026-11-12

Clean `61e0a24ba` compiles the four pages with zero warnings and unchanged
inputs. All eleven actual native-article guards pass with correct intended
hrefs in their tables and no unlinked Python roles. The latest existing-runtime
cohort passes 74 cases after the GRO locator adjustment; 32 source controls
also pass. The [remaining-native receipt](../../../devtools/data/native_remaining_form_reference_receiving_727_20261112.json)
retains source/HTML hashes, failures, source-file proof and resource limits.
Eleven reviewed native pages now deliver 214 reference occurrences to 204
matched published source files. This completes the native-family debt identified
by this census, not the whole issue.

The unchanged-source/HTML audit now receives 83 cached articles: 75 retain
1,461 unlinked Python-role nodes, all outside the native class-form family.
Continue external class, file and string families with actual destination and
availability checks. Complete intake remains 647 issues, 93 open and no open
PRs; no newly numbered issue after #728 is present at this checkpoint. Keep
the finite documentation-review handoff cutoff, original score and separate
complete-source, causal, long-memory, installed and publication boundaries.

Fifteen common fast gates, generated-index verification and whole-repository
Ruff checks/format verification pass with unchanged checked inputs. Board/queue
reconciliation passes. Seven exact task-owned services are terminal/retired; no
foreign process is touched. These results do not lift the qualification pause.


## File-family source review — 2026-11-12

The next increment covers all 26 flagged file notebooks. The new discriminating
baseline has 29 failures/55 passes: missing intended-link delivery, three stale
attribute inventories (H5MSM and two YAML domains), and missing MolSys routes
for SMILES/topology YAML. Corrected H5MSM/MolSys-YAML/topology-YAML inventories
match 116/98/78 declarations, distinguishing version/layer/instance availability
and PyYAML prerequisites. Both omitted routes are restored. Unavailable
add/merge/append/set/iterator and copy hooks are no longer advertised as working.
Resident versus backend iteration and coordinate-dump XYZ's actual header,
units and absence of an element column are explicit. Earlier reader, identity,
chemical-evidence and selection explanations remain.

The first corrected cohort has one failure/83 passes. GRO's self-conversion
links to a dormant to_file_gro wrapper rather than its registered extract
route; the final route correction passes all 84 cases. The shared private
guards preserve eleven native cases and add an explicitly reviewed file
inventory, conditional YAML registry checks and independent converter-table
destinations for hooks reused as converters. They do not glob-admit future
adapters or execute every optional conversion. Actual HTML receiving remains
due. Notebook code, stored outputs, metadata, anchors and six-cell order remain.

The source review separately discovers #729's independent-copy/source-safety
bug. Its functional correction is published in 7b607f638, with a retained
80-failure/52-pass baseline and 136 corrected focused/example passes. That
correctness work is admitted under #334's finite cutoff; its documentation,
common gates and lifecycle closeout remain separate from #727's link repair.


## File-family integrated source receiving — 2026-11-12

The final combined cohort passes 237 cases, including the 84 reference/native
controls, #729 file extraction, dictionary schemas, PDB/GRO instructional
examples, the new recipe under two unit policies and basic.extract doctests.
One expected LegacyH5MSMWarning is retained rather than suppressed. The final
26 pages contain 493 intended reference occurrences to 440 independently
matched files at published 7b607f638. Empty getter modules and unavailable
operations are distinguished from delivery through other supported routes.
Actual HTML and common/lifecycle completion remain pending; #727 stays partial.


## Public-route follow-up before final receiving — 2026-11-12

The first clean 543831138 build receives 29 pages with zero warnings; its
37 actual native/file article guards pass. An extra public HDF5 subset control
then exposes a legacy output_name route defect despite direct-adapter success.
Nine further identity routes reproduce that same issue. #729 corrects those
registered routes in public 7097f81c5 without enabling unsupported MOL2 output.
All 26 file articles now point to that exact updated source. The final combined
cohort passes 258 cases with the same one expected legacy-0.4 warning. Renew
clean HTML/article receiving after the source-link change; preserve the earlier
237-case and first HTML results at their original scope.
