---
summary: Expose public protonation-removal correspondence for managed consumers.
issue: uibcdf/molsysmt#576
status: resolved
opened: 2026-11-05
closed: 2026-11-06
verification: measured
area: [build, protonation, molsysviewer]
guard: tests/build/test_protonation_assessment.py
normative:
blocked_by: []
supersedes: []
---

# Public protonation-removal correspondence for managed consumers

**Status:** native provider contract resolved and integrated on main. Managed
consumer receiving is separate. Native method and pH criteria are unchanged;
the result remains experimental.

## What

Provide a public, provider-owned correspondence contract for `build.reconcile_protonation` so consumers can synchronize atom removal without importing private protonation rules, matching labels/coordinates, or running the scientific decision twice.

This is a missing integration capability, not a request to change the pH method, add detectors, or make Viewer observe arbitrary external edits. Requested under #421 / PR #543 and uibcdf/molsysviewer#264. The independent native result is already useful.

## Baseline inspected before owner implementation

Reviewed published native source `ccff2557f576f004461c96950d36a8b6e465e91f`:
- The public signature is `reconcile_protonation(molecular_system, pH=7.4, engine="MolSysMT", in_place=False, skip_digestion=False)`.
- The private `build._protonation.unexpected_hydrogens` determines the removal list, then public `basic.remove` publishes a subset.
- Default independent output has no operation-scoped public removal report; `in_place=True` returns None.
- The helper also rebuilds derived components, so it is not an approved read-only public preflight contract for consumers.

A native-only check on bundled villin (`chicken villin HP35/1vii.pdb`), explicitly extracting structure indices [0, 0, 0], gives 596 atoms at pH 7.4 and 590 at pH 12.0. The removed labels are H3 in group 0 and HZ3 in groups 7, 24, 29, 30 and 32. All three structures survive. These are bounded reference-rule checks, not environmental-pKa validation.

The existing Viewer managed-edit boundary needs trusted retained-atom correspondence before publication. Atom counts do not establish identity; atom/group IDs can repeat. A successful None result cannot provide that correspondence. Viewer must not reconstruct the provider's scientific selection from templates or private helpers.

## Requested contract

Please choose a public design that supplies:
1. Operation-scoped source indices and retained old-to-new correspondence, with explicit direction/order, universes, structures and input identity/version assumptions.
2. Assessed versus unassessed scope and the actual native reference/naming/pH parameters. Empty removal must distinguish a true no-op from unsupported/unassessed chemistry.
3. A read-only assessment/prepared-operation route available before mutation, reusable by execution without repeating the scientific decision; or an equivalent map-producing independent-result/publication contract suitable for safe integration. A post-write report alone does not satisfy the current host's prepublication mapping boundary.
4. Native independent/in-place return semantics, no-op behavior and failures, including whether candidate preparation is atomic and whether derived components/analysis coverage may change.
5. Consistent remapping/invalidation of named analyses and stored domains, without hidden charge assignment, hydrogen addition, chemical-state choice or preparation.

This does not prescribe a particular function name or force a new viewer-specific public API. A reusable native report/plan is preferable to a second protonation implementation in a consumer.

## Acceptance criteria

Add native pytest coverage for actual H removal and no-op results, unsupported/unassessed and declared named-state groups, repeated/nonunique labels, all source structures, preserved retained coordinates, map direction/uniqueness/composition, independent ownership, analysis remapping and failure/partial-publication semantics. Test that preparing the public assessment does not mutate the source and that execution consumes the same declared decision. Document the limits of fixed-pKa reference rules.

The addon can meanwhile expose the independent route and reject managed `in_place=True` before science, with that limitation explicit. This is not full in-place receiving or package qualification. No scientific native implementation is authored in Viewer.

Record through PR #543: `devguide/pending_proposals/protonation_removal_correspondence_for_bound_consumers.md`.


## Scope

The report requests a reusable public native integration contract. It does not
request automatic observation of arbitrary molecular edits or require a specific
API spelling. The consumer will receive the independent default first, with
managed in-place execution rejected before science until correspondence is qualified.
No private protonation helper or scientific inference is added to the addon.

## Owner implementation plan — 2026-11-06

The maintainer-ordered objective authorizes preparation of this source while
earlier entries complete integration. No issue closes out of order.

1. Share one read-only native evaluation with the existing unexpected-H warning.
   Derive temporary component labels through the existing compiled native
   component primitive, honoring stored joins_components. Do not rebuild source
   components or change reference-state/naming/pH interpretation.
2. Add public `build.assess_protonation` and a typed
   `build.ProtonationAssessment` result. The result owns detached coverage,
   source-index maps, actual parameters and references, not a coordinate copy.
   Its `to_dict()` provides report data; `apply()` consumes the same decision
   without invoking hydrogen-reference inference again. The existing
   `reconcile_protonation` delegates this path with its existing signature.
3. Bind a prepared operation to its source object/resource and a chemistry,
   stable-inventory and axis fingerprint. Validate again before publication.
   Avoid hashing trajectories: coordinate edits on unchanged axes remain valid;
   changing inventory, chemistry, naming, reference state or structure count
   invalidates the operation. Callers serialize source access. Plans are
   process-local execution objects, not authentication or general value passports.
4. Stage an independent subset through the existing public removal tool, then
   use its native atomic publication boundary for in-place execution. Do not
   publish partial domains, select a chemical state, assign charges or add H.
   True in-place no-ops retain domain identities; independent no-ops must return
   independent data. Successful plans are single-use; preparation failures do
   not consume an otherwise valid plan.
5. Expose full-source positional maps in both directions with -1 for removed
   atoms, retained order and an unchanged all-structure axis. Distinguish fully
   assessed no-change, partial no-change and entirely unassessed scope. Repeated
   IDs/names never substitute for these maps. Preserve ordinary removal's stored
   domain and named-analysis projection/invalidation contracts.
6. Validate actual removal, no-op/unsupported/named-state cases, immutable
   assessment, all structures/coordinates, source staleness, once-only scientific
   evaluation, failure atomicity, map composition and analysis projection. Reuse
   ArgDigest, SMonitor, optional Ackredit and existing conversions; introduce no
   engine or dependency. Update docstrings, User Guide, Cookbook/course and
   maintained contracts before declaring source receiving complete.

Implementation and tests are pending at this planning checkpoint. The type is
an operation result, not a molecular-system form or a new chemical data store.

## Initial source-in-progress checkpoint — 2026-11-06

The read-only core and public prepared-operation route are now implemented in
`dev/ordered-stabilization-576-20261106`, still uncommitted and unreceived. The
first affected selection passes 281 cases. The subsequent focused controls
exercise actual and no-op removal, source staleness, detached reports, weak
source ownership, metadata-only H5MSM assessment, map composition through the
existing atom_map@1 tool, all states/associations, named analyses and mechanical
arrays. Candidate preparation stays independent before atomic publication.

Initial exploratory tests assumed the wrong LYN H-name layout, used a removed H
as the endpoint of a supposed surviving observation, equated occurrence row
positions across distinct remapped analyses, or treated raw native canonical
charge arrays as quantities. The corrected controls check reference-state
pH independence, guaranteed retained endpoints, per-analysis occurrence indices
and actual charge values without changing the scientific reference rules or
the existing interaction/removal contracts.

At that checkpoint public lifecycle documentation, optional-attribution receiving,
public provider floors and broader final checks were pending. The tutorial was
authored but not yet executed. The following receiving supersedes those pending
source-preparation tasks, without claiming main integration or addon admission.

## Prepared owner contract and receiving — 2026-11-06

Prepared source: **5c13fcd85f03a5db956f7854686f5493789820d4**, published on
`dev/ordered-stabilization-576-20261106`. The owner handoff is recorded in
[issue #576](https://github.com/uibcdf/molsysmt/issues/576#issuecomment-6688444056).
This source is available for consumer review; it is not yet integrated in main.

**Implemented and contract-tested:** `build.assess_protonation` returns a public
`build.ProtonationAssessment`. Its detached `to_dict()` report uses
`molsysmt.protonation_assessment@1` and the existing `molsysmt.atom_map@1` schema.
The latter retains `n_source_atoms`, `n_output_atoms`, full-length
`source_to_output_atom_indices` (-1 for removed atoms), and ordered
`output_to_source_atom_indices`. `structure_indices` spans the unchanged current
source axis, not deposited IDs or an inferred upstream structure mapping.

Every group retains its actual name, naming declaration, assessment status/reason
and available terminal/disulfide context, including unassessed and empty groups.
Coverage distinguishes assessed and unassessed groups, unassigned atoms and stored
chemical states outside the reference comparison. Actual pH, method/version,
producer version and detached consulted references accompany the result.

`apply(source)` reuses the exact decision once. Native source/domain identity and
inventory/naming/chemistry/axis fingerprints are validated before candidate
preparation and again before publication; skip_digestion never bypasses these
guards. Coordinate values are intentionally excluded. Current coordinates,
mechanics, analyses and history are projected at execution. Native publication
uses the existing atomic subset boundary after complete candidate preparation;
failed preparation leaves the source and plan unchanged. Callers must serialize
external source access. No persistent transaction or resource authentication is
claimed, and executable plans are process-local.

The existing reconcile_protonation signature is unchanged and delegates this
route. Its independent output is now explicitly a native MolSys for every
supported input form, including files/complementary inputs. Independent no-ops
return independent data; true native in-place no-ops preserve domain identities.
This corrects the old no-op aliasing and unspecified foreign-form output behavior.
All stored states are subset without choosing or certifying another state;
named analyses follow normal remapping/invalidation without recalculation.

Native and modular H5MSM assessment avoids coordinate/interaction payload reads.
The plan holds metadata/maps and weak source references rather than a trajectory.
Other form conversions and full candidate application retain their ordinary
memory costs; neither a universal streaming promise nor an RSS benchmark follows.
Existing compiled component labeling honors joins_components without rebuilding
source components. No scientific pH rule, heavy template or H placement changes.

The [receiving receipt](../../../devtools/data/protonation_assessment_receiving_576_20261106.json)
retains source/runtime identities, fingerprints and separate overlapping checks:

- **1,717 affected cases pass**, covering build tools, amino-acid expectations,
  atom maps/removal, chemical-domain extraction and native forces (135.67 s).
- **260 public-provider-floor cases pass** using unchanged ArgDigest 0.14.0,
  DepDigest 0.15.1, SMonitor 0.16.0 and Ackredit 0.9.0 payloads (13.46 s).
- **631 documentation, doctest and final assessment controls pass** (32.21 s),
  including two additional native/H5MSM non-default-unit controls. These
  selections overlap and must not be summed as distinct cases.
- The ten-code-cell assessment tutorial executes successfully. Foundations,
  Toolbox, Cookbook, course guidance, API entries and generated experimental
  inventories are synchronized. Course changes preserve every executable cell,
  saved output, cell ID and metadata value.
- The fast gate passes **14/14**; Ruff lint/format, dependency routes and public
  signature checks pass. This is not a complete source matrix or installed pair.

The initial broad command included nine online PDB/BCIF controls that failed
under restricted DNS, plus one isolated subprocess test whose global `tests`
import resolved to the controlled Viewer's test package. Repeating with permitted
public reads resolved the nine network cases. The subprocess now loads its own
exact fixture file and still rejects every optional chemical-engine import.
The complete final selection passes without excluding those cases. The reduced
course-navigation fixture also now receives two real target headers and asserts
their rendered links, rather than suppressing the missing-target warnings.
An initially incorrect root-level MolSys doctest import was corrected to the
public native namespace. Regenerating the scientific matrix adds only the two
experimental symbols; it does not fabricate new scientific validation.

ArgDigest owns the operation-specific finite-pH/source/boolean boundary; SMonitor
provides signals and typed failures. No new optional scientific engine is required;
foreign conversion routes retain their existing lazy DepDigest guards. PyUnitWizard
unit-policy controls preserve physical coordinates. Real optional Ackredit sessions
receive reused consulted references, while detached references survive provider
absence. Applying a prepared decision does not credit a second pH inference.

**Remaining:** integrate the qualified owner source in the maintainer's order,
then perform documented provider closeout. The Viewer team must separately receive
the prepared correspondence before admitting managed in-place removal. No tag,
Release, publication, Viewer runtime change or installed-package qualification is
authorized or implied by this source checkpoint.

## Integrated checkpoint receiving — 2026-11-06

The prepared source reached main at 6b76a9d7e. Its actual smoke run
[42252758948](https://github.com/uibcdf/molsysmt/actions/runs/42252758948)
failed before runtime tiers: the hosted command omitted the newly added
`test_native_receiving_583_584.py`, and the exposure inventory still assumed
that every new native build function had already been admitted to the addon.
These are real integration failures, not passing or cancelled evidence.

Recovery includes the omitted module in the existing single pytest invocation
and explicitly guards the sole unexposed build route, `build.assess_protonation`.
The inventory continues reporting it as missing. This does not add a placeholder,
claim complete addon exposure, remove an existing public bound route or admit
managed assessment/application. The remaining native-route and command-completeness
assertions stay active. All three hosted guard modules plus the newly included
native-receiving module pass 38 local cases; six legacy-H5MSM warnings remain.
The next published exact-head smoke run must still execute and be inspected.

## Resolution — 2026-11-06

The public provider contract is implemented and integrated on main:
`build.assess_protonation` returns a read-only prepared `ProtonationAssessment`
with detached typed report, explicit source/retained maps, named/reference-state
and evaluated/unassessed scope. `apply` consumes that same decision, validates
its declared identity/axis/chemistry assumptions, and preserves the documented
independent/in-place/no-op and atomic-failure behavior. Actual H removal,
repeated labels/structures, retained geometry, analysis remapping and refusals
remain protected by `tests/build/test_protonation_assessment.py`; the final
joint source selection reruns this guard. Earlier 1,717 affected, public-floor
and documentation results remain the scoped evidence recorded above.

This completes the native contract requested by the issue. Fixed-pKa rules remain
bounded and experimental; no H addition, charge assignment or environmental pKa
prediction is claimed. The existing independent bound reconcile route remains,
and managed assessment/application receiving stays with the Viewer consumer
under #421 / uibcdf/molsysviewer#264. The explicit missing facade in the source
inventory is not erased or replaced with a placeholder. Closing this provider
issue does not certify that consumer workflow or the #334 installed release pair.
