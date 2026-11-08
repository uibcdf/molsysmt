---
summary: Define an explicit stored-hydrogen policy composition before strict correspondence.
issue: uibcdf/molsysmt#645
status: active
opened: 2026-11-07
closed:
verification: measured
area: [api, build]
guard:
normative:
blocked_by: []
supersedes: []
---

# Explicit stored-hydrogen policy before correspondence

## What

DockingMT asks for a supported explicit composition to align stored hydrogen
policies from source conversion and fixed-state H generation before strict
chemical correspondence. Its reported source/generated inputs have matching
indexed atom/bond counts but differ in the `allows_implicit_hydrogens` flags
on indexed H atoms. The strict graph matcher treats those policies as labels
and returns no retained maps. This is not established as a matcher defect.

## Evidence and limits

The executed consumer chain, exact public P59 source/reference inputs, versions,
failed witness and source nonmutation limits are preserved in
uibcdf/molsysmt#645 and uibcdf/dockingmt#79. The reported 39-atom/42-bond
comparison and successful heavy-coordinate preservation are consumer findings,
not newly executed provider acceptance in that original intake. Other differing identifiers/coverage
metadata also require review; literal record agreement does not certify
chemical equivalence. The bounded feasibility study below now receives the exact public input bytes; no supported normalization is implemented here.

## Intended study

- Inspect existing public copy, assignment, state/history and H-representation
  tools before proposing another API. ChemicalStates owns stored assignments;
  build owns H generation. Reuse supported general operations.
- Determine whether detached copy plus public assignment is sufficient, with
  explicit preconditions, affected atoms/fields, source axes, allowed losses
  and a retained transformation record. The consumer must not invent a policy.
- If a provider tool is missing, design the smallest useful general operation
  in its owner; keep unknown, isotopic, charged, radical and truly incompatible
  H states explicit. Preserve original sources, coordinates, H-parent links,
  charge, isotope/stereo and meaningful preparation history.
- Receive both actual producers, nondefault units and detached persistence as
  applicable before claiming that an explicit common policy enables matching.
  Do not coerce flags inside the matcher, weaken labels or turn zero matches
  into zero RMSD.

## Priority and scope

This remains a separately assessed provider-policy proposal after #644's clear
public argument defect. It does not automatically enlarge frozen initial-1.0
gates or authorize a downstream workaround. Existing strict correspondence
and #612/#334 qualification obligations remain unchanged. No new engine,
chemical assignment or public namespace is selected by this intake record.

## Provider feasibility study — 2026-11-07

Clean public source `4f642256996bd25a21a9b204d7a684207e589974`, with RDKit
2025.9.5, receives both original public SDFs after verifying the SHA-256 values
in the issue. Attribution remains with the pinned AutoDock Vina examples in
uibcdf/dockingmt#79 and uibcdf/molsysmt#645; these input files are not chemically validated ground
truth. No fixture is copied into the product or test tree. The
[study receipt](../../devtools/data/stored_hydrogen_policy_study_645_20261107.json)
retains observations, exact execution and enforced resource limits.

The source chain is native SDF conversion with explicit RDKit stereo/discard
policy, native-to-RDKit-to-native interpretation, then fixed-state H generation
on the heavy reference. In both normal and pm/fs/coulomb contexts:

- The H operation adds fifteen indexed H atoms and retains the original heavy
  coordinates within 1e-12 angstrom absolute tolerance, zero relative tolerance.
- Strict correspondence has two candidates and zero retained maps, with complete
  search and an empty `(0, 24, 2)` heavy-atom result.
- Each input has fifteen indexed H atoms with known zero virtual-H, formal-charge
  and radical counts. The stored inventory audit is available.
- On detached public copies, setting only those H atoms'
  `allows_implicit_hydrogens=False` changes fifteen flags on the source and zero
  on the generated reference. Heavy-atom flags, other atom attributes, isotopes,
  bonds, coordinates and H-parent pairs remain unchanged.
- The unchanged strict matcher then retains two maps, shape `(2, 24, 2)`. Full
  H5MSM persistence preserves those assignments and the same witness. This does
  not equate the sources' different coordinate poses or compute an RMSD.
- Original serialized MolSys snapshots and caller unit authority are unchanged.
  Historical preparation records remain zero on the source and two on the
  generated reference. Copy/set does not add evidence for the new policy edit.

The private study exits zero in about seven seconds under one CPU, a 2 GiB
process-tree bound and zero swap; peak is 175,140,864 bytes. The original SDF
2D/3D-tag warnings remain in the log. This is **measured feasibility**, not
acceptance of a general normalization policy or the consumer's different
provider/RDKit versions.

## Existing pieces and ownership

`physchem.get_hydrogen_inventory` audits indexed H-parent links and stored
virtual counts. Available inventory does not certify valence or protonation.
Public selected-state getters supply the charge/radical/permission fields;
`basic.copy` and `basic.set` already perform detached assignment. H generation
belongs in build. Strict correspondence and a reusable state-policy operation
belong in chemical_states; the matcher must not normalize labels implicitly.

ChemicalStates.get_preparation_history preserves original operation evidence.
Its public append_preparation_history archives validated versioned envelopes
without authenticating sources or applying chemistry. The envelope validator
requires operation-local output dimensions and a report with a declared schema;
it does not provide the scientific meaning of a new hydrogen policy. Typed
ChemicalStatesDict/H5MSM history persistence already exists. No new serializer,
force field, minimizer, Rust kernel, optional dependency or chemical store is
needed for the measured assignment.

## Decision still required before implementation

Two defensible delivery shapes remain: a documented composition using the
existing tools, or a small provider-owned policy tool that performs the same
checked composition and produces its own transformation report. A recipe avoids
another API but leaves callers to repeat the chemical admission and provenance
logic. A general tool centralizes that logic and can be received independently,
but needs an exact scope rather than a blanket claim of H canonicalization.
The latter is the preferred direction if this policy is reused across clients.
No public function name, default, report schema or accepted policy is fixed yet.

The first candidate policy should be bounded to already indexed, terminal
covalent H with known zero virtual counts and declared supported chemistry. It
would close the implicit-H permission only; heavy-atom permissions, H inventory,
charges, isotope/radical/stereo labels and graph topology would stay explicit.
Whether labelled isotopic H is admitted unchanged, and whether charged/radical
or unusual H states must reject, requires independent controls. Unknown fields,
nonterminal/H-H/dative relationships, incomplete connectivity and incompatible
heavy-atom states must not be silently coerced.

Before acceptance, define selected-state/multistate behavior, deterministic
changed/unchanged atom indices and identity maps, atomic failure/source
preservation, attached-analysis invalidation, and provider/version evidence in
the original operation domain. Do not discard older history or invent chemical
equivalence from equal atom counts. Receive both producers, unchanged/no-op and
rejection cases, isotope/charge/radical/stereo controls, nondefault units and
detached persistence. Review copy costs for large coordinate ensembles; a
chemical-state policy must not require an unexplained full-coordinate snapshot.
The proposal remains open and adds no release milestone credit.
