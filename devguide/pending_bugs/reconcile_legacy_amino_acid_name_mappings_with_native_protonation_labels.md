---
summary: Reconcile legacy amino-acid name mappings with native protonation labels
issue: uibcdf/molsysmt#549
status: open
opened: 2026-11-03
closed:
severity: medium
verification: reproduced
area: [attribute, build]
guard:
normative:
blocked_by: []
supersedes: []
---

# Legacy names versus explicit native protonation labels

**Reported:** 2026-11-03 while receiving #545/#547. **Status:** open; a bounded
naming-context decision and native repair remain due.

## What

The current public one-letter/name helpers disagree with the explicit native
protonation-template vocabulary. `get_1_letter_code_from_name('GLH')` returns Q
and `get_standard_name('GLH')` returns GLN. HID/HIE raise KeyError in the one-letter
helper. The native pinned peptide-fragment inventory includes GLH, HID and HIE;
GLH has OE1/OE2 side-chain oxygen atoms, unlike GLN's terminal amide nitrogen.

```python
from molsysmt.element.group.amino_acid import get_1_letter_code_from_name, get_standard_name
print(get_1_letter_code_from_name('GLH'), get_standard_name('GLH'))
# Q GLN
get_1_letter_code_from_name('HID')  # KeyError
```

## How

The legacy MDTraj-derived `element/group/amino_acid/group_types.py` table and the
separately curated `data/databases/peptide_templates/residue_fragments.json` have
different vocabularies. A name-only helper lacks an explicit dialect or molecular
chemical context; simply broadening recognition can conflate old catalogue names
and force-field state labels. Inspect the original legacy source and the pinned
Meeko/Amber naming profiles before choosing the supported interpretation.

## Why

Sequence labels, canonical-parent reporting and preparation should not silently
imply different identities for a name produced by native workflows. No incorrect
prepared graph or downstream charge calculation was demonstrated by this report;
the observed defect is the public naming-contract mismatch.

## What is measured and what is assumed

The values and missing-key failures above were executed with Python 3.14.7 on
main be2f3fb7cb6ac0e52170669edea165166899ad3c plus the bounded #545 canonical-code
repair. Existing variants are unchanged by that repair. Two newly authored tests
incorrectly assumed HID support and GLH/E in the unqualified legacy helper; they
failed. They are not converted into assertions that Q is chemically correct.
Those external-profile assumptions are removed from #545's acceptance tests and
are instead the explicit scientific question recorded here.

## What was refuted

This is not the missing XLE/XAA canonical-table route fixed by #545. The mismatch
already exists in the prior variant catalogue and is retained by the bounded
repair. Code-table parity cannot establish the chemical interpretation of GLH.

## Scope and acceptance

Decide the public naming context and supported native protonation-label contract;
resolve GLH/HID/HIE consistently in name/code helpers and relevant consumers.
Audit additional CYM/CYX/LYN and other colliding labels rather than guessing an
exhaustive mapping. Add independent semantic controls and builder-to-name/sequence
round trips. Preserve ChemicalStates as the chemical-assignment owner: lookup
must not protonate, replace chemical graphs or choose a state implicitly.

The initial disposition is an open stabilization review, not an automatic
post-1.0 deferral. No naming migration, legacy-table update, additional chemical
profile or public signature change is implemented here.

## Provenance

Local Linux, shared Python 3.14.7 and unchanged native backend. The native fragment
provenance is recorded in its bundled JSON and `make_peptide_chemical_templates.py`;
no upstream source or coordinate asset was changed.
