---
summary: molsysmt.MolSys converts to openmm.System through a converter that receives a native topology.
issue: uibcdf/molsysmt#137
status: partial
opened: 2026-08-08
closed:
severity: medium
verification: reproduced
area: [form, convert]
guard:
normative:
blocked_by: []
supersedes: []
---

# `molsysmt.MolSys` -> `openmm.System` passes a native topology to OpenMM's extractor

**Reported:** 2026-08-08, found while mapping how an item of every declared form can be
obtained, for a `get_form` test battery.

**Status:** `openmm.System` fixed on 2026-08-08. `openmm.Simulation` still open -- the
same route uncovered a second, independent defect described below.

**Severity:** medium. Two declared conversion targets, `openmm.System` and
`openmm.Simulation`, are unreachable from `molsysmt.MolSys`, and the failure surfaces as a
bare `TypeError` from inside a form module rather than as a catalogued diagnostic, so the
message does not tell the caller what went wrong.

## Symptom

```python
import molsysmt as msm
from molsysmt import systems

molsys = msm.convert(systems['alanine dipeptide']['alanine_dipeptide.h5msm'],
                     to_form='molsysmt.MolSys')
msm.convert(molsys, to_form='openmm.System')
```

```
  File "molsysmt/form/openmm_Topology/extract.py", line 23, in extract
    for chain in topology.chains():
                 ~~~~~~~~~~~~~~~^^
TypeError: 'Chains_DataFrame' object is not callable
```

`openmm.Simulation` fails identically. `openmm.Topology` and `openmm.Modeller` convert
correctly from the same origin, so the defect is in the route, not in the OpenMM support.

## Diagnosis

`extract` in `molsysmt/form/openmm_Topology/` expects an `openmm.app.Topology`, whose
`chains` is a method. It is being handed MolSysMT's own `Topology`, whose `chains` is a
`Chains_DataFrame` attribute. The two are being treated as interchangeable somewhere along
the `MolSys -> openmm.System` route.

The failing line is inside the form module, so the mistake is upstream of it: whatever
selects `openmm_Topology.extract` for this conversion is passing the native topology
straight through.

## Next steps

1. Find where the route composes: which converter calls `openmm_Topology.extract`, and
   with what. The fix is likely a missing `MolSys -> openmm.Topology` step before the
   extraction, not a change to `extract` itself.
2. Add both targets to the conversion coverage once fixed.
3. Consider whether `extract` should assert the type it was given. A form module receiving
   an item of another form should say so, rather than failing on the first attribute that
   does not match.


## Resolution for `openmm.System`, and what it uncovered

`molsysmt_MolSys/to_openmm_System.py` reached for
`molsysmt.form.openmm_Topology.to_openmm_Topology` -- the converter that *subsets an
openmm.Topology* -- and handed it a `molsysmt.MolSys`. The sibling of the same name in its
own plugin is the one that converts this form, and `to_openmm_Context` and
`to_openmm_Modeller` already used it. Both `to_openmm_System` and `to_openmm_Simulation`
now do.

`MolSys -> openmm.System` works after that. `MolSys -> openmm.Simulation` gets further and
fails on something else:

```
TypeError: to_openmm_System() got an unexpected keyword argument 'coordinates'
```

`openmm_Topology/to_openmm_Simulation.py:6` has the same shape of mistake -- it imports
`to_openmm_System` from the **openmm_System** plugin, which converts an openmm.System, not
a Topology. But correcting the import is not enough: the sibling
`openmm_Topology/to_openmm_System` does not take `coordinates` either, and neither should
it. A `System` describes forces and constraints; positions belong to the `Context` the
`Simulation` builds.

So the fix is behavioural, not an import swap: build the System from the Topology, then set
the positions on the Simulation's context. That needs someone to decide what
`coordinates=None` should mean there -- leave the context unpositioned, or refuse -- which
is why it was not guessed at.

**The shape of both defects is worth noting**, because a third instance is likely: a
converter reaching into *another plugin* for a converter whose name matches the target
form, instead of the sibling in its own plugin that converts *from* this form. The names
are identical, so the mistake reads as correct. A check that every `to_x` called on `item`
comes from the plugin whose form `item` has would find them all.
