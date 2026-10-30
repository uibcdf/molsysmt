---
summary: PDB export reports unknown chain membership as an unhandled TypeError
issue: uibcdf/molsysmt#525
status: open
opened: 2026-10-30
closed:
severity: low
verification: reproduced
area: [form, convert]
guard:
normative:
blocked_by: []
supersedes: []
---

# Unknown chain membership leaks through the PDB writer

What — Exporting a native MolSys with valid coordinates/groups but unknown atom-to-chain membership raises an unhandled TypeError while coercing pandas.NA to int.

How — With the independent-domain source 97f6b58ff6096750a955459c58bdff67c325aae7, extract the first ten atoms and structure 0 from the bundled pentalanine trajectory, then convert to string:pdb_text. The legacy file stores unassigned atom-to-chain positions; the writer fails at molsysmt/form/molsysmt_MolSys/to_string_pdb_text.py:286. No network or optional chemistry engine is required.

Why — Unknown membership is legitimate native information. PDB may require a deliberate format-loss/prerequisite policy, but a raw nullable-index exception does not explain that policy. Decide whether to support the representable missingness with an explicit fidelity report or reject with an actionable domain diagnostic. Do not invent chain zero or rewrite native membership to make export succeed.

This is a diagnostic/partial-export follow-up found during uibcdf/molsysviewer#269 receiving for uibcdf/molsysmt#255. The positive Viewer composition fixture now explicitly declares its intended chain; the unknown-membership selection guards remain active. It is not evidence that declared-chain export fails, nor authorization to weaken native invariants or introduce automatic repair.

Reproduction:

```python
import molsysmt as msm
molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'],
                     selection=list(range(10)), structure_indices=[0],
                     to_form='molsysmt.MolSys')
assert msm.get(molsys, element='atom', chain_index=True) == [None] * 10
msm.convert(molsys, to_form='string:pdb_text')
```

Observed: TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NAType'. Source coordinates, hierarchy and chemistry must remain unchanged on rejection.

Record — devguide/pending_bugs/pdb_export_reports_unknown_chain_membership_as_an_unhandled_typeerror.md


## Acceptance criteria

- State the supported partial-hierarchy policy for PDB export: an explicit
  representable projection with a truthful loss report, or an actionable typed
  rejection identifying missing atom-to-chain membership.
- Keep unknown membership distinct from an assigned unnamed chain. Do not assign
  chain zero, infer membership from geometry or mutate the source as a repair.
- Add an independent guard for the reported nullable input, with a declared-chain
  positive control and unchanged source coordinates, units, inventory and chemistry.
- Preserve existing PDB field-capacity and multi-structure behavior. No scientific
  interaction or chemical-state policy change is required to improve this diagnostic.

## Current disposition

Open diagnostic/partial-export follow-up, discovered in the Viewer source gate.
The positive composition fixture was corrected to declare its intended chain;
that does not resolve this unsupported-input diagnostic. The appropriate PDB
projection/prerequisite policy remains to be decided. This record introduces no
new provider runtime change or release-scope decision.
