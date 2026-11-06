---
summary: Support native MolSys input in get_forces for primary-bound consumers.
issue: uibcdf/molsysmt#572
status: open
opened: 2026-11-05
closed:
verification: reproduced
area: [api, molsysviewer]
guard:
normative:
blocked_by: []
supersedes: []
---

# Native MolSys force reader for primary-bound consumers

## What

Provide a scientific-owner route for molecular_mechanics.get_forces on a native
MolSys, or a supported public replacement with explicit conversion/model rules.
The existing implementation admits only OpenMM Context and Simulation inputs;
the Viewer tools addon binds the current native MolSys. This is a capability
request, not evidence that the existing OpenMM force numbers are incorrect.

## Reproduction

On published native basis 532d036228c9673c5ddd63beaa8093220b06b6b2 and contribution
04b9fbbda4654516c01d6c34e9c19ad17c1be0fb, Linux/Python 3.14.7 with OpenMM present:

```python
import molsysmt as msm

molsys = msm.convert(
    msm.systems["Trp-Cage"]["1l2y.h5msm"],
    to_form="molsysmt.MolSys",
    structure_indices=[0],
)
msm.molecular_mechanics.get_forces(molsys)
# NotImplementedError (empty message)
msm.molecular_mechanics.get_forces(molsys, skip_digestion=True)
# NotImplementedError (empty message)
```

Both calls are independently reproduced without importing Viewer. The legacy
H5MSM warnings are retained; the failure occurs in the explicit unsupported-form
branch, before molecular parameterization. A first draft probe used a nonexistent
pentalanine.pdb catalog key and was discarded; the final issue uses the actual
bundled Trp-Cage file above.

The positive control constructs a two-particle OpenMM System with one harmonic
bond, k=100 kJ/(mol nm²), equilibrium length 0.1 nm and actual separation 0.2 nm.
An explicit CPU Context with one thread returns the analytical [+10,0,0] and
[-10,0,0] kJ/(mol nm) forces through the native reader. Engine absence and an
incorrect existing Context result are thus refuted for this bounded control.

## Why

uibcdf/molsysviewer#264 and #421/#543 require expert mirrors to consume the
current view.molsys and delegate scientific work to MolSysMT. An always-rejected
bound method adds no useful capability; implicit consumer-side context creation
would also introduce scientific model/preparation decisions outside its owner.
The addon therefore keeps get_forces unexposed and continues other mechanical
queries without changing its denominator or claiming a complete force surface.

## Acceptance

Define which structures are read and whether selection returns forces in the
complete parameterized environment or in a rebuilt subsystem. Specify magnitude,
output axes/units, supported element levels, stored/default mechanics, periodic
conditions, explicit engine behavior and unsupported-form diagnostics. Preserve
source/engine ownership and avoid hidden preparation or fallback.

Protect native MolSys plus Context/Simulation routes with pytest cases for
selection forms and order, magnitude, units under a non-default policy, unsupported
inputs and scientific source preservation. Compare with analytical forces or an
independent energy-gradient oracle. The scientific owner chooses and implements
the contract; this consumer report does not authorize native changes or publication.

## Disposition

The maintainer explicitly authorized opening #572. Existing source and installed
qualification retain their own scopes. No native force implementation, placeholder
wrapper, Viewer runtime change or dependency-floor increase is added here.
