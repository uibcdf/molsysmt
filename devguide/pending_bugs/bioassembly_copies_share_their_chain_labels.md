---
summary: After make_bioassembly, a chain-and-residue selection silently returns every copy
issue: uibcdf/molsysmt#198
status: open
opened: 2026-09-02
closed:
severity: medium
verification: reproduced
area: [build, selection]
guard:
normative:
blocked_by: []
supersedes: []
---

# The labels stop identifying, and the selection does not say so

**Reported:** 2026-09-02, from `uibcdf/molsysviewer` while closing the viewer half of the
old #163. The viewer defect is fixed and this asks for nothing on its behalf: it is a
separate, MolSysMT-side consequence of the same underlying fact, found because fixing the
first one required measuring the second.

## What

`make_bioassembly` reuses the asymmetric unit's chain labels for every generated copy, so
after the call an author label no longer identifies a chain.

```python
molsys    = msm.convert('2BUK')
assembled = msm.build.make_bioassembly(molsys, bioassembly='1')
```

| selection | atoms | |
| --- | --- | --- |
| `chain_id=='A'` on the asymmetric unit | 1 427 | as expected |
| `chain_id=='A'` on the assembly | **85 620** | 60x, silently |
| `chain_id=='A' and group_id==12` | **420** | what a user reads as *one residue* |
| `chain_index==0` | 1 427 | correct |

The third row is the one that matters. Naming a chain and a residue number is the most
natural way to point at a residue, and on an assembly it returns sixty of them, with no
error and no warning. The result is not empty and not malformed — it is plausible and
wrong, which is the expensive kind.

## How

| | atoms | chains | distinct `chain_id` | distinct `group_id` |
| --- | --- | --- | --- | --- |
| asymmetric unit | 1 588 | 5 | 5 | 345 |
| assembly | 95 280 | 300 | **5** | **345** |

`chain_index` holds 300 distinct values, so the information is present and correct. Only
the labels repeat, and only the labels are what a selection expression can name.

## Why

The PDB/mmCIF convention for generated assemblies gives each copy its own `label_asym_id`
precisely so copies stay addressable, while `auth_asym_id` may repeat. The current
behaviour is defensible — the copies genuinely *are* chain A, sixty times — but then no
label-based expression can name one of them, and nothing says so at the point of use.

The decision is MolSysMT's. The options visible from here:

1. give the copies distinguishable identifiers (`A`, `A-2`, … or an operator suffix, as
   mmCIF does), keeping the original label in its own attribute;
2. keep the labels and warn from `make_bioassembly` that they no longer identify;
3. document it as expected, and point users at `chain_index` for addressing copies.

## What was refuted

**That this is the viewer's bug.** It was filed there first, as #163, because the
symptom was visual: a 60-copy capsid drew its waters and one protein. The viewer's own
defect was real and is fixed — it fed the author label into Mol\*'s internal identity, and
now sends `chain_index` beside it — but fixing it does not touch this. A selection made in
Python, with no viewer involved, still returns sixty residues for one.

**That `chain_index` is the answer for identity generally.** It addresses copies, and it
is what the viewer now uses for Mol\*'s hierarchy. But it is positional: an identity that
changes when a system is reordered is not an identity. That is why this asks about the
*labels* rather than proposing that everything switch to indices.

## Related

- `uibcdf/molsysmt#163` — the original report; its viewer half is
  `uibcdf/molsysviewer#64`, fixed 2026-09-02.
- A MolSysViewer state document re-resolves onto another system by
  `(chain_id, group_id, group_name, atom_name)`. On this assembly that tuple has 1 588
  distinct values for 95 280 atoms, so re-resolution refuses rather than guessing.
  Correct on that side, and a second independent demonstration that the labels have
  stopped identifying.
