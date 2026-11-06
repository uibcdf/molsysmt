---
summary: Preserve a prepared PDBQT representation while projecting explicitly mapped coordinates.
issue: uibcdf/molsysmt#599
status: active
opened: 2026-11-06
closed:
verification: measured
area: [form, structure, build, data, docs]
guard: tests/form/file_pdbqt/test_coordinate_projection.py
normative:
blocked_by: []
supersedes: []
---

# Prepared PDBQT conformation projection

## What

Support explicit coordinate replacement on an actual prepared PDBQT representation,
retaining atom fields, declared torsion-tree meaning, source/output lineage and
source immutability. Both complete known-native preparations and external partial
PDBQT references remain in scope. DockingMT owns scoring, study decisions and state
selection; MolSysMT owns general representation, units, correspondence validation
and serialization. No downstream parser/coordinate writer is required.

## Existing public composition and measured limits

Inspected main 882b65b9c after the preceding twelve ordered closures. Native
`copy` plus atom-level `get/set` already replaces coordinates without changing
source chemistry or original geometry. Public native PDBQT writing accepts a
supplied ROOT/BRANCH tree even when chemistry is partial; complete graphs receive
additional independent tree consistency checks. Therefore this feature must not
require or invent complete chemistry for external PDBQT input, or weaken the
complete-context known-source `read_poses` contract under #226/#521.

The existing writer deliberately canonicalizes charges to three decimals,
occupancy/B-factor fields to two decimals and molecular record presentation.
Native conversion deliberately omits format-level remarks/tree storage. A public
native copy/set/write probe on independent rigid and flexible fixtures with a valid
8-character charge field 0.123456 produces 0.123 and drops the original Vina score
REMARK. Native connectivity remains partial and source coordinates are unchanged.
This is documented writer normalization, not a newly alleged writer bug; it proves
that the composition alone does not preserve every supported prepared field.
The local receipt is `.pytest_cache/599-existing-composition-probe.json`.

## Reusable owners and implementation direction

- Reuse `PDBQTFileHandler`, its validated resident/indexed document and MODEL grammar.
  Opening already validates every source model, invariant atom fields and trees.
- Keep native copy/set/write as a documented supported composition when its explicit
  canonical normalization is acceptable. Do not wrap it in a fake complete-state
  claim or infer a map from counts, names or source array order.
- The format-owned `project_coordinates` route is now implemented through the
  handler and thin file/text form functions. It delegates to one shared private
  field-projection kernel, without native chemical reconstruction.
- The shared implementation changes only the fixed coordinate columns of original
  validated atom records. Charges, types, IDs, names, grouping fields, occupancy,
  B factors, record kinds and ROOT/BRANCH/TORSDOF records are retained. Do not
  duplicate the chemical parser or reconstruct atoms through native chemistry.
- Reuse ArgDigest coordinate normalization and strict positional-axis/map tools;
  retain public `skip_digestion`. Private helpers remain undecorated. Convert the
  serialization boundary explicitly through PyUnitWizard to angstroms, independently
  of the application policy. Keep nonfinite/width errors typed through SMonitor.
- No optional scientific engine is needed. Reuse the actual parser/writer primitives;
  no new dependency or Rust routine is justified by these formatting operations.
  Retain original scientific provenance as declarations and actual producer metadata;
  never credit an engine merely because its name appears in an input REMARK.

## Contract to implement and verify

1. Require an explicit complete bijective correspondence between the supplied
   coordinate atom axis and source PDBQT atom positions. Preserve both full axes.
   Reject missing/duplicate/invalid indices, booleans, quantity-wrapped indices,
   wrong dimensions, incompatible units and nonfinite values. An omitted H must
   not inherit an old or parent coordinate and appear to be an observed pose.
2. Associate each replacement structure with an explicitly selected source
   structure. Retain order, actual source indices and source MODEL labels,
   independently of coordinate-array positions. Serialized structure selections
   retain the existing nonempty/unique rule. Bounded serial projection of many
   new conformations from one reference is supported without a study/cache API.
3. Preserve arbitrary valid source charge precision and all noncoordinate atom
   fields. Coordinate rounding/field limits must be explicit and measured. Never
   neutralize, protonate, repair, retype or renormalize charges during projection.
4. Make REMARK disposition explicit, including stale score annotations. An output
   must not silently present an old score as a new evaluation. Preserve original
   input identity/provenance in the report, and keep known chemical-state
   provenance as a caller declaration rather than a reconstructed state store.
5. Return detached prepared text or write through the existing staged/atomic
   file route, with a typed report containing input/output payload digests,
   atom/structure maps, source labels, units, precision, metadata disposition
   and software. String form-prefix bytes and molecular payload bytes must be
   distinguished in the hash contract. No source object/file is modified.
6. Validate adverse later source models and replacement structures before
   publishing a result. Preserve existing destinations on failure; reject
   indexed-source changes and output paths aliasing the source. Indexed/file
   output must avoid whole-source/whole-output text materialization. Describe
   coordinate-input, model-buffer, report and result-string memory separately.
7. Exercise rigid and nested flexible references, partial input chemistry,
   nonidentity atom maps, nonconsecutive structure selections, ordinary and
   nondefault unit policies, malformed maps/units/coordinates, fixed-field
   overflow, stale annotations, source immutability and later-model failures.
   Reuse pinned real Vina examples as format controls, without executing new
   docking searches, scoring or claiming biological acceptance.
8. Update public docstrings/doctests, User Guide, Cookbook, course, native/form
   contracts and API registry. Retain the experimental boundary. Run relevant
   source/provider-floor, lifecycle and lint gates before publishing/closing.

## Why

A prepared representation is more than an array of positions. Existing native
operations are useful reusable pieces but intentional format normalization can
alter fields that a rescoring workflow must hold fixed. A bounded operation in
the format owner can preserve those fields without a consumer molecular utility,
complete-graph guess or duplicate chemical store. Source association remains a
declared correspondence, not authentication by matching counts or hashes.

## Scope and limits

This is molecular representation editing and evidence, not docking execution,
chemical-state prediction, force-field selection, ranking, H generation or a
new trajectory format. #521 and #447 retain partial reading and cross-pose identity
assessment respectively. #600/#601 follow this work in the accepted fifteen-issue
order. Full release-pair and platform qualification remain separate from these
native/form contracts; no release, tag or package upload is authorized here.

## Shared validation prerequisite — 2026-11-06

Before introducing the projection API, strict-map controls expose five unsafe
acceptances in the existing shared atom-correspondence digester: Python/NumPy
booleans hidden by integer coercion, an unsigned index outside int64, and whole
or scalar quantity-wrapped indices. Two further controls specify new detached
int64 canonicalization, rather than alleging that earlier int32/uint32 returns
violated a published dtype promise. Seven of ten initial controls fail; three
pass. The original unit-wrapped array also emits a unit-stripping warning.

The shared digester now rejects these invalid values before coercion, reusing
existing unit/axis semantics, and returns independent signed int64 pairs. Ten
new controls plus existing peptide/template/context/EST/receptor contracts pass:
226 cases, no failures or omissions. This remains unpublished source on the
#599 branch at that prerequisite checkpoint, before project_coordinates existed. The measured
receipts are `.pytest_cache/599-shared-map-before.xml` and
`.pytest_cache/599-shared-map-after.xml`. The existing public helpers, their
form-agnostic behavior and optional providers remain the intended reusable path.

A complete paginated owner inventory at this checkpoint contains 549 issues:
443 closed and 106 open, with no issue numbered above #617. This observation
is not a reason to widen the accepted fifteen-issue goal. The new classifier,
model-merging, GRO context and catalogue/widget lifetime closures remain published
on main 882b65b9c. Their live board states have been independently rechecked.

## Implemented and contract-tested — 2026-11-06

The public handler method and file/text form functions now require exhaustive
coordinate-input/source positional atom pairs and explicit real length quantities.
Coordinate blocks align one-to-one with the unique selected source structures.
Partial external references remain partial; no complete source graph, H fallback,
typing, charge calculation or third-party scientific engine is used. Non-coordinate
atom columns retain their original characters; nested tree records retain meaning.
Original MODEL label lexemes are retained, while numerical aliases still trigger
the original duplicate-label refusal.

The default refuses all REMARK-bearing sources until discard_remarks=True is
explicitly supplied. This removes every remark, including stale scores and
unselected/global/trailing annotations. A detached typed JSON-compatible report
retains exact input/output payload digests and byte counts without the form prefix,
both atom-axis directions, selected source structures/labels, explicit angstrom
field precision and measured per-structure error, converted-coordinate digest
encoding, caller-declared state provenance and actual producer version metadata.
MODEL wrapper whitespace is canonical; inter-model blank lines and a terminal
document END may be omitted. Hashes and declarations are not authentication.

File output reuses PDBQTDocument.write_chunks and one-model source reads, with
destination alias refusal, indexed source-change checks and atomic replacement
only after completion. Input coordinates, source/index metadata, maps/report,
model buffers and any full string have separate memory costs. Estimated buffer
limits are checked, without a total-RSS or constant-time hash/opening claim.

Verification on Python 3.14, with the published Pytest Receptor and twelve workers:

- **392 affected tests/doctests pass**, no failures or omissions. They include all
  PDBQT file/handler/indexed/known-source/presentation/real-example tests, shared
  atom-map controls, naming/H-merge/map consumers, the tutorial/course guard and
  all three public projection docstrings. Five pinned real Vina preparations,
  including a receptor, retain every non-coordinate atom field under explicit
  nonidentity coordinate maps; no new search or scoring experiment is executed.
- **80 cases pass with all five published provider floors**: ArgDigest 0.14.0,
  DepDigest 0.15.1, SMonitor 0.16.0, Ackredit 0.9.0 and PyUnitWizard 0.28.1.
  Only the incompatible development pytest SMonitor plugin is disabled on that
  route; runtime diagnostics and public validation remain active. No environment
  is created and no provider is installed or edited.
- **14/14 fast gates**, Ruff checks and formatting pass. Form APIs inherit the
  existing Experimental subtree policy; no stable namespace is promoted.
- The complete modified **Module 10 executes successfully** through the quiet
  notebook runner on an isolated copy. Only the new cell output is received;
  all 22 previous cells, their outputs and notebook metadata remain unchanged.
  The first isolated kernel startup was blocked by sandbox socket permissions;
  the authorized local-kernel route passes. The public tutorial's two blocks and
  new course code are also executed by the addressable documentation guard.

Retained local XML: `.pytest_cache/599-affected-final.xml` and
`.pytest_cache/599-five-provider-floors.xml`. The first 48-case draft had thirteen
test-expectation failures (wrong standard-unit query and treating the explicit
form prefix as molecular text); corrected expectations pass all 48. The first
broader command passes 369/370: a pre-existing fresh-process fixture import finds
the controlled Viewer checkout's regular tests package instead of this
repository's namespace package. The test now explicitly scopes only its own
fixture namespace in that child, retaining its unchanged engine-denial assertions.
The next command passes 384/386, with two further prefix mistakes in new examples;
both examples are corrected before the final 392/392 receiving. None of these
nonpassing attempts is reported as passing evidence, and no production parser or
dependency check is weakened to satisfy the tests.

No new scientific method is introduced. Existing AutoDock field/tree references
remain owned by the parser. No credit is assigned to RDKit or Vina merely because
source annotations mention them. The producer version is recorded as actually
reported; editable installation metadata and the implementing source commit are
kept separate in the receiving receipt. Publication and owning-issue closure
follow this measured source block; #600 and #601 retain their ordered places.
