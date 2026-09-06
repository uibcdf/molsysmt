---
summary: Three forms declare an extract the dispatcher cannot call
issue: uibcdf/molsysmt#210
status: open
opened: 2026-09-06
closed:
severity: medium
verification: reproduced
area: [form, basic]
guard:
normative:
blocked_by: []
supersedes: []
---

# Three forms answer TypeError to every extract

**Reported:** 2026-09-06, from the signature scan run while fixing
[uibcdf/molsysmt#204](../archive/resolved_bugs/form_extract_signatures_do_not_match_the_dispatch_contract.md).
That entry fixed the two forms whose contract was unambiguous; these three are the same
symptom and a different question, so they are filed apart rather than folded in.
**Status:** open. Reproduced, not started: each needs a decision before it needs code.

## What

`msm.extract` raises `TypeError` on `molsysmt.MolecularMechanics`,
`molsysmt.MolecularMechanicsDict` and `string:amino_acids_3`.

```python
>>> msm.extract(MolecularMechanics())
TypeError: extract() got an unexpected keyword argument 'atom_indices'
>>> msm.extract('AlaAlaAla')
TypeError: extract() got an unexpected keyword argument 'atom_indices'. Did you mean 'group_indices'?
```

## How

`molsysmt/basic/extract.py:139` calls every form the same way, with `atom_indices`,
`structure_indices`, `copy_if_all` and `skip_digestion`. These three declare something
else:

| form | missing from the signature | has instead |
| --- | --- | --- |
| `molsysmt_MolecularMechanics` | `atom_indices`, `structure_indices` | — |
| `molsysmt_MolecularMechanicsDict` | `atom_indices`, `structure_indices` | — |
| `string_amino_acids_3` | `atom_indices`, `structure_indices` | `group_indices` |

The fix is not mechanical in any of the three, which is why this is a separate theme:

- **The two mechanics forms have no element axis.** `MolecularMechanics` holds
  force-field settings plus an `atoms_ff` DataFrame indexed by atom position, so
  "extract these atoms" is either meaningless or a real subsetting of `atoms_ff` — a
  decision, not a rename. `molsysmt_MolecularMechanics/extract.py` already raises
  `NotWithThisFormError`, which is the right answer once it can be reached; the dict form
  returns a copy and would silently ignore any indices it were handed.
- **The sequence form indexes by group throughout.** `add`, `merge`,
  `to_string_amino_acids_1`, `to_string_amino_acids_3`, `to_biopython_Seq` and
  `to_biopython_SeqRecord` all take `group_indices`, and `to_string_amino_acids_3` calls
  `extract(item, group_indices=...)`. Renaming the parameter in `extract` alone would
  break its own caller, and a sequence has no atoms to index.

## Why

Three of the 89 supported forms answer `TypeError` to a public operation, and the message
names an internal keyword the user never wrote, so it reads as a MolSysMT defect rather
than as an unsupported operation. Whatever each form should answer — a value, or
`NotWithThisFormError` — it is not that.

Severity is `medium` rather than `high` because none of the three is Tier 1 and no
documented workflow extracts from them; the Tier 1 case found by the same scan,
`molsysmt.StructuresDict`, was fixed under #204.

## What is measured and what is assumed

**Measured:** the reproductions above, and the signature scan over all 84
`molsysmt/form/*/extract.py`:

```bash
python - <<'PY'
import ast, pathlib
required = {'item','atom_indices','structure_indices','copy_if_all','skip_digestion'}
for p in sorted(pathlib.Path('molsysmt/form').glob('*/extract.py')):
    for node in ast.parse(p.read_text()).body:
        if isinstance(node, ast.FunctionDef) and node.name == 'extract':
            missing = required - {a.arg for a in node.args.args}
            if missing:
                print(p.parent.name, sorted(missing))
PY
```

**Assumed, and worth checking before the fix:** that the same divergence does not exist in
the other dispatched form operations. `extract` is the only one this scan covered.

## What was refuted

**That the three could be closed with the signature change that fixed the other two.**
Accepting `atom_indices` and ignoring it would make `msm.extract(sequence, selection=...)`
return the whole sequence — a plausible wrong answer, which is worse than the `TypeError`
it replaces.

## Scope and exclusions

Covered: what these three forms should answer when asked to extract, and the code that
makes them answer it.

Not covered: whether `string:amino_acids_3` should adopt `atom_indices` across its whole
module. That is a larger question about how sequence forms are indexed, and it should be
answered deliberately rather than as a side effect of this.

## Acceptance criteria

- `msm.extract` on each of the three returns a value or raises a MolSysMT error that names
  the form, never `TypeError`.
- The three names are removed from `EXTRACT_CONTRACT_DEBT` in
  `tests/test_form_plugin_conventions.py`, which then covers every form with no exception.

## Provenance

Linux, Python 3.13.14, `molsysmt` at working tree `be0efb35f`, 2026-09-06.
