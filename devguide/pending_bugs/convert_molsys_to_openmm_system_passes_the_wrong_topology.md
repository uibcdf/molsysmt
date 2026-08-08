# `molsysmt.MolSys` -> `openmm.System` passes a native topology to OpenMM's extractor

**Reported:** 2026-08-08, found while mapping how an item of every declared form can be
obtained, for a `get_form` test battery.

**Status:** open. Reproducible.

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
