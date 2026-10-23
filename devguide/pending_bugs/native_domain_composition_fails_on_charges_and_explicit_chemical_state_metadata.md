---
summary: Native domain composition fails on charges and explicit chemical-state metadata
issue: uibcdf/molsysmt#430
status: partial
opened: 2026-10-22
closed:
severity: medium
verification: reproduced
area: [form, convert]
guard:
normative:
blocked_by: []
supersedes: []
---

# Native domain composition fails on charges and explicit chemical-state metadata

**Reported:** 2026-10-22, while qualifying form-agnostic input for #223.
**Status:** Partial. Numeric charge delivery is repaired; explicit four-domain
composition retains its separate metadata-resolution failure.

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
