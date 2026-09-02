---
summary: After make_bioassembly, a chain-and-residue selection silently returns every copy
issue: uibcdf/molsysmt#198
status: resolved
opened: 2026-09-02
closed: 2026-09-02
severity: medium
verification: reproduced
area: [build, selection]
guard: tests/build/make_bioassembly/test_make_bioassembly.py::test_generated_copies_receive_unique_chain_ids_and_keep_author_names
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

## Decision

`chain_id` is the local, addressable identity and must be unique in the generated
assembly. `chain_name` is the author-provided name and may repeat legitimately. The
1BRS BCIF makes the distinction explicit: its twelve `label_asym_id` values map to
`chain_id` values `A` through `L`, while its `auth_asym_id` values map to the repeated
`chain_name` sequence `A` through `F`, twice.

`make_bioassembly` therefore preserves the first occurrence of every source `chain_id`
and replaces only collisions in later generated copies. Replacement identifiers use
the repository's established uppercase sequence: `A` through `Z`, then `AA`, `AB`, and
so on. Allocation follows output chain order and skips every source identifier, so a
generated identifier cannot displace a source identifier that occurs later.

Author names are copied unchanged. Legacy PDB output remains a separate representation
constraint because its chain field cannot encode multi-character identifiers; this fix
must not truncate identifiers while constructing the assembly.

## Implementation

Before merging the transformed units, `make_bioassembly` now collects every source
`chain_id`, reserves those values, and walks the units in output order. The first
occurrence of a source identifier is unchanged. Every later collision receives the
next free value from `molsysmt.element.chain.all_chain_names`. Only `chain_id` is set;
the copied `chain_name` column and all other element identifiers remain untouched.

The docstring and the User Guide describe the distinction between local identity and
author naming. The three path-specific course modules that call `make_bioassembly`
carry the same contract; the Antiviral path does not call this function.

## Validation

The contract test uses the bundled 1BRS BCIF, whose source fields provide the needed
counterexample without network access: twelve unique chain IDs `A` through `L`, but
author names `A` through `F` repeated twice. Three identity copies produce 36 unique
IDs `A` through `Z`, then `AA` through `AJ`, while the complete author-name sequence is
preserved three times. Selecting `chain_id == 'A'` in the assembly returns exactly as
many atoms as it does in the source, rather than all generated copies.

Validation commands:

```text
pytest -q --receptor=llm tests/build/make_bioassembly/test_make_bioassembly.py
pytest -q --receptor=llm --doctest-modules molsysmt/build/make_bioassembly.py
ruff check molsysmt/build/make_bioassembly.py tests/build/make_bioassembly/test_make_bioassembly.py
python devtools/scripts/validate_docstrings.py
```

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
