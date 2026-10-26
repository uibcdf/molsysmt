---
summary: Physchem property readers drop the declared selection syntax.
issue: uibcdf/molsysmt#470
status: resolved
opened: 2026-10-26
closed: 2026-10-26
severity: medium
verification: reproduced
area: [physchem, selection]
guard: tests/physchem/test_property_selection_contract.py
normative:
blocked_by: []
supersedes: []
---

# Physchem property readers drop the declared selection syntax

**Reported:** 2026-10-26 during provider addon receiving under uibcdf/molsysmt#421;
consumer uibcdf/molsysviewer#264. Filing explicitly authorized by the maintainer.
**Status:** resolved at the native boundary; consumer reception is separate.

## What

get_charge (tabulated definitions), get_atomic_radius, get_electronegativity and
get_hydrophobicity accept syntax but resolve an MDTraj string with MolSysMT.

```python
import molsysmt as msm
molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'])
msm.physchem.get_atomic_radius(molsys, selection='name CA', syntax='MDTraj')
# ArgumentError: selection could not be parsed with the 'MolSysMT' syntax
```

The same expression succeeds in native get_mass, get_polarity and
get_transmembrane_tendency on that primary. The MolSysMT expression
`atom_name=='CA'` succeeds in the affected readers. The default selector is
unaffected, so ordinary default-only tests do not protect this contract.

## How

The four implementations call basic.get without forwarding syntax. The ProtOr
radius delegates to atoms.protor.get_protor_atom_type, whose own basic.get calls
also omit it. The addon passes syntax unchanged through the ordinary native
public boundary. It supplies no selector conversion or substitute table lookup.

## Why

Users cannot use an advertised selection syntax through these native functions
or their thin bound wrappers. An expression can fail or be interpreted under a
different grammar. No incorrect numerical result has been measured in this
reproduction; the observed outcome is explicit rejection.

## What is measured and what is assumed

Seven native default-definition calls were executed with the same MDTraj string:
three succeeded, four rejected it as MolSysMT. Vdw radius was executed; the ProtOr
propagation gap is additionally source-inspected, not separately scientifically
qualified by this reproduction. No statement covers every alternative syntax.

## What was refuted

This is not a Viewer-only failure or absent MDTraj selector support: the same
primary/selector works in the three controls. No automatic molecular preparation
or scientific algorithm replacement is needed in the addon.

## Scope and exclusions

Repair selector propagation and protect default/explicit syntax, numerical and
empty selections, intended atom/group output, order, units, container type and
source nonmutation. Preserve intentional unknown-group errors. This report does
not redefine supported element hierarchies, table values or optional force fields.
Until repaired, use MolSysMT expressions or explicitly resolve numeric indices.

## Acceptance criteria

Native pytest guards must compare equivalent selections with independently
resolved intended atom/group populations across all four functions and radius
definitions. Validate the native functions without Viewer, then receive the
repair in the addon. A parity test comparing two rejected calls is not the native
repair guard.

## Provenance

Linux, Python 3.14.7, molsyssuite@uibcdf_3.14, native source e395e5264 and the
ongoing addon changes. Only public native functions perform the calculations.


## Additional receiving scope — 2026-10-26

On frozen native d7c82e92f, native-only calls also reproduce the MDTraj
selector loss in get_protor_atom_type, get_protor_vdw_radius, get_volume and
get_buried_fraction. get_surface_area is a successful control on the same
primary and selector. get_area_buried has no syntax argument and is not
classified as dropping one. These tools are part of the next addon slice;
include their actual public signatures in this same selector-propagation
repair and native guards. Concurrent working-tree repairs are not qualified
by this frozen-baseline observation.

## Resolution — 2026-10-26

Every relevant attribute query now retains the supplied syntax through the
charge, atomic-radius, electronegativity, hydrophobicity, ProtOr typing/radius,
volume and buried-fraction paths. Existing polarity, transmembrane-tendency and
surface-area controls keep their correct delegation. The implementation stays
form-agnostic through basic.get and its providers; no consumer-side selector
translation or new molecular store is introduced.

The actual signatures remain intact: get_volume has a fixed group axis and no
element argument; get_area_buried has no syntax argument. Callers can resolve
alternate syntax explicitly with public basic.select and supply group indices
to the latter. This is not an implicit signature expansion. Source values,
tables, containers and existing unit boundaries remain unchanged. The raw
Collantes unit interpretation remains separately open under uibcdf/molsysmt#473.

The native guard uses an explicit three-group, nine-atom labeled fixture with
literal property values. Independent selected populations distinguish atom and
group positions, default/MolSysMT/MDTraj syntax, empty and repeated indices,
MolSys and Topology, nm/pm policies, direct ProtOr provenance, component charge
aggregation, source nonmutation and expected unknown-group diagnostics. The
original eight-tool guard failed 112 cases with 175 controls passing; the
additional receiving scope failed 52 filtered cases with 88 controls passing
after the earlier repairs. These are separate overlapping campaigns, not an
additive coverage count. The current combined guard passes 435 cases.


## Qualification — 2026-10-26

The full physchem and argument selection passes **976 tests** in 81.59 seconds
with `--receptor=llm -n 12`, without skips. Its 87 warnings are existing legacy
H5MSM, future pandas fillna and explicit unsupported-GPU diagnostics. All forty
new source doctest examples pass. The original generic group example selected
an unparameterized ACE cap and correctly raised UnknownGroupInTableError; it
was corrected to known amino-acid groups, without weakening that diagnostic.
Ten property tutorials and course Module 20 execute successfully. The named
charges Cookbook and Foundations were updated as prose; their unrelated
pre-existing chemical-preparation examples were not rerun by this checkpoint.

The [normative query contract](../../physchem_query_contract.md) records current
scope and units. Commands, environment, source hashes and remaining limits are
retained in the [query qualification receipt](../../../devtools/data/physchem_queries_20261026.json).
No installed-consumer, full scientific/release matrix or new attribution-method
qualification is claimed. Consumer receiving remains separately owned by
uibcdf/molsysmt#421 and uibcdf/molsysviewer#264.
