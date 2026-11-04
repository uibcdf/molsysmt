---
summary: Reconcile legacy amino-acid name mappings with native protonation labels
issue: uibcdf/molsysmt#549
status: active
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

**Reported:** 2026-11-03 while receiving #545/#547. **Status:** active; the
maintainer accepts the explicit scheme design below. Runtime cutover remains due.

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

The initial disposition is a stabilization review, not an automatic post-1.0
deferral. The maintainer accepts the scheme-aware direction on 2026-11-04.
No naming migration, runtime profile, schema field or public signature change is
implemented by this analysis/documentation checkpoint.

## Provenance

Local Linux, shared Python 3.14.7 and unchanged native backend. The native fragment
provenance is recorded in its bundled JSON and `make_peptide_chemical_templates.py`;
no upstream source or coordinate asset was changed.

## Source study — 2026-11-04

The [dated inspection record](../../devtools/data/name_scheme_review_549_20261104.json)
retains exact AmberClassic/MDTraj commits, the Amber library content digest,
native Meeko fragment provenance, bounded RCSB CCD observations and executed
native sequence probes. It is review evidence, not a new runtime dictionary.

Primary CCD metadata confirms independent meanings for HID, CYX and ASH
(non-peptide compounds), HIP (phosphonohistidine) and LYN (lysine amide).
The Amber peptide vocabulary uses the same labels for histidine, cysteine,
aspartate or lysine states. Even matching parent letters do not equate those
chemical meanings. GLH/HIE/CYM API requests returned 404; that observation does
not establish universal or historical CCD absence. The legacy table is mixed
historical data and must not be relabelled as a certified current CCD reference.

Native template-to-sequence calls on 5f3af9374 reproduce the public impact:
GLH gives Q; HID/HIE and a declared CYX pair fail with KeyError. Template group
labels remain as supplied and the bond table is unchanged by the queries.
This demonstrates incorrect or unavailable sequence projection for those native
templates, not a newly demonstrated wrong prepared graph, force-field charge or
coordinate calculation.

## Accepted design — 2026-11-04

The maintainer accepts the following decisions after the pros/cons discussion:

1. Preserve original group names and interpret them under a declared scheme.
   Do not choose a universal Amber or legacy interpretation implicitly.
2. Use `from_naming_scheme` for source interpretation in public conversion and
   `naming_scheme` for a direct name helper. `None` means no explicit override:
   read stored declarations, otherwise resolve only supported unambiguous names.
   Ambiguous or unassessed meanings require an actionable SMonitor diagnostic.
3. Detect contradictions between explicit and stored declarations. Missing
   metadata remains unknown, including on older files. File form, Python class,
   matching counts or historical preparation records are insufficient evidence.
4. Associate declarations with names in Topology at group granularity, supporting
   a mixed Amber-labelled protein and CCD-labelled ligand. MolSys coordinates
   the domain; ChemicalStates remains the assignment/connectivity owner.
5. Preserve declarations through native lifecycle operations, typed dictionaries
   and H5MSM. Select reviewed physical encoding and schema revisions before
   implementing writers; new reader behavior cannot silently reinterpret old
   bytes or discard a declaration. Root 0.5's modular layers permit a layer
   revision study; no root/layer/dictionary version is selected by this plan.
6. Make `molsysmt.element.group.get_1_letter_code_from_name` the canonical public
   entry point, reusing one private resolution authority. Update internal
   consumers, docs, stability records and bound-tool inventory together. Do not
   introduce duplicate name tables or infer an alphabet for arbitrary groups.
7. Document each supported scheme, definition version, provenance, accepted
   names and unsupported behavior, with explicit comparisons. Initial profile
   identifiers are amber, ccd and legacy, each bounded to its actually reviewed
   implementation. Do not advertise complete CCD or other-force-field support.

The direct scalar helper initially covers amino-acid projection. Naming
interpretation does not protonate, select a chemical state, generate coordinates
or chemically replace a modified group with its parent. General target-name
translation and atom naming remain separately scoped future operations; no
unused `to_naming_scheme` parameter is added merely to reserve a spelling.

## Documentation contract

The conceptual User Guide page
[Group naming schemes](../../docs/content/user/foundations/molecular_system/naming_schemes.md)
compares amber/ccd/legacy and marks the scheme-aware runtime/persistence contract
as planned. It links primary references and distinguishes independently verified
records from legacy compatibility values and unverified record lookups.

For the initial correction, the eight reviewed state labels require a declared
scheme. Canonical names can remain convenient where their requested
interpretation is unambiguous. Definition versions/snapshots and explicit
unsupported cases must appear in published support tables when implemented.
Keep the table aligned with one runtime authority; a future generated view may
report that authority but cannot substitute for scientific review of its entries.

## Implementation sequence and exit evidence

- [x] **D0 — bounded source study and public reproduction.** Verify the naming
  collisions, native sequence failures and provider/data provenance.
- [x] **D1 — maintainer decision and documentation plan.** Record defaults,
  domain ownership, mixed groups, relocation and the required user comparison.
- [ ] **D2 — typed naming declarations and schemas.** Choose group-aligned
  storage and the scheme/version registry; specify null/unknown and conflict
  rules, copy/extract/remove/merge/builder behavior, partial and atom-free native
  domains, dictionary and H5MSM readers/writers. Reject declared unsupported
  persistence rather than losing context. Do not require coordinates for names.
- [ ] **D3 — shared private resolver and public helpers.** Add independent
  Amber/CCD/canonical/legacy controls, refusal paths and immutable-input tests;
  introduce the group-level public code helper with ArgDigest and SMonitor.
  Keep modified-parent projection distinct from chemical replacement.
- [ ] **D4 — native producers and consumer propagation.** Producers that
  explicitly know their input vocabulary declare it. Propagate the conversion
  argument through selected direct and MolSys routes. Resolve declarations per
  selected group, preserve ordering/repetitions and refuse ambiguous mixed
  overrides. Audit sequence, recognition, missing-atom/H and preparation callers
  so a name-only lookup cannot select chemistry implicitly.
- [ ] **D5 — persistence and lifecycle receiving.** Exercise mixed schemes,
  unknown declarations and conflicting overrides across source maps, copies,
  extraction/reordering, merging, atom-free sequences and H5MSM/dictionary round
  trips. Old files retain unknown context; no implicit online enrichment.
- [ ] **D6 — coordinated public cutover and documentation.** Move the public
  code entry point, update old-path consumers and PR #543's mirror/manifest,
  User Guide, Cookbook, course, API help and stability/tier inventories. Any
  necessary bounded compatibility alias needs an explicit removal condition.
- [ ] **D7 — final receiving and closure.** Verify exact-source guards, units
  where other operations carry quantities, source/chemistry preservation,
  documentation execution, Ruff and required gates. Close #549 only with its
  addressable guard and public evidence. Installed-client/release qualification
  remains under #334; this plan does not qualify or publish a package.

Do not patch GLH globally to E, add all state aliases to the historical table,
rename source groups during conversion or infer a scheme from native form as an
interim shortcut. Those approaches would hide the confirmed cross-scheme
collisions. Reassess progress at the phase exits rather than estimating an
unmeasured completion percentage.

## Documentation checkpoint validation — 2026-11-04

The selected heading/source-boundary/directive/notebook-schema suite passes
533 cases with zero failures or omissions and 514 Sphinx/MyST deprecation
warnings. The new conceptual page also renders independently with strict Sphinx
(`-W --keep-going`), retaining its pending-implementation warning and PyData
table markup. This is a bounded page render, not a complete site/release build.
Developer-guide, generated-index and diff checks pass. No runtime or schema is
implemented, and the four pre-existing generated API edits remain untouched.
