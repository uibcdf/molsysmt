---
summary: Native domain composition fails on charges and explicit chemical-state metadata
issue: uibcdf/molsysmt#430
status: resolved
opened: 2026-10-22
closed: 2026-10-22
severity: medium
verification: reproduced
area: [form, convert]
guard: tests/basic/convert/mult_to_one/test_native_mechanics_composition.py
normative:
blocked_by: []
supersedes: []
---

# Native domain composition fails on charges and explicit chemical-state metadata

**Reported:** 2026-10-22, while qualifying form-agnostic input for #223.
**Status:** Resolved. Numeric charge delivery and explicit standalone native-domain composition are repaired and qualified.

## What

Two native composition controls failed on stored, finite charges and a complete
single chemical state:

1. `msm.convert([topology, structures, mechanics], to_form='molsysmt.MolSys')`
   rejected its native partial-charge values with ArgumentError.
2. Adding the explicit ChemicalStates domain to that list reached an
   InternalAlgorithmError for `reference_chemical_state_index`, whose generic
   set target is None. The current bounded composition documentation does not
   promise this four-domain combination; the internal-error diagnostic still
   exposes an unresolved native-domain integration need.

The first case is exercised by
`tests/basic/convert/mult_to_one/test_native_mechanics_composition.py`.
For the second, use the same declared system and convert
`[source.topology, source.chemical_states, source.structures,
source.molecular_mechanics]`. No external provider is required.

## How

MolecularMechanics properties expose object-backed pandas columns. Its adapter
passed those object arrays directly to the public charge setter, whose numeric
boundary accepts finite numeric dtypes. The getter now returns Float64 values
in the existing canonical elementary-charge convention. It does not infer a
unit from the presentation policy or relax validation of arbitrary object data.

The four-domain case follows generic attribute composition. It attempts to
route reference-state metadata as an ordinary settable Topology attribute;
there is no such setter. Repair requires defining explicit provider/conflict
ownership for native-domain composition, not adding a meaningless setter or
silently discarding the chemical state. This remains pending here.

## Why

Native tools must be able to consume the attributes delivered by registered
providers. #223 now accepts the functioning three-domain route with a declared
shared atom axis, and also accepts a MolSys carrying all required domains.
The new transform does not implement a competing composition engine.

## Evidence and bounds

Reproduced on Linux / Python 3.14.7. Getter/composition guards cover values,
Float64 delivery, complete chemistry and a non-default pm/coulomb policy.
The source mechanics property representation is unchanged. The explicit
four-domain combination is not newly admitted or qualified by this fix.
No new publication gate, optional dependency or Ackredit boundary is introduced.
The getter is data transport, so additional scientific attribution is not applicable.


## Explicit native-domain composition — 2026-10-22

The owning native-composition seam now assembles standalone Topology,
ChemicalStates, Structures and MolecularMechanics providers before generic
attribute routing. It also handles native lists with mechanics plus chemical or
structural domains and Topology plus explicit ChemicalStates without mechanics.
Existing ChemicalStates/Structures pair shortcuts, generic external/dictionary
routes and the separate partial-MolSys/H5MSM composition contract remain in place.
Partial MolSys lists still reject nonempty mechanics; the new standalone route
does not certify that separate format/provider combination.

One explicit provider is allowed per domain. The existing molecular-system
classifier rejects multiple primary topologies; other repeated explicit domains
raise StructuralInconsistencyError. Explicit ChemicalStates owns the complete
collection/reference even when Topology carries different compatibility states.
Without that provider, the topology collection supplies fallback chemistry.
This is domain ownership, not list-order precedence or a per-attribute merge.
No fake reference-state setter is added. Full shared axes must agree before
selection; per-atom mechanics requires a complete declared atom axis of the same
length. Matching axes are a caller declaration, not source authentication.

Native ownership and extraction handle copying and selections. Topology and its
chemical domain detach; a Structures wrapper with another live owner detaches
through existing protected geometry storage. The default conversion takes an
independent native snapshot. Explicit full-axis copy_if_all=False suppresses
that final snapshot but still respects ownership; unowned structures and mechanics
can be shared. No full source coordinate series is read to discover providers.
Topology-backed subsets remain sorted, while chemical/structural-only extraction
retains requested atom order. Multiple chemical states are not assigned to
structures implicitly.

The whole mechanics domain is transferred, including scalar/quantity settings and
original named assignment reports, without recalculation or new certification.
Existing extraction helpers project original atom maps and preserve original
producer versions, references and attribution. Incompatible chemistry makes
projected reports stale; composition never rebinds them to legitimize changed
chemistry. H5MSM 0.5 still rejects nonempty mechanics before file creation.
This transport is not an Ackredit calculation boundary.

The public convert Notes, User Guide/Foundations and course Module 04 document
the ownership/copy rules with an executable four-domain example. The primary
guard module now covers every permutation of four providers, conflicting full
axes, repeated providers, explicit chemistry overriding compatibility fallback,
multiple/empty states, source independence, full-axis no-copy ownership, indexed
selection, named-provenance preservation/staleness and H5MSM behavior.


### Declared versus absent structural atom axes

Qualification also exposed an owning-axis distinction in the same composition
path: an empty or observable-only native Structures has no declared atom axis,
although its historical public n_atoms property returns zero. The general
molecular-system assessment had treated that placeholder as a declared zero
length, rejecting a valid chemical inventory before composition could run.
Structures now owns a private metadata-only `_atom_axis_size` seam, shared by
native MolSys axis validation/count discovery and molecular-system assessment.
It reads shapes only and returns None for an absent axis; actual coordinates
with shape (n_structures, 0, 3) still declare zero atoms and conflict with a
nonempty chemical inventory. Public count-property behavior is unchanged.
Both empty/observable-only inputs and a genuinely zero-sized coordinate axis
are covered by the primary guard; a selection cannot hide the latter mismatch.


## Resolution and qualification

Both reported slices are resolved: numeric getter delivery was fixed in
`af44df89e`, and the owning native-domain seam now handles explicit standalone
providers without sending reference-state metadata to a nonexistent setter.
The guard module fails on the reported four-domain reconstruction and tests all
24 provider permutations, owner precedence, provenance, full-axis conflicts and
native extraction. It also distinguishes an absent structural atom axis from
a genuinely declared zero-sized coordinate array. No fake setter, independent
chemical store or consumer-side composition engine was introduced.

Final local qualification passed **482 tests**, zero failures/skips, in 92.42 s
with 12 workers and Pytest Receptor. The 119 unsuppressed warnings comprise 108
legacy H5MSM notices, six MDAnalysis mass deprecations, three declared off-axis
attribute drops, one expected incompatible-box warning and one previously
recorded optional NumPy ABI-size warning. The pandas 3.1.0 compatibility selection
passed **76 tests**, zero failures/skips, in 17.37 s, retaining 32 legacy H5MSM
notices. It uses the published wheel already recorded under #431.

The final course Module 04 and Convert tutorial executed in 7.2 s and 73.4 s;
the convert doctest passed (1.10 s). Ruff, the public-signature guard, 249 public
docstrings and all 14 fast gates pass. Exact commands, environment, tested
executable hashes and documentation-provider bounds are in the
[source receipt](../../../devtools/data/native_domain_composition_20261022.json).
This source-level result neither qualifies a new installed pair nor changes
the publication pause under #334. Existing generic dictionary/external routes
and partial-MolSys mechanics exclusions remain explicit scope boundaries.
