# MolSysViewer tools guide content contract

Preserve explicit molecular_mechanics.get_engine_forcefield resource lookup
without a primary or engine execution, and serialized primary-bound
get_degrees_of_freedom and get_potential_energy with native OpenMM parameterization and prerequisites.
Keep the 3*N_particles-N_constraints integer definition, absence of COM/thermal
corrections, explicit one-structure receiving and no implicit visible-frame use.
These queries do not adopt engine objects, prepare chemistry or change the
scene/history. Keep the native shared-resource-list limit (#560) and unsupported
platform contract (#559) explicit until their owner repairs are received.
Native result ownership and errors are delegated; do not silently copy a
registry list or add the other two mechanical functions without qualification.
Energy selection constructs a parameterized subsystem, not an embedded energy
contribution. Preserve native quantity/unit-policy and force-name decomposition
contracts, explicit single-structure CPU receiving, the independent OpenMM
reference and native defaults, chemistry, periodic and optional-engine limits.
Do not introduce implicit frame iteration, preparation, engine adoption or a
scientific platform fallback. Keep pending reads independent of scene sync.

Preserve native potential_energy_minimization with independent output by default,
managed retained-axis in-place coordinates and keyword-only update_view and
local skip_digestion. Native validation is never bypassed. Keep independent
result ownership, explicit single-structure CPU/model prerequisites, native
analysis invalidation and synchronization-only retry after completed science.
Do not invent tolerance/selection/frame arguments, global-minimum guarantees,
preparation or implicit adoption. Scene history is not molecular Undo.

Preserve the four explicit supported-capability reports and their open-empty-view
contract. Keep native filters/default Styler and explicit plain outputs, directional
syntax flags, independent metadata, closed-owner rejection and unchanged pending
edits/scene/history. Declarations and dependency reports are not execution or
installed-pair certificates. Do not bind a molecular system or add update_view.

Preserve the explicit attribute-metadata namespace and open-empty-view contract.
Keep raw canonical membership distinct from alias reporting and native validated
classification, overlapping categories distinct from domain availability, and
stored stable inventory distinct from state-local connectivity or conversion
inference. Utilities must not read/synchronize the primary or alter scene/history;
addon-only keyword digestion controls are not forwarded to flag-free native tools.

Preserve the distinction between the initial experimental source API and
published package compatibility. Keep the explicit qualified-tool inventory: six queries, native extraction and managed native removal and geometry-only setting with synchronization controls, plus native copy, conversion/preflight, composition predicates and non-mutating comparison.
Update it only when more tools are implemented and qualified. Explain the bound primary system,
native parameter/return/validation behavior, automatic entry-point discovery,
replacement/close semantics, the native independent/in-place distinction, pending
synchronization/recovery and the absence of task panels and other editing families. Link native tool references and Viewer host/author documentation.

Preserve the explicit secondary comparison input and the separation between
read-only comparison and the unreceived two-system topology rebuild. Keep native
argument aliases and duplicate-name rejection; never reinterpret a mutating
comparison as an ordinary query.

Preserve bound identity/attribute-owner queries and the explicit-input collection
utility. Document keyword-only addon digestion controls separately where native
helpers deliberately lack digestion. Never insert the current MolSys into an
explicit collection, promise automatic locking for caller-owned utility inputs,
or present a returned native owner as a copied result.

Preserve the received chemical_states graph namespace, topology sequence namespace and exact native output/state/selection
contracts. Graph cuts are analytical and never delete molecular bonds. Keep
ragged quartet blocks as native lists/sets, no implicit visualization or chemistry
preparation, and distinguish declared native skip flags from addon-only controls.
Do not advertise unreceived tools or invent root aliases.

Preserve the eleven tools across nine chemical_states graph and two topology sequence exports,
with optional RDKit/Biopython routes, chemistry prerequisites, search limits and
native independent reference ownership. The native sequence/group fix is now
received: preserve contributing source-group mapping and the declared native
keyword-only validation flag without an addon-specific identity formula.

Preserve the received structure readers, native physical quantities,
independent secondary systems, output metadata and explicit periodic/weight/engine
choices. Never treat centers as coordinate edits or silently correct native
heavy routes. Preserve the received native endpoint/unit fixes with independent
numeric checks; distinguish scientific references from mere native parity.

Preserve the four additional independent structure readers: raw/minimum RMSD,
principal axes and least-squares planes. Minimum RMSD does not fit either input
in place. Keep references caller-owned, axis/moment arrays native, plane results
separate from shapes and rich-selection/optional-engine limits explicit. Retain
the source receipts of #441/#442 and actual package-compatibility limits.

Preserve the received maxima/contacts/RMSF paths and their native index, threshold,
unit and non-editing contracts. Preserve the locally received minimum/neighbor
wrappers, independent weights/reference systems, local endpoint positions and
native criterion admission. Distinguish working-tree receiving from the provider
commit, issue closure and published package compatibility. Keep the native pytest
family matrix visible; never repair scientific forwarding inside the addon.
Historical receipts remain immutable.


Preserve the received structural-analysis readers and their separate contracts.
Secondary-structure numeric selections address groups and retain native sorted
unique output; MDTraj is explicit. Symmetry-corrected RMSD retains declared
chemical prerequisites, RDKit, search-scope bounds and attribution without any
alignment or periodic repair. PCA retains row eigenvectors, squared-length units,
weighted population covariance, dense-memory and degeneracy limits. Preserve
actual provider input/engine qualification; do not normalize or prepare science
in the addon to conceal a provider defect.


Preserve the native translation default/return and independent-output ownership.
Keep in-place synchronization controls separate from native mutation, exact
selected-scope invalidation and retained scene identities explicit. Document
pending work, rejection/uncertain states and synchronization retry without
scientific replay; never substitute system replacement for managed geometry.


Preserve the first seven physchem property readers, native atom/group scopes,
units and containers, explicit definitions, missing-table errors and the
separation between tabulated group charge and parameterized partial charge.
Keep OpenMM form/box prerequisites and pending-reader behavior visible.
The native selection/scope repairs are now received: preserve positive syntax
checks and explicit unsupported-level rejection. Do not present pending physchem
exports as received or introduce implicit coloring, preparation or assignment.


Preserve all thirteen received physchem paths, including ProtOr type/rule arrays,
native radii and four reference tables. Preserve the native provisional ISA area
quantity and standardization, with original-paper verification still open under
uibcdf/molsysmt#473. Keep the remaining raw-table units, Janin reference
percentages, Grantham relative values and the unverified Collantes unit label
separate from geometry/SASA. Preserve addon-only digestion for get_volume and
no invented syntax parameter for get_area_buried. Native PBC repairs now receive
orthogonal factory defaults and centered in-place publication; remove the old
temporary-rejection claims without introducing a downstream scientific repair.


Preserve the separate conformational SASA reader and all-atom occlusion contract.
Keep the #478 squared-unit contract and #479 explicit Cartesian/MIC engine
limits visible; bounded CPU receiving does not qualify arbitrary-cell surface
accuracy, GPU execution or installed artifacts. Do not add scene effects or hidden preparation.


Preserve both detached stored-chemistry reports, explicit single-structure/state
selection, sorted unique indices and typed empties. Keep unknown inventory counts
at -1, indexed/virtual H separate, full-graph auditing and incident/crossing bonds
explicit. Do not interpret availability as chemical validity or introduce repair,
assignment, a universal ready flag or a file-backed view query promise.
Preserve positive default-reference readiness syntax receiving under
uibcdf/molsysmt#480 and the separate restrictions for explicit/associated states.


Preserve the separation between stored aromatic-ring memberships and detached
RDKit-model perception. Keep full-graph prerequisites, explicit declarations,
whole/fused ring selection, packed source axes, nonunique basis and block bounds.
Perception neither assigns flags nor prepares the stored-ring reader. Preserve
internal-bond output filtering, model attribution and received native #482/#483 reference/frame contracts
without downstream scientific workarounds.


Preserve the three received chemical-feature readers: sparse formal-charge
centers with distinct participant/reference memberships and elementary-charge
quantities, typed hydrophobic atom sites and ordered halogen donor/reference
pairs. Keep full-source matching, explicit chemistry/state requirements,
complete-center versus complete-pair selection, match caps and native
attribution separate from interactions and rendering. Default/None-reference MDTraj
works for all three readers after native #488; explicit/associated SMARTS states
retain their selector restrictions. No selector
rewrite, implicit preparation or scene synchronization. The current reviewed
inventory has 34 native physchem exports after lipophilicity was added; 25 have
wrappers and nine remain pending; lipophilicity is now explicitly received. The earlier 02671792f gate retains its 31-export baseline; the new reference-
scale receiving uses its own 32-export source. This is source exposure,
not installed or universal scientific qualification.


Keep #490's reference-metadata ownership limit explicit for the 02671792f
qualification baseline: independent numeric arrays and primary/scene preservation
do not establish independence of every metadata dictionary. A native repair
needs its own receiving; never silently deepcopy results in this consumer or
claim the older green source gate qualifies later metadata changes.


Preserve native group-only bulkiness and secondary-structure propensity lookups:
area quantities versus raw dimensionless frequency-ratio arrays, required
conformation, explicit scale definitions, ordered/repeated/scalar/empty group
axes and strict unsupported-name handling. Do not silently remove caps, invent
parent mappings or aggregation, normalize ratios, predict/assign structure or
color the scene. Keep lookup coordinate independence distinct from rich-selector
coordinate needs. Retain native optional attribution without duplicating credits.


Preserve the native TPSA mirror and all received contribution levels: native squared units,
N/O versus N/O/S/P choice, complete molecule order/repetitions/scalar/empty maps,
state/structure scope and optional detached report/provenance. It is a graph
descriptor, not geometric SASA or a permeability prediction. No fragment capping,
implicit aggregation, chemistry/hydrogen preparation, engine fallback, adoption, color or
synchronization is added. Retain strict native chemistry/boundary validation and
actual optional-provider limits. Keep source receiving distinct from scientific
accuracy and published package compatibility.

Keep the explicitly RDKit-read caffeine example and declared hydrogen inventory.
Native SDF sources with unspecified CTAB evidence retain rejection; do not infer
missing hydrogen counts. Preserve source-qualified #494/#495 repairs: inherited molecule identity,
MDTraj target-only placeholders, stable source order and absent native hierarchy.
No consumer workaround or biological identity inference is added. Keep #499's received atom-growth repair separate from read-only calculations;
unknown appended chemistry remains unknown/partial and may be rejected.


Preserve the explicit get_lipophilicity mirror and both descriptor output/context
contracts: seven element levels, source order/repetitions, scalar system sums,
empty shapes, complete parent chemistry and separate element_* versus molecule
maps. TPSA retains squared area units and N/O versus N/O/S/P; lipophilicity
retains dimensionless float64 values, negative contributions, formally charged
sites and the limits of logP/logD applicability. Document indexed/nonindexed H
attribution without changing source H or atom indices. Keep exact native
state/structure, selector, provider, provenance and optional attribution semantics;
no preparation, neutralization, counterion removal, fallback or scene sync.


Preserve the explicit AutoDock, CIP and partial-charge expert mirrors: required
scheme/model parameters, keyword-only coordinate inference, native sorted unique
atom outputs, full graph before selection, state/structure resolution, units,
providers and provenance. Do not prepare H/protonation, assign results, color or
synchronize the scene. Keep native force-field/template and charge-standard
limits explicit. The source-qualified #503 nested CIP author-list defect remains
visible until an owner repair is received; no consumer deepcopy or claim of full
nested ownership is permitted. The three reader help/doc examples remain native
contracts; tutorial links describe their scientific definitions.


Preserve all 34 explicit physchem paths at the recorded baseline, including
whole indexed waters, bounded metal/ligand roles, explicit template/context maps,
independent template application/aromatic normalization and the explicit-input
coordinate-free peptide factory. Do not conflate source, returned copy and scene
adoption. Preserve native copy costs, history/index domains, invalidation, unknown
chemistry, required scientific choices and no automatic primary/visible-frame use
for explicit-input factories. The initial three build diagnostics select native
group/atom scopes and one structure explicitly; candidates remain unassigned.
Retain the legacy pentalanine chain-metadata limitation and positive 181L route
until the data contract is independently resolved. Broad API inventories measure
source exposure, not scientific or installed qualification.


Preserve the eight additional build diagnostic readers and their native scopes.
Group-index audits, source-atom bond pairs, selected-subsystem sequence insertion
positions and the single structure_index must remain distinct. Missing sequence
reference warnings and empty reports do not certify completeness. Standard-name
suggestions never replace groups; sulfur candidates never insert covalent bonds.
Hydrogen presence and water-density predicates are not chemical preparation.
Keep addon-only keyword digestion controls explicit where native readers lack
that parameter, and preserve the native multi-structure solvation limitation
until an owning scientific repair is independently received.


Preserve the explicit interactions.hbonds expert path and the distinction between
legacy roles, full-graph site recognition, local directional hypotheses and actual
detection. No named attachment or scene effect is implicit. Keep indexed-H and
selection differences, scientific profiles, chemistry prerequisites, unsupported/
undefined status, repeated structure positions, origins' units, row-box support
images and bounded-estimate limitations visible. Native mutable-list/external-rule
and empty-path/frame-validation limits remain native until separately received.
Do not weaken the expert API or introduce a scientific repair in the facade.


Preserve the three raw hydrogen-bond detectors and disulfide-candidate family,
their exact native output defaults, tuple/ragged ordering versus sparse coverage,
selection/profile/site-array and secondary-system limits, provenance, physical
units and observed PBC images. Results remain independent from named storage and
core visualization. Named analysis maps use the native validated setter, not
mutation of a read-only map. Keep eager and budget limits explicit; no universal
RAM, preparation or covalent-assignment promise follows from thin wrappers.


Preserve the three explicit ionic, hydrophobic and halogen detection mirrors.
Keep ionic's required unit-bearing cutoff, compound whole-center selection and
formal-charge geometry references distinct from partial charges/energy. Keep
hydrophobic canonical unordered pairs and native SMARTS profile distinct from
scales/fingerprints/Mol* rules. Halogen selection includes all D-X-A-R roles;
retain two angular intervals, reference-neighbor identity and chain MIC images.
Preserve chemical prerequisites, optional RDKit, three calculation scope modes,
sorted/deduplicated structure coverage, declared units, estimates and resident
sparse-output limits. Legacy incomplete demo data must reject without hidden
preparation. These independent analyses do not attach, edit or update the scene.


Preserve all fifteen explicit canonical interaction function paths at this source
baseline, without equating source exposure with universal qualification. Metal
roles are directed proximity candidates, independent from stored dative bonds or
coordination assignment. Aromatic methods/profiles keep whole participants,
different plane/reference definitions, NaN meaning, native periodic rejection
and the custom four-cutoff proposal. Water order is exactly one or two indexed
mediators with six/nine actual leg roles; preserve alternative H paths and shared
oxygen images. Keep native selector limitations and resource/provider boundaries
visible. Do not add implicit chemistry, virtual H, unwrapping, storage or scene
updates. Extend course prose without changing declared notebook schemas or
existing cell IDs, code and outputs; validate raw stored schemas.


Preserve primary-bound independent permute_atoms and explicit compose_atom_maps:
full new-to-old bijections, native domain remapping, historical axes, generated
versus representative lineage, detached reports, resident-output limits and no
implicit adoption. File tools retain Python-process paths and explicit caller
layers/text; only h5msm.write binds the current primary through its serialized
reader. Preserve partial/absent/empty distinctions, named analyses, mechanics
rejection, legacy-source preservation and native append/overwrite limits. FASTA
readers preserve raw occurrences/newlines and decoded-character spans without
sequence admission, topology construction or an optional Biopython import.
Keep all file results independent of scene load/save/synchronization.


Preserve the four explicit composition mirrors: current destination only for
add/append_structures; complete caller collections for merge/concatenate.
Keep native True in_place defaults, None returns, independent output ownership,
keyword-only update_view, per-system list versus common-array conventions and
complementary source items. Preserve native atom/structure order, chemistry/state,
box/attribute/mechanics and analysis limitations. Receive prefix identities,
new-origin/source accounting, deferred composition and recovery through the
host axis_growth capability, without a full candidate-preparation framework.
Do not invent new per-structure visual values or repeat completed science.
Keep native #520 partial-publication receiving separate from successful implicit
state/no-analysis cases, and distinguish missing-coordinate synchronization
failure from uncertain scientific writes. Installed compatibility is separate.


Preserve the eight explicit element utilities: two element-level predicates,
four atom symbol/name/force-field/isotope helpers and two group-label helpers.
They work on an open empty view without a primary reader or scene/edit effects.
Keep the element-name composition relation distinct from basic's actual-system
predicate and root alias. Preserve canonical case, native D/T/isotope and
AutoDock4 contracts, public group-name lookup/unknown markers and native errors/
warnings. Four addon-only skip controls remain keyword-only and are not sent
to native functions lacking that parameter.

Preserve the nine current-primary chain/entity readers and their managed-reader
binding, including completed pending edits without scene synchronization. Keep
native output-level defaults, IDs/unknowns, containers, selection and redefine_*
projection semantics without molecular assignment, an update_view parameter or
new root aliases. entity.get_n_entities consumes only its keyword-only local
skip control; other native skip flags are forwarded. Require a loaded open
owner.

Preserve the twelve additional primary-bound paths: five molecule, five
component, group type and the legacy small-molecule/amino-acid name heuristic.
Keep stable molecules distinct from reference-state ChemicalStates components,
native selectors/defaults/unknowns, returned projections without assignment, and
missing-domain/error behavior without implicit chemistry or frame-state choice.
The count helper consumes its local skip flag; other declared native flags pass
unchanged. The legacy helper is a catalogued name plus five atom-name checks,
not chemical or stereochemical validation or stored preparation; its group_name
stays explicit and its keyword-only skip control is local. All reviewed element
source paths are now exposed, with qualification separate from exposure.


Preserve fourteen additional explicit name/type/code helpers with open-empty-view
lifetime, native scalar/case/error behavior, and locally consumed keyword-only
skip controls. They do not read the primary system, normalize science, prepare
chemistry or synchronize scene/history. Name recognition is distinct from
system classification; standard-name lookup preserves None for canonical or
unmapped labels. Preserve received canonical XLE/J and XAA/X and the protected
peptide-end convention (ACE at N; NME/NHE/NH2 at C). Keep legacy protonation-name
semantics (MolSysMT#549) explicit without addon substitution. Keep inherited
native examples executable.


Preserve all fourteen explicit group-template queries: seven bond helpers, five
family database readers and expected amino-acid heavy/hydrogen names. Explicit
index labels do not refer to the primary; no graph inference, chemistry repair,
protonation, cache, normalized database schema or scene publication is added.
Retain native template fallback, family support, container/order/error behavior,
caller chemical context and fixed pH-rule limits. Native skip controls pass for
amino-acid/ion bonds; the other twelve controls are local and keyword-only.
Keep protected peptide-end classification separate from explicit template data
access and from attaching atoms to a system.
Preserve received native flat-name array/list/tuple support for the three
reference families and their dispatcher, with actual positive pair controls and
native ArgumentError for invalid dimensions. The addon introduces no coercion
or native-validation bypass. Preserve the received #554 index-map validation:
one nonnegative unit-free int64-range integer per name, repeated labels allowed,
structured argument/length diagnostics, valid readonly/strided and empty maps,
and native scalar compatibility. Explicit map labels are not primary-system
selections. Native skip flags retain trusted-caller semantics; local addon
flags do not disable native validation. Keep legacy name semantics under #549
and source receiving separate from installed compatibility.


Preserve the three independent build routes: infer_covalent_bonds,
assign_autodock_atom_types and assign_partial_charges. Bind the current primary
through the serialized reader, retain explicit methods/states/structures/native
validation, and never adopt results or publish scene/history automatically.
Distinguish inference evidence and output-only invalidation from mechanical
assignment snapshots. Keep the single-state restriction, required scheme/model,
optional providers, provenance and elementary-charge storage, H5MSM 0.5 mechanics
exclusion and materialization limits explicit. Pending reads do not synchronize;
independent outputs require deliberate chaining or replacement.


Preserve project_atom_names as primary-bound independent label projection:
required export constraint, no file write/output-format conversion or adoption,
full axes/IDs, original/projected names and identity maps with native composition.
Keep lexical collision scope distinct from chemistry and never recertify stale
assignments. Native mutable domains detach while protected geometry can stay
shared until a public edit. Keep pending reads and replacement/close behavior
consistent with the other independent build routes.
