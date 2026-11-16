---
summary: mmCIF declared covalent links lose their source identifier correspondence
issue: uibcdf/molsysmt#766
status: resolved
opened: 2026-11-15
closed: 2026-11-15
severity: high
verification: measured
area: [form, convert]
guard: tests/form/mmcif_PdbxContainers_DataContainer/test_declared_covalent_links.py
normative:
blocked_by: []
supersedes: []
---

# mmCIF declared covalent endpoint correspondence

**Reported:** owner receiving of unchanged 3WU2 while repairing #763.
**Status:** resolved in source with independent endpoint/model and original-file controls.

## What

The original public conversion raises IndexError on a declared `struct_conn`
covalent link, even when both endpoints exist. A two-atom independent control
reproduces it with `get_missing_bonds=False`:

```bash
python -m pytest --receptor=llm -n0 tests/form/mmcif_PdbxContainers_DataContainer/test_declared_covalent_links.py::test_numeric_native_group_ids_do_not_lose_declared_covalent_links
```

## How

The converter compares a textual source `auth_seq_id` with a native numeric
group ID. It also compares `label_atom_id` with the author atom name. The
previous group-first search does not retain the endpoint's insertion-code and
model namespace. After fixing source lookup, the new two-model controls expose
another stale-axis error: the cross-chain warning dereferences pre-extraction
atom indices after the separate models have been reduced to one atom axis.
That intermediate run fails 15 of 106 controls and is preserved as failed.

## Why

CIF/BinaryCIF and compressed public readers share this route. Explicit covalent
evidence must not disappear, move to the wrong atoms or prevent a valid source
from loading. #763's earlier entity failure hid this independent defect on
3WU2; correcting only entity allocation was insufficient.

## What is measured and what is assumed

The causal tiny control fails before the fix. The corrected 32 endpoint cases
cover five entry forms, one/two models, distinct author/label atom names,
insertion codes and an unmappable endpoint. They pass alongside #763's 74
identity controls. The affected complete cohort passes 961 cases without skips.
Both unchanged originals pass all eight policy/unit combinations, with
independent retained-source-label joins checking every admitted covalent pair
and its explicit evidence. These are measured source contracts, not complete
bond inference, alternate-location chemistry or installed-pair qualification.

The [combined receipt](../../../devtools/data/mmcif_entity_identity_receiving_763_766_20261115.json)
retains actual commands, native exits, receptor/JUnit reconciliation, original
hashes, negative and operator-error invocations and bounded resource measurements.

## What was refuted

Normalizing source endpoint labels through native numeric group IDs does not
preserve the deposited namespace. Author and label atom names are not
interchangeable. Restricting the input or disabling declared links is not a
repair. Model-global atom positions also cannot be used on the later extracted
model's compact axis.

## Scope and exclusions

Only the existing admitted `conn_type_id == 'covale'` profile is changed. A
sparse endpoint index scans source atoms once, then joins each declaration
within common models using original label-chain, author-sequence, insertion
and label-atom keys. Supplied alternate/component labels constrain candidates.
No matching common-model endpoints raises the existing SMonitor FormatError;
input is not mutated. The existing bond accumulator retains explicit evidence.
The warning is rendered on the matching atom axis before model extraction.
No optional dependency, native kernel, new covalent-inference rule, disulfide
profile, periodic-image interpretation or alternate-location policy is added.
The resolver remains private inside the existing format-specific bond helper.

## Acceptance criteria

The public two-atom oracle must retain exactly bond [0, 1] with explicit
evidence; all supported entry forms and compatible two-model ensembles must
preserve that identity. Distinct author names and insertion codes must work;
unmappable declarations must fail clearly without modifying input. Both
originals, adjacent regressions and relevant quality/documentation checks must
be received without changing source input bytes.

## Provenance and resolution

2026-11-15, Linux, existing Python 3.14.7 and the recorded frozen support-source
profile, parent ca3071960. Native binary 4ffb82e4 remains unchanged. Execution
uses one CPU and 2 GiB per job, at most two owned concurrent jobs, no own swap
and a 6.5-GiB host reserve. The independent source expectations—not the helper's
returned pairs—supply the guard. No shared-prefix mutation, new build, hosted
matrix or publication occurs.
