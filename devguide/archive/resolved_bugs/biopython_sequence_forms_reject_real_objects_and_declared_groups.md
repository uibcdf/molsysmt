---
summary: Biopython sequence forms reject real objects and cannot deliver declared groups.
issue: uibcdf/molsysmt#359
status: resolved
opened: 2026-10-09
closed: 2026-10-09
severity: medium
verification: reproduced
area: [form, attribute]
guard: tests/form/biopython_Seq/test_group_queries.py::test_real_biopython_sequence_group_queries
normative:
blocked_by: []
supersedes: []
---

# Biopython sequence forms reject real objects and declared groups

**Reported:** 2026-10-09, during the maintainer-authorized pre-1.0 issue audit.
**Status:** Resolved for sequence recognition and the two declared group queries.

## What

Real Biopython objects fail the public input boundary:

```python
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import molsysmt as msm

msm.get_form(Seq("AGX"))
# NotSupportedFormError
msm.get(SeqRecord(Seq("aGx")), element="group", group_name=True)
# ArgumentError: input is not a recognized molecular system
```

Both adapters also declare `group_index` and `group_name` without getters or a
semantics-preserving delivery pipe. The delivery audit reports those four bits.

## How

The recognizers in `molsysmt/form/biopython_Seq/is_form.py` and the corresponding
SeqRecord module compare Python class names with `biopython.Seq` and
`biopython.SeqRecord`. The actual class names are `Bio.Seq.Seq` and
`Bio.SeqRecord.SeqRecord`. Their topological getter modules were empty.

The repair recognizes the actual class names while retaining the established
public form names. Direct, digested group getters return source sequence
positions and characters. SeqRecord delegates to its sequence without changing
its ID, annotations or content.

## Why

Even these two declared read-only queries fail on normal inputs. Sequence-only
systems cannot provide atomic chemistry, but they can safely provide sequence
positions and characters. Keeping the capabilities declared and actually
implementing them is preferable to masking the defects by removing declarations.

## What is measured and what is assumed

Manual public calls reproduced rejection for both forms and all, reordered and
empty selections before repair. After repair:

```bash
python -m pytest tests/form/biopython_Seq/test_group_queries.py \
  molsysmt/form/biopython_Seq/get_topological_attributes.py \
  molsysmt/form/biopython_SeqRecord/get_topological_attributes.py \
  --doctest-modules --receptor=llm -n12
python devtools/scripts/validate_form_adapters.py
```

The first command passes 13 facade tests and four docstring examples. The audit
reports 96 structurally valid forms and 74 unreachable declarations across seven
forms, down from 78 across nine. Only the four resolved baseline bits were removed.

## What was refuted

The missing delivery is not a reason to infer three-letter amino-acid names,
atom inventories or chemical states from arbitrary sequences. Source characters
and positions are sufficient for the declared query. A record's ID does not
replace sequence-position indices.

## Scope and exclusions

Known-empty sequences return empty lists. Undefined or partially defined content
returns `None` for names while retaining known positions. An absent record sequence
returns `None` for both attributes. `has_attribute(..., include_none=False)` follows
those distinctions. Selection order and repetitions are preserved.

This repair does not certify sequence copy/conversion/editing workflows, promote
the Tier 2 forms or close the broader uibcdf/molsysmt#139 delivery debt. No new
hard dependency, atomic topology or structural information is introduced.
The frozen release candidates and publication pause remain unchanged.

## Acceptance criteria and resolution

The guard queries real objects through `msm.get_form` and `msm.get`, using list
and dictionary outputs and all, repeated, reordered, scalar and empty selections.
It asserts the exact source-position/name pairing and source immutability, so a
recognizer regression or empty/stub getters cannot satisfy it. Companion guards
cover missing and empty information. Foundations, both form tutorials, the
conversion cookbook and Common Core Module 8 describe this boundary.

## Provenance

Linux, Python 3.14.7, shared `molsyssuite@uibcdf_3.14` development environment,
2026-10-09. Biopython is optional and available for this local qualification.
