---
summary: PDB export reports unknown chain membership as an unhandled TypeError
issue: uibcdf/molsysmt#525
status: resolved
opened: 2026-10-30
closed: 2026-10-30
severity: low
verification: reproduced
area: [form, convert]
guard: tests/form/molsysmt_MolSys/test_pdb_text_missing_membership.py
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

Record — devguide/archive/resolved_bugs/pdb_export_reports_unknown_chain_membership_as_an_unhandled_typeerror.md


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

## Resolution — 2026-10-30

The native PDB writer now checks selected atoms for unknown `group_index` or
`chain_index` before formatting records. It rejects missing memberships with
`NotCompatibleConversionError`, naming the missing prerequisite and suggesting
an explicit correct assignment or H5MSM 0.5 for lossless missingness. It does not
infer or repair the hierarchy. Missing membership outside the selection does not
block export. An assigned chain with an unknown label retains the existing PDB
label fallback; label projection does not create a native chain assignment.

The regression module first reproduced five failures and three positive controls
on the original writer (run 124, exit 1). With the fix, all eight cases pass and
the atom-name alignment controls also pass (run 125: 22 passed, exit 0). The wider
PDB regression selection passes 440 cases, exit 0 (run 126), covering conversion
fidelity, selected payloads, capacity rejection, alternate locations, model
records, units, file/text routes and the new nullable-membership cases. Three
legacy-H5MSM warnings remain visible; none is suppressed for this qualification.

The new guards exercise the actual reported bundled legacy H5MSM, unknown groups
and chains in later atoms, unchanged source coordinates/units/inventory/bonds,
selected-only prerequisites, assigned unnamed chains and rejection before file
creation or overwrite. This is a diagnostic fix, not a scientific calculation or
an extension of the PDB data model. Docstrings, the User Guide foundations and
conversion tutorial, the conversion cookbook and course Module 04 state the policy.

This resolves the separate #525 follow-up. It does not close #255, qualify a
published artifact, migrate the remaining clients or authorize main integration.

Validation — the fast gate passes 14/14 checks (run 133), whole-package Ruff and
the form-adapter audit pass (run 129), and strict Sphinx HTML passes (run 132,
exit 0). Notebook edits are narrative-only: code cells and saved outputs are
byte-equivalent as parsed JSON. The Sphinx API supplies a typed boolean to
`autosummary_generate=False` to preserve unrelated generated-file edits; no
new API page is needed. An earlier CLI invocation (run 127, exit 1) passed
`False` as a string and produced configuration warnings. That invocation error
is preserved separately, not attributed to the product or relabeled as a pass.
