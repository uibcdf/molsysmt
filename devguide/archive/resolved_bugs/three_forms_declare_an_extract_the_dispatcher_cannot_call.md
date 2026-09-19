---
summary: Three forms declare an extract the dispatcher cannot call
issue: uibcdf/molsysmt#210
status: resolved
opened: 2026-09-06
closed: 2026-09-19
severity: medium
verification: measured
area: [form, basic]
guard: tests/basic/test_extract_extended.py
normative: devguide/forms_and_conversions.md
blocked_by: []
supersedes: []
---

# Three forms answer TypeError to every extract

**Reported:** 2026-09-06, from the signature scan run while fixing
[uibcdf/molsysmt#204](../archive/resolved_bugs/form_extract_signatures_do_not_match_the_dispatch_contract.md).
That entry fixed the two forms whose contract was unambiguous; these three are the same
symptom and a different question, so they are filed apart rather than folded in.
**Status:** resolved. All three adapters satisfy the dispatcher contract and their actual
axis semantics are covered through the public API.

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

- **The two mechanics forms do have a conditional atom axis.** `MolecularMechanics`
  stores `formal_charge`, `partial_charge`, and `atom_ff_type` in an `atoms_ff` DataFrame
  indexed by atom position, and the dict form exposes the same three arrays. Their
  getters, setters, merge implementation, and cross-converters all already subset those
  fields by atom. Extraction must therefore preserve the system-level force-field
  settings and subset all present per-atom fields. When no per-atom data exist, a subset
  request has no axis to act on and must raise `NotWithThisFormError` naming the form.
- **The sequence form indexes by group throughout.** `add`, `merge`,
  `to_string_amino_acids_1`, `to_string_amino_acids_3`, `to_biopython_Seq` and
  `to_biopython_SeqRecord` all take `group_indices`, and `to_string_amino_acids_3` calls
  `extract(item, group_indices=...)`. Renaming the parameter in `extract` alone would
  break its own caller, and a sequence has no atoms to index.

The generic extraction boundary nevertheless uses `atom_indices` for every form. For a
sequence-only representation those indices are positional sequence tokens -- one token
per residue -- which matches the established behavior of `string:amino_acids_1` and
`biopython.Seq`. The adapter therefore accepts the generic name and retains
`group_indices` as a compatibility alias for its group-aware converters.

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

**Measured during resolution:** the mechanics conversion implementations already slice
all three per-atom fields, and the mechanics getters expose an atom count whenever one of
those fields is present. The dict form's detector nevertheless omitted those three legal
keys, so a dictionary emitted by `MolecularMechanics.to_dict()` could not be detected as
`molsysmt.MolecularMechanicsDict`; that inconsistency is part of this fix because the
public extraction path cannot otherwise reach the advertised atom axis.

## What was refuted

**That the three could be closed with the signature change that fixed the other two.**
Accepting `atom_indices` and ignoring it would make `msm.extract(sequence, selection=...)`
return the whole sequence — a plausible wrong answer, which is worse than the `TypeError`
it replaces.

**That the mechanics forms have no element axis.** That was inferred from the old
`extract` bodies and was wrong. Their getters, setters, merge paths, and converters agree
on a conditional atom axis backed by the three per-atom force-field attributes. A
permanent `NotWithThisFormError` would discard a capability the forms already implement.

## Scope and exclusions

Covered: what these three forms should answer when asked to extract, and the code that
makes them answer it.

Not covered: whether `string:amino_acids_3` should adopt `atom_indices` across its whole
module. That is a larger question about how sequence forms are indexed, and it should be
answered deliberately rather than as a side effect of this.

## Acceptance criteria

- `msm.extract` on each of the three returns a value or raises a MolSysMT error that names
  the form, never `TypeError`. Confirmed through public extraction tests for both
  mechanics representations and the sequence form.
- The three names are removed from `EXTRACT_CONTRACT_DEBT` in
  `tests/test_form_plugin_conventions.py`, which then covers every form with no exception.
  Confirmed: the debt set is empty and the all-form contract test passes.

## Resolution

The mechanics adapters now copy an unrestricted input, preserve global force-field
settings, and subset every present per-atom field. A subset request on an object without
per-atom data, or a structure-index request on these structureless forms, raises
`NotWithThisFormError` with the form name. The dictionary detector accepts the same three
per-atom keys that its declared attributes, getters, setters, and converters already use.

The three-letter sequence adapter accepts the generic extraction signature, treats the
selected positions as residue tokens, retains `group_indices` for its existing converters,
preserves the explicit prefix, and reports invalid positions as a catalog
`ArgumentError` rather than leaking `IndexError`.

Validation on the final working tree:

- focused and adapter census: 263 passed, 2 accepted PyTraj skips;
- fast release gate: 13/13 passed;
- complete suite: 10,217 passed, 11 accepted dependency/environment skips under
  `-n 12 --dist loadfile` in 377.90 seconds;
- Ruff: all changed Python files clean.

## Provenance

Reproduced on Linux, Python 3.13.14, at `be0efb35f`, 2026-09-06. Resolved and
re-measured on the same platform and Python line on a working tree based at
`a68454a24`, 2026-09-19.
