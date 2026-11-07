# MolSysViewer molecular tools workspace — design for review

**Role:** proposed GUI design under uibcdf/molsysmt#421 and
uibcdf/molsysviewer#264, delivered through PR #543.
**Date:** 2026-11-05. **Input:** addon c0149a2d6, native owner 8486ea59c.
**Status — 2026-11-06:** contribution source implements System / Remove atoms,
Extract subset and Copy system, plus Geometry / Translate, Center, Superpose structures and qualified periodic tools. Selection controls,
lifecycle, bounded metadata and independent-result presentation are shared.
Chemistry adds stored-information and hydrogen-inventory inspection, plus explicit
heavy-atom and hydrogen preparation with reviewed independent-result replacement.
Analysis adds native distances, extrema, neighborhoods and explicit selected-row
selection/focus/live-Measure actions. Its isolated follow-up adds raw/optimal
RMSD, gyration, per-atom RMSF and deliberate core structure plots; the receipt
below preserves that source's pending host integration. Rotate, further Chemistry
assignments/construction and remaining Analysis families remain proposed; no placeholder
panel/button is registered. Human Jupyter/visible Qt acceptance remains
postponed, separate from automated Jupyter/Mol*/native numerical receiving.
Center uses native geometric/mass-weighted source references and explicit
point/selection destinations per processed structure, with fixed box and reviewed
current/independent effects. Shared diagnostics retain rejected-operation text
through automatic refresh without replaying science (#603). The
[Center receiving receipt](../devtools/data/molsysviewer_tools_center_receiving_20261106.json)
records analytical, native and actual Jupyter/popup coverage. The
[superposition receipt](../devtools/data/molsysviewer_tools_fit_receiving_20261106.json)
adds 315 native/panel and 63 route cases plus six actual Jupyter scenarios. It
also records the completed 4,568-case collection on the prior Center source;
that full result is not presented as a full run on the new superposition source. Owner integration,
hosted exact-head and installed gates remain separate.

**Independent results update — 2026-11-05:** source now adds Extract subset and
Copy system through the host presentation boundary in uibcdf/molsysviewer#301.
The result is computed once, then explicitly shown in notebook output or a
window (desktop: window only). Python recovers the View by handle. Unpresented
results are discarded when a task is left; presented Views survive panel/source
closure. Real Jupyter receiving covers ordered structures, separate native data
and both destinations, repeated destination changes, fullscreen delivery and
detached Studio. Hosted exact-head gates remain pending. Native-window ownership is tested separately from postponed human
visible Qt qualification. Other destinations, further Geometry tasks and Chemistry/Analysis
remain planned. The dated status above retains its initial scope.

The initial Geometry controlled host was Viewer `177e19a8fa06e37484a801da1711cc99acbc8f2d`, retaining
presentation recovery and interactive declared readers under #304 and adding
conditional replacement under #306. Earlier receipts retain their own host identities.
The five contribution routes at that receiving checkpoint pinned Viewer
`239c8dd74815a660159a95970e9136d7beebfdd2`, receiving #307 and the measurement
geometry/value/lifecycle corrections in #308–#313. Complete local Python and
44-suite core receiving, hosted E2E, four Linux Python cells and Linux/Windows
source-pair jobs pass for that host. MacOS remains queued; the source pin is
not installed-artifact or full-platform qualification.
The source receiver also incorporates native ed09f6453, including the owner's
#583/#584 repairs. Consumer observations are archived alongside the native
resolutions; no duplicate open report is retained. The final receiving receipt
records exact source hashes and separately selected browser/Qt scopes.

The expert API remains the scientific foundation. This design uses qualified
native operations and their existing managed-edit adapters; it does not change
Python signatures, defaults or result types. The core/addon boundary and
[accepted plan](pending_proposals/molsysviewer_tools_addon.md) remain in force.

## Navigation and information density

Use one addon workspace titled **Molecular tools**, identified as **MolSysMT**.
Reuse AddonWorkspaceSpec, AddonPanelSpec and AddonPanelWidget. Four intended
horizontal panels follow the existing Elastic Networks pattern; register only
panels with real tasks and receiving guards. Current source registers System,
Geometry, Chemistry and Analysis:

| Panel | User intent | Typical tasks |
| --- | --- | --- |
| System | Choose and modify molecular inventory | Remove atoms, extract a subset, copy a system, inspect the chosen inventory. |
| Geometry | Work with coordinates, structures and cells | Translate, rotate, align, choose structures, wrap/unwrap and edit an explicit cell. |
| Chemistry | Assess, prepare or construct molecular data | Inspect missing chemistry, add supported atoms/bonds/cappings, type or charge atoms, build a peptide or water cell, solvate and reconcile protonation. |
| Analysis | Calculate and inspect scientific results | Distances/neighbors, conformational/sequence/chemical reports, qualified interactions and mechanical quantities. |

The panels are tasks, not copies of module names. One task picker shows one
form at a time; do not stack dozens of tools or put three unrelated action
buttons below one ambiguous selection. Each task states its input, scope,
method/model, prerequisites, result ownership and effect. Use short task
labels, stable drafts, normal-size labels and help beside consequential choices.
Keep advanced syntax, indices and specialized parameters in disclosures.
The exact English labels and grouping are proposed, not frozen API names.

Use core Load for loading/composition and core Export for established system
output. Core selections, regions, scene Interactions, Measures, Shapes and
visual styles remain their owners. A calculation does not automatically create
a representation. Do not add a competing Loader, molecular-system store,
scene manager, result serialization promise or second set of saved selections.

At narrow widths keep the panel navigation reachable with keyboard and without
page overflow. Wider/Qt/popup layouts may widen fields and summaries; their
operation semantics must remain identical. Do not couple addon visibility or
panel switching to molecular mutations.

## Scientific capability placement

| Expert namespace | GUI use and boundary |
| --- | --- |
| basic | Inventory, native selection, removal, detached copies/extraction and explicit composition; only qualified effects. Core loading/export remain shared. |
| topology | Sequence/inventory reports in Analysis; preserve contributing-group maps and native prerequisites. |
| chemical_states | Graph/state reports in Chemistry or Analysis; graph cuts do not delete stored bonds. State/reference choices are explicit. |
| structure | Geometry transforms and Analysis observables; separate calculations from coordinate edits and keep structure/reference choices explicit. |
| pbc | Geometry tools and explicit cell utilities; no inferred box, image policy or automatic wrapping. |
| build | Chemistry auditing/preparation/construction; independent outputs need an explicit use decision. Reference-rule protonation is not environmental-pKa prediction. |
| physchem | Chemistry readiness/typing or Analysis properties; tables, geometric calculations and typed results retain their distinct units and meaning. |
| molecular_mechanics | Analysis/qualified minimization with explicit model, structure, engine and units; no hidden parameterization or fallback. |
| interactions | General results in Analysis; visualization/attachment remains explicit in core Interactions. Native experimental classifications remain visible. |
| element | Native reference/name tools where a task needs them; no parallel chemical interpretation or naming conversion. |
| attribute | Native field metadata/help and admitted choices, not a generic unqualified setter. |
| supported | Explain declared availability and missing prerequisites; declarations do not certify execution. |
| h5msm and form | Specialist file/text tasks where needed; reuse qualified destination/delivery contracts, including remote use. |
| historical hbonds | No duplicate GUI menu for aliases; use the canonical family. |
| molecular_dynamics | No executable GUI item for unconditional native stubs. |

The source inventory is a dated snapshot, not a permanent count. New owner
exports, such as work currently in progress outside this contribution, require
source receiving and qualified effect contracts before GUI admission.

## First complete slice: remove selected atoms

The default System task is **Remove atoms**. It never defaults a destructive
selection to the whole system. An empty workspace says **Load a system first**
and leaves editing actions disabled. A loaded workspace shows bounded context:
label, atom count and structure count, not a trajectory-sized payload.

1. **Choose atoms.** Offer Current selection, Saved selection, Region and
   Molecular category, plus explicit expression/indices in Advanced. Water and
   ions prefill native selection criteria; they are not separate removal tools.
   Resolve groups/categories with public native selection. Explicitly changing
   a selection source never changes data or silently changes canvas selection.
   A separate Show selection action may use the core selection owner.
2. **Review removal.** Resolve native atom indices without copying coordinates.
   Display selected/retained atom counts, relevant group counts, the molecular
   target and all-structure effect. Removing inventory removes those atoms in
   every structure. A visible-frame selector must not imply per-frame topology.
   Include a concise scene/reference remapping notice. Zero matches is neutral
   (**Nothing to remove**). Reject all-atom removal before execution; clearing
   a view is a different explicit host operation.
3. **Confirm inline.** Replace Review with **Remove N atoms** plus Back. This is
   the only destructive confirmation in the normal path, without modal chains.
   The review states that molecular removal has no scene-history Undo. It
   distinguishes deletion from hiding and from disabling a region.
4. **Execute once.** Invoke the same qualified native removal plan used by
   basic.remove(in_place=True, update_view=True). Do not apply its independent
   default and silently adopt it. Preserve native validation and all structures;
   the GUI explicitly chooses in_place, while the expert default stays intact.
5. **Report outcome.** Show actual remaining inventory and retain the user's
   task/selector draft. Native no-op, rejection, completed edit with projection
   failure, and uncertain partial write are different outcomes. A completed-edit
   projection failure points to the existing canvas Update view action, never
   repeats removal. Addon commands remain paused until that recovery. Uncertain
   writes require the host's explicit recovery/replacement contract.

Completed removal retains its bounded outcome across synchronized-context
refreshes while the same target, revision and draft remain valid. A new action,
changed target/revision/draft or panel lifetime expires it. The retained outcome
contains neither selected indices nor an executable token; refreshing never
repeats removal. Review summary labels and values explicitly own their layout
under notebook HTML styles. These corrections are tracked in #590 and #591.

## Review validity and concurrent windows

A reviewed operation is transient and bound to its view, target object, managed
revision, resolved atom indices, structure universe, task and parameter draft.
Any target replacement, managed edit or relevant draft change expires it.
Panel unmount/disable/close expires executable review tokens; drafts may survive
navigation. Other live endpoints receive/requery current molecular status.
A stale completion cannot publish a result into a replacement or closed view.

The comparison and publication must share the coordinator's serialized boundary.
A UI-only revision check followed by a later independent edit call is insufficient.
Reuse the addon-owned removal preparation adapter inside system_edits.execute:
check the review token on the callback target before preparing/publishing the
existing qualified plan. Do not add expected_revision to every scientific API
or duplicate native removal. Prove the interleaving with two-window/thread tests
before enabling Confirm. Merely equal counts or labels do not establish identity.

The protocol concerns managed edits. It does not claim to observe arbitrary
mutations of view.molsys or raw arrays. External edits retain the documented
explicit reconciliation responsibility; preview tokens are not source fingerprints.

The host's bounded `viewer:system-sync-changed` event invalidates frontend
reviews and triggers a fresh context request when synchronized. Python still
checks target identity, managed revision, structure and relevant selection
inside the serialized execution callback. Mount/unmount scopes the token;
only bounded drafts survive navigation. The source consumer requires the host
fixes tracked in uibcdf/molsysviewer#297/#298, not merely its older declared
capability floor. Current receiving pins the exact host source independently
of public artifact compatibility.

Keep only bounded drafts in persistent frontend state. Resolved indices stay
in Python; the requesting panel receives one opaque, transient confirmation
token without persisting it in the model or exported session. Do not broadcast full MolSys,
coordinate arrays, all selection indices or candidate trajectories to every
popup. Do not serialize stale tokens or arbitrary live addon state in session
exports; use only the host's qualified persistence contracts.

## Extraction, copying and result destinations

**Extract subset** and **Copy system** are separate tasks with separate result
ownership. basic.extract and basic.copy return molecular data. view.extract
returns a new View with migrated scene objects; these are not interchangeable.
The source is unchanged. Explicit structure order, including nonconsecutive
indices, stays visible. Explain materialization for trajectory-sized outputs;
do not construct a candidate just to display an atom-count preview.

After creating a result, present its actual kind, size and provenance and offer
only qualified destinations. **Use in this view** is an explicit replacement,
with its scene/history consequences reviewed first; it is not automatic adoption.
Saving uses the established local/remote delivery contract, never an arbitrary
browser path treated as a server path. H5MSM is recommended where its domain
coverage applies, with native loss validation for other formats.

**Open as new view is a host presentation gate.** Constructing a Python View is
not equivalent to presenting it from a widget callback or opening a second Qt
window. Source review found no common public addon operation that guarantees
that presentation in all hosts. Do not silently call IPython.display, invent a
Qt-only path, or show a successful invisible View. Qualify/reuse a generic host
presentation contract before enabling that destination. This does not block the
remove-atoms slice. It must be settled before calling the extraction GUI complete.
Candidate retention, replacing an earlier result and explicit discard need
bounded ownership; unmounting a panel must not leak large independent outputs.

The current source uses `view.addons.manager.presentations.prepare` and `get`
and the panel's `model.present_view` adapter under Viewer #301. Expert wrappers
retain molecular returns. A fresh destination click handles browser activation;
Qt creates another native window with its own transport in the same application.
Retry does not recalculate. Source support is not published-package or human
visible Qt qualification.

## Remaining panels and result policy

### Next Geometry slice: translation and rotation — design review 2026-11-05

**Implementation update — 2026-11-06:** Translate is implemented as the first
Geometry slice; Center and Superpose structures are now implemented in contribution source. Rotate remains proposed pending #602. The maintainer keeps human System/Jupyter/Qt
acceptance postponed. That deferral does not accept the UI or block preparation
of this next slice. Register Geometry only when actual tasks and their guards
exist. Preserve System as a separately pending acceptance item.

Use one Geometry task picker for implemented **Translate**, **Center** and
**Superpose structures**, adding **Rotate** when its native prerequisite is received, with the
same selection/result vocabulary as System. Both edit molecular coordinates;
they do not change the camera. Directions use the molecular Cartesian axes,
independently of the camera orientation. Keep one task form visible at a time.

The proposed form has these ordered groups:

1. **Atoms:** Whole system, current selection, saved selection, region or an
   explicit expression/index list. Reuse the selection owner; resolve one fixed
   atom population in a stated current/explicit structure context. Do not
   silently select a different population in every trajectory frame. Empty
   selections cannot become a whole-system edit. Duplicate GUI atom indices
   must not accidentally weight a centroid; retain expert native semantics.
2. **Structures:** All (visible default), Current or explicit distinct indices
   in their supplied order. The review states actual atom and structure counts.
   GUI uniqueness avoids ambiguous repeated edits; expert wrappers retain native
   repeated-axis behavior and broadcasting. Never substitute the visible frame
   for an explicitly requested all-structures operation.
3. **Parameters:** Translate exposes dx/dy/dz and explicit length units. Rotate
   should expose a clearly labeled system axis and angle with degree/radian
   units, not require a nonprogrammer to enter a 3x3 matrix. Its center is an
   explicit choice: geometric center of the selected atoms **in each processed
   structure**, coordinate origin, or a fixed unit-bearing point. The proposed
   friendly default is the geometric center, without mass weighting. This GUI
   choice does not change native rotation_center=None or the expert API.
4. **Effect:** propose Current system (with review) or Independent result. Keep
   one primary action: Review change / Apply translation or rotation for the
   current system; Create result for independent output. Native independent
   defaults remain unchanged. An independent transform returns a **complete
   system**, modifying only the chosen atoms/structures; it is not an extraction
   of that population. Reuse the qualified result destinations and handle
   lifetime rather than implementing another result registry.

An inline current-system review freezes target identity, managed revision,
selection/structure context, resolved indices and the full parameter/effect
draft. Changing any relevant input, navigation, replacement or managed edit
expires it. The final validation and calculation share system_edits.execute's
lock, using the same admitted coordinate-transform preparation adapter as the
expert API. Compute frame-dependent centers inside that serialized operation,
not in an earlier preview that can become stale. Preview must not copy a
trajectory merely to count atoms or display parameters.

Use the native public translate/rotate operations and get_center(weights=None)
for geometric centers. Native centers already have shape (n_structures,1,3),
matching the transform's frame broadcasting; preserve explicit structure order.
The native quaternion/Rodrigues kernels and an existing builder axis-angle
helper are available. Before enabling an axis/angle control, settle and test
the reusable conversion in its proper MolSysMT mathematical owner (#602); do not copy
a rotation formula into the frontend/addon or add an undeclared SciPy dependency.
Matrix and rotation-object inputs remain available through the expert API.

Scientific effects must stay visible: these operations keep the periodic box
fixed and do not wrap coordinates. A coordinate rotation is not automatically
a rotation of a periodic lattice. Euclidean rigid-body invariance does not
promise unchanged periodic minimum-image geometry. Native coverage invalidation
for affected stored analyses remains authoritative. Anchored and absolute scene
objects keep their existing coordinate semantics; molecular edits have no
scene-history coordinate Undo. After completed science with failed projection,
retry only Update view. Do not infer scientific no-ops from approximate matrix
equality or suppress a small requested transformation.

Qualification must include analytic translations and +90-degree proper rotation,
nondefault unit policies, fixed and per-structure centers, explicit [2,0]
structure order, unchanged unselected atoms/structures, independent source
preservation, fixed boxes, native analysis coverage, stale confirmations across
windows and synchronization-only recovery. Then qualify real Jupyter/Qt and
popup presentation in their separate scopes. Do not claim human acceptance from
headless tests.

**Read-only receiving:** on contribution f7b305b3a/native ed09f6453 with Viewer
42234de8, the existing transform and principal-axis receiver files pass 184
cases in 55.93 s. Their 188 legacy-H5MSM warnings and one invalid-determinant
warning from negative-input validation are retained. A separate real-pentalanine
probe rotates six atoms in structures [2,0] about their native geometric centers
under an angstrom application policy. The +90-degree Cartesian oracle agrees
within 2.23e-16 nm, the source stays unchanged and no scene/result View is
created. This supports reuse of the primitives; it does not qualify a GUI or
arbitrary axis/angle inputs. No runtime or scientific function changes here.

Geometry chooses atoms, structures, reference, units and periodic behavior
explicitly. A GUI Apply action may choose a qualified in-place edit with immediate
projection; native independent defaults and expert options remain unchanged.
Reflection is not rotation; coordinate wrapping is not a new periodic model.
Coordinate-free systems and unsupported multi-structure operations get accurate
prerequisite messages, not an implicit first/visible-frame substitution.

Chemistry distinguishes reports, proposed independent systems and managed edits.
Never add H, assign charges, change protonation or choose a force field to make
a later task succeed. Native assessed/unassessed scope and incomplete results
remain visible. Independent candidates need explicit use; unsupported mapping
must not be faked by atom names, counts or coordinates. Managed protonation
now receives #576's public assessment/maps through the expert edit adapter;
#572's force reader is also source-received. Their graphical tasks and broader
scientific qualification remain explicit work. Missing modes do not block
unrelated qualified tasks. Do not present unpublished owner work as a released capability.

Analysis uses bounded summaries/tables/pages and explicit units, structures,
method/model and provenance. A zero result is distinct from missing data,
unassessed scope or unevaluated structures. Long calculations need actual
progress/cancellation contracts before such controls are promised. Plotting or
adding a result to the scene uses the appropriate core owner and a separately
qualified adapter. Generic native results do not imply universal H5MSM storage.

### Analysis distance family — source contract 2026-11-06

Distances, Minimum distance, Maximum distance and Neighbor search delegate to
the four public structure tools through the unchanged expert facade. Two shared
atom editors independently select source populations; a within-population mode
keeps the native symmetric/self or directed-neighbor conventions explicit.
Selections resolve in a stated reference-state/structure context before the
fixed population is used in the requested structures. Analysis permits ordered
repeated structure indices; coordinate edit callers retain the distinct-index
default. Atom order/repeated occurrences are preserved. Geometric or mass-weighted
centers keep population labels, not invented atom identities. Provided periodic
coordinates are not reconstructed to make those centers whole.

Cartesian versus corresponding pairing, inclusive cutoff versus neighbor count,
and requested versus actually available PBC remain separate choices. Extrema
reuse native tie order. Neighbor local positions map back through their native
endpoint populations; the panel does not implement a distance, cutoff, PBC or
nearest-neighbor algorithm. Positive-cutoff flat inputs use native CSR where
admitted; other native supported output forms keep their own resource behavior.

Only 50 rows travel to the frontend. Pages convert requested native values to nm
through PyUnitWizard, without copying the full result to change units. Flat
Cartesian distance queries explicitly request native block mode. A returned
native disk handle is consumed in pages and retired on Clear, changed context
or unmount. Centers, corresponding pairs, extrema and nearest-count queries keep
their native resource admission; bounded frontend pages are not a universal RAM
limit or out-of-core promise. Current calculation receiving is serial; native
concurrent configuration restoration was separately reported under #613. Its
owner correction is now delivered; combined consumer receiving remains due.

Reports are private to the mounted panel, expire on managed source/input or
dependent structure/scene-membership changes. Calculation never alters
coordinates, chemistry, scene objects or analysis stores. Explicit current-primary requests
remain declared readers while a scene update is pending; old-scene populations
are rejected. Expert Python calls retain complete native results and signatures.
Generic result persistence, plots, further
structural/property/sequence/mechanics families and complete-session acceptance
remain required work; no placeholder operation is registered for them.

### Analysis-to-scene actions — source contract 2026-11-06

A chosen result row offers Select participants, Focus participants and Add live
distance. Python resolves the private report token and global row position
through the same native-axis mapper used by bounded pages. It rejects foreign,
expired, off-page and malformed rows; browser-supplied atom lists are not
admitted. Source identity, managed revision and scene-dependent membership are
revalidated inside the existing host action lock. Reader callbacks only
validate; scene calls occur after they return. These three actions are not
declared readers and remain unavailable during pending/failed synchronization.

Selection uses the unique union of actual participant atoms. Focus uses the
existing core camera owner in the visible structure, enclosing atomic spheres;
it does not promise an arithmetic-center camera target. Neither action seeks
the calculated structure. A live distance uses the full geometric populations,
including repeated occurrences, through core Measurements. It follows visible
structures and stays separate from the immutable calculated row. Core may
compute values across all loaded structures; no new resource bound is promised.
The live Measure survives Clear and addon unmount and retains core history,
visibility and persistence ownership. No frozen scalar is inserted as geometry.

Actual periodic observations and mass-weighted centers cannot be converted to
that nonperiodic geometric live distance; their participant actions remain
available. A requested periodic calculation with no stored box reports its
native nonperiodic fallback and may create a nonperiodic live Measure.

One radio group selects rows by report identity and page. Changed input/page or
result clears it; unchanged context refreshes can retain it. An action's own
selection may expire a current-selection report. Retain the bounded action
acknowledgement while refreshing, without restoring stale drafts or allowing
old scene requests through synchronization recovery. Empty results offer no
invented row. No second public scene-action service or expert wrapper is added.

### Conformation tables and core plots — source contract 2026-11-06

Analysis offers raw RMSD, optimal-superposition RMSD, radius of gyration and
per-atom RMSF through the unchanged public structure wrappers. Calculations
retain ordered/repeated atoms and structures, explicit initial reference
structure and positional atom correspondence. No input fitting, periodic
reconstruction or preparation occurs implicitly. Gyration exposes uniform or
native standard atomic-mass weighting and its unit-policy prerequisites; RMSF
does not align its input and keeps an atom axis across the requested structures.

Mounted reports retain native quantities and send at most fifty source-index
rows per page, displaying nm with nine significant digits. Participant actions
reuse core selection/focus in the visible structure without seeking a result
row. Deliberate plot adoption is separate from calculation and admits only one
finite scalar for each loaded structure, exactly once in canonical index order.
Never pad missing observations, discard repeats, sort requested indices or label
RMSF atoms as structures to obtain a plot. Core owns each adopted card, its
axes, navigation, visibility and lifetime; Clear/unmount does not remove it.
Repeated adoption updates the same report-derived card, and retry reuses the
native result. Relevant source/revision/context changes retire the report;
pending synchronization blocks scene actions while admitting declared readers.

The [conformation receipt](../devtools/data/molsysviewer_tools_conformation_receiving_20261106.json)
keeps independent coordinate oracles, native unit/axis/lifecycle cases and the
17-step actual Jupyter/popup workflow separate from owner, hosted, installed
and postponed human acceptance. Viewer #314 receives actual plot-origin Python
authority and mirrored navigation; local playhead movement alone is insufficient.

### Remaining Analysis integration — planned

Qualify report/context dependencies before offering deliberate row navigation.
The present row actions never navigate implicitly.

Further structural observables and PCA, property/sequence/connectivity and
mechanical results, qualified interaction adoption and other result-axis
renderers remain required implementation/receiving work under #421. Native
expert exposure does not complete those GUI tasks or the full session ledger.
Reuse core owners where the result's actual mapping applies; another axis needs
its own reviewed renderer contract, not an implicit scientific transformation.

### Chemistry preparation and explicit replacement — source contract 2026-11-06

Chemistry offers Add missing heavy atoms and Add missing hydrogens alongside its
unchanged read-only inspection tasks. It delegates through the existing public
build wrappers without changing expert signatures or native defaults. Heavy
completion resolves the shared atom editor to stable group indices through
public basic.get, then processes those groups across all structures. It exposes
native versus PDBFixer engines and the actual strict/intersection admission.
Hydrogen completion makes template/pH approximation versus fixed-state RDKit
explicit. The latter exposes chemical-state and preservation policy; the former
exposes its pH/engine and lack of strict preservation. Both require one source
structure in this panel; no frame/component is extracted implicitly.

Prepared results use the existing host View presentation service. Only bounded
counts, method parameters, software and attribute-availability differences travel
to the frontend. Native preparation history remains in the independent MolSys;
warnings remain observable in Python. Availability differences do not certify
all other attribute values, protonation, geometry or scientific readiness.

Use in this view opens an inline scene-reset/copy review. Confirmation consumes
the token, checks the independent result's object/revision under its molecular
reader and copies it. The source replacement then atomically checks the original
source identity and managed revision through Viewer #306. Source and candidate
checks do not observe raw external writes. The copied candidate is never shared
as a mutable primary with a separately displayed View. Back makes no edit;
successful replacement resets scene objects rather than inventing an atom map.
Load failure keeps the host recovery contract, not a rollback guarantee.

Preparation/replacement/presentation are not declared recovery-sheet readers.
While pending, only the existing exact inspection actions remain admitted.
Leaving a task releases unpresented results; already presented Views survive.
The preparation receipt records actual TcTIM/Jupyter and pending-reader controls;
human Qt/Jupyter, owner integration, installed artifacts and full matrices remain
separate. Further Chemistry assignments/construction, all required Analysis and
the complete-session persistence target remain required in the family ledger.

### Superpose structures — source contract 2026-11-06

The task delegates to public `structure.least_rmsd_fit` through the existing
managed coordinate adapter or independent expert route. It moves the chosen
atoms in all/current/ordered-distinct structures. A same-system reference index
is explicit and refers to the initial pose. Default fit/reference atoms are the
moving indices; advanced expressions choose fixed ascending-index populations
in their declared source/reference structure contexts. Pairing is positional,
user-declared and unweighted; there is no inferred sequence/name mapping.
Fit atoms may be outside the moving set. Native non-collinearity validation
covers the whole request before writes; the GUI does not implement Kabsch.

The qualified GUI route identifies MolSysMT CPU explicitly; expert engine,
external-reference and execution controls remain intact. Shared review tokens,
managed revision locking, coverage, fixed-cell/no-wrap semantics, independent
whole-system results and projection-only retry are preserved. The shared
reference snapshot now groups center/target/fit/reference populations with an
immutable reference index for exact revalidation; no trajectory is copied by
review. Sequence correspondence, principal-axis orientation, further reference
workflows and periodic/cell tools remain pending families, not removed scope.

### Periodic source tasks — qualification 2026-11-06

Wrap coordinates delegates primary-origin, centered-primary and nearest-image
placement with explicit Å/nm reference points and native selected-component or
atomwise grouping. Unwrap trajectory delegates per-atom temporal continuity in
a deliberately supplied sequence of at least two structures. Both retain the
same reviewed current/independent effects, box vectors, selected scope and
projection-only recovery. No periodic formula or chemical preparation is added.

The [bounded source qualification](periodic_tools_gui_qualification.md) admits
exact lower-triangular row-vector cells; temporal unwrapping additionally needs
identical selected cells. These retained consumer controls await receiving of
the delivered native #607/#606 corrections; they are not general physical
definitions. The expert API remains native. The owner has also repaired #608;
combined cross-policy receiving remains due without a scientific addon workaround.
General orientation, changing-cell unwrapping and the cell editor using the
delivered #605 validation remain required before declaring this family complete.
No nonfunctional cell control is registered. The delivered owner corrections
trigger review of these guards, retaining the 2026-11-13 checkpoint. The
[periodic source receipt](../devtools/data/molsysviewer_tools_periodic_receiving_20261106.json)
records the independent lattice controls, 356 affected System/Geometry/PBC cases
and seven actual Jupyter scenarios. The window-title receiving race (#609) is
corrected by waiting for presentation acknowledgement; no runtime or scientific
behavior is substituted to satisfy the harness.

## Chemistry inspection source tasks — 2026-11-06

Inspect stored chemistry and Hydrogen inventory reuse the two public physchem
reports without preparing molecular data. They use one explicit structure
context and a reference, structure-associated or indexed chemical state.
Selections resolve in the reference context; the report audits those fixed
atoms in the stated state. Unknown, missing, conflicting, unsupported, empty
and unassessed results remain native. A stored value is not a chemistry or
readiness certificate; unknown H counts do not become zero.

Only a bounded summary and up to fifty source-index rows cross the panel
boundary. Full native reports remain private to each mounted panel, without a
universal RAM limit or generic H5MSM/result-store promise. Long labels are
shortened explicitly. Paging reuses the report, retains units and native indices,
and never reruns the calculation. Inputs, source revision, structure context
and relevant scene membership expire the report; unmount/Clear releases it.
No molecular/scene/analysis/history operation follows from inspection.

The new read_only_actions capability in uibcdf/molsysviewer#304 admits declared
incoming reader requests under pending synchronization. The addon rejects old
scene selections/regions in that state. The host now temporarily places that already mounted reader inside the
recovery sheet, preserving input/DOM identity and native bounded pages while
the old scene stays inert. Synchronization restores its original Studio host.
Chemistry retires stale requests and only refreshes in admitted states, avoiding
a busy request without a response during editing. Actual Jupyter and both popup
boundaries are received under #304; exact-head hosted/owner/installed gates
remain separate and human visible acceptance remains postponed. The full periodic source dd34c371c completed
4,657 cases before these Chemistry changes; retain that input distinction.

## Whole-session target and task-family ledger — 2026-11-06

**Approved product objective; incomplete.** The maintainer adopts completion of
an actual molecular working session through the expert API and these four task
panels. The ledger below groups scientific tools by user intent; it is not a
promise to expose every native argument as a GUI field. Preserve the full expert
API. Entries remain pending until their own operation/effect and host acceptance
is recorded. A missing native mode is an owned prerequisite, not a successful
GUI result or an automatic post-1.0 exclusion.

| Surface / task family | Reused scientific and host owners | Required receiving |
| --- | --- | --- |
| System inventory, selection, removal, subset and copy | Core System/selection; basic remove/extract/copy; host edit/presentation services | Current three tasks have source and real Jupyter guards. Retain all-structure inventory semantics and independent output ownership. |
| Geometry explicit translation, rotation and centering | structure translate/rotate/center/get_center | Translate and Center implemented with analytical/native/Mol* receiving. Rotate needs the public constructor requested in #602. Preserve centers, handedness, units, selections and actual rendered coordinates. |
| Geometry structural comparison/fitting and principal-axis alignment | structure least_rmsd_fit/least_rmsd_align/align_principal_axes | Superpose structures implements rigid fitting within the current system, with explicit moving/fitting/reference populations, initial reference structure and user-declared index pairing. Sequence-derived matching, principal-axis orientation and other reference workflows remain required work. Preserve native degeneracy/prerequisite errors. |
| Geometry periodic coordinates and cell assignment | pbc wrap_to_pbc/wrap_to_mic/unwrap, public cell factories and admitted basic.set | Wrap coordinates and Unwrap trajectory retain the bounded source profile in periodic_tools_gui_qualification.md. Receive the delivered native general-orientation (#607), varying-cell temporal (#606), reference-point (#608) and factory-validation (#605) corrections; cell editing remains unimplemented. Preserve explicit units/order/effects and native validation. |
| Chemistry readiness and preparation audits | build audit readers, physchem chemical-readiness/H inventory, chemical_states reports | Preserve reference/state and assessed/unassessed scope. Reports do not prepare or assign chemistry. |
| Chemistry explicit repair and assignments | Received build/physchem atom/bond/H/terminal and typing/charge tools | State method/model and prerequisites; use qualified maps for managed edits or independent results. No inferred identity by equal counts/names. |
| Chemistry construction, solvent and ions | Received peptide/water-cell/assembly/solvation/add_ions tools | Explicit independent inputs, charge source, model, box, seed and placement limits. Construction may start without a loaded primary; no implicit equilibration. |
| Coordinate refinement | Native molecular_mechanics potential_energy_minimization | Explicit model/engine, native single-structure admission and independent/current effect; no hidden parameterization or global-minimum promise. Final panel placement follows this edit intent. |
| Analysis geometry, neighborhoods and structural series | Received distances/vectors/angles/torsions, neighbors/contacts, RMSD/RMSF/radius and PCA tools | Independent numerical controls, explicit reference/weights/PBC/structures, native local/global index maps and units; bounded summaries/pages/plots. |
| Analysis properties, sequence/connectivity, interactions and mechanics | Received physchem, topology, chemical_states, interactions and energy readers | Tables versus calculations stay distinct; scientific prerequisites, evidence, engine and evaluated scope remain visible. Core Interactions/Measures/colors/plots own visual adoption. |
| Saving and recovery | Core Load/Export/session services plus actual MolSysMT format capabilities | Recover molecular data, supported named interactions and scene through their owners. Independent generic results retain their actual native format contracts. |

A task family may contain several understandable operations or method choices;
implemented forms must identify the qualified inputs and limitations precisely.
Required families cannot be silently dropped because another family is easier
to render or because an old subset of tests passes. Keep API exposure distinct
from complete graphical/effect qualification and source distinct from installed
availability. Do not add placeholder panels for the rows above.

### Scientific session acceptance

1. Load bundled TcTIM / 1TCD and record source identity, atom/group/structure
   counts, molecular selection and the default scene. Receive the PDB-ID route
   separately where networking applies; no live download is needed for local
   deterministic guards.
2. Inspect/select categories or arbitrary atoms, review and remove an explicit
   population, extract a subset and create an independent copy. Verify exact
   retained coordinates, inventory and scene/reference remapping.
3. Inspect chemical readiness before an analysis that needs missing chemistry.
   Run a deliberately chosen qualified preparation with explicit state/method
   and destination; inspect its report and input/output correspondence. Do not
   silently add hydrogens or choose a force field to obtain a desired result.
4. Apply a coordinate transform and a reference-based comparison/alignment.
   Supplement TcTIM with three distinct pentalanine conformations and structure
   order [2,0]; verify unselected structures/atoms and the stated cell effects.
5. Calculate representative geometric, property and interaction results,
   inspect units/method/evidence/coverage and deliberately add qualified visual
   content through its core owner. Missing prerequisites, zero results and
   unevaluated structures must remain distinguishable.
6. Preserve the resulting molecular system and supported analyses in an actual
   native-supported format (H5MSM recommended), and preserve scene state through
   the Viewer owner. Reopen and compare inventory, coordinates, structures,
   coverage, scientific parameters/units and recoverable scene objects.
7. Exercise the same resolved operations headlessly and through Jupyter, the
   canvas popup and detached Studio; retain applicable native Qt observations
   separately. Check error/retry behavior and source/result lifetimes. Human
   visual acceptance remains explicitly postponed, not inferred from automation.

**Headless session receiving — 2026-11-06:**
`tests/molsysviewer_molsysmt/test_scientific_session.py` now receives real TcTIM
removal/coordinate analysis/H5MSM and scene recovery plus nonempty pentalanine
observations under the unchanged native 0.23 nm Buch criterion. It independently
checks H-A distances, complete native records and evaluated-empty/unevaluated
coverage. The later Viewer #307 fixes numeric selector metadata; native #616
prevented compatible-source append at that checkpoint. The owner has since
delivered its correction; combined session receiving remains due.
This is a partial expert/source checkpoint, not completion of GUI steps 1–7 or
all required families. Its evidence stays distinct from the clean 4,775-case
8f8c442e collection on the earlier host.

Independent analytical fixtures supplement the real-protein workflow. Native
parity alone is not a scientific oracle. Reproducibility does not introduce a
general scientific-result store, observation of arbitrary raw writes, molecular
Undo, or the previously deferred Copy Python feature. Keep broad documentation,
owner integration, exact installed qualification and publication as separately
executed gates; both 1.0 publications remain paused.

## Evidence and implementation gates

The offline [interaction prototype](../devtools/prototypes/molsysviewer_tools_workspace.html)
uses explicitly labelled static counts from bundled TcTIM 1TCD. It demonstrates
navigation, narrow/wide layout and inline review, with no kernel, molecular edit
or capability qualification. Its buttons must not impersonate live calculations.
The accompanying receiving record identifies exact source/data and the separate
headless native-flow exercise. A screenshot is design evidence, not a Qt test.

Implement in vertical slices after review of this design:

1. Shared panel shell, lifecycle/state protocol and read-only selection review.
2. Removal with atomic review validity, immediate edit projection and recovery.
3. Extraction/copy results with qualified presentation/delivery destinations.
4. Geometry, Chemistry and Analysis tasks using already received capabilities;
   qualify each method/effect rather than adding one button per native function.

For the first slice verify real native/demo systems and click-to-Python execution:
empty/no-match/invalid/all-atom input, a loaded 1TCD, multi-structure water fixtures,
nonconsecutive structures, scene remapping, repeated/no-op submission, pending
edits and failed projection, stale revisions/replacements, independent view
lifetimes, addon disable/re-enable, drafts, popup navigation and late responses.
Test keyboard access, focus, errors, scroll and compact/large layout separately.
Retain actual Jupyter and visible Qt observations; headless browser layout tests
are not substitutes for those hosts. CI/source/installed evidence stays separate.

The local actual-Jupyter receiving runner creates a private loopback server,
source-bound kernel and named workspaces. It exercises real anywidget comms,
Mol* rendering and both popup lifecycles, compares browser errors with a plain
notebook control, and shuts down its own server/kernels. Run with the qualified
Python 3.14 interpreter from this repository:

```bash
python tests/molsysviewer_molsysmt/system_panel_jupyter.py \
  --viewer-root ../molsysviewer --output /tmp/molecular-tools-jupyter-receiving
```

Use a new output directory. `--provider-root` may select the explicitly recorded
public PyUnitWizard snapshot when required by the receiving profile; it does not
install or change a provider. `--node` and `--chromium` name the inspected local
tools. Retained private server logs are not publication-ready artifacts. Actual
Jupyter transport evidence remains distinct from human visual acceptance,
visible Qt/GPU observation and clean installed-package qualification.

The same browser boundary has an explicitly selected pytest guard at
`tests/molsysviewer_molsysmt/jupyter_receiving_guard.py::test_actual_jupyter_review_and_independent_popups`.
Set `MOLSYSVIEWER_ROOT` and optionally `MOLSYSVIEWER_PROVIDER_ROOT`, then run
that node with `--receptor=llm` in the qualified GUI environment. This separate
local GUI lane is not part of the default scientific filename collection;
missing Jupyter/browser prerequisites fail rather than producing a skip.
