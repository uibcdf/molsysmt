---
summary: Physchem property readers drop the declared selection syntax.
issue: uibcdf/molsysmt#470
status: open
opened: 2026-10-26
closed:
severity: medium
verification: reproduced
area: [physchem, selection]
guard:
normative:
blocked_by: []
supersedes: []
---

# Physchem property readers drop the declared selection syntax

**Reported:** 2026-10-26 during provider addon receiving under uibcdf/molsysmt#421;
consumer uibcdf/molsysviewer#264. Filing explicitly authorized by the maintainer.
**Status:** open; scientific repair belongs to the native provider.

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
