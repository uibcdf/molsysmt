---
summary: Descriptor SDF reference fixtures duplicate V3000 valence on supported RDKit writers
issue: uibcdf/molsysmt#627
status: resolved
opened: 2026-11-06
closed: 2026-11-06
severity: medium
verification: reproduced
area: [tests, form]
guard: tests/physchem/test_sdf_reference_valence.py
normative:
blocked_by: []
supersedes: []
---

# Keeping descriptor reference CTAB fixtures valid across RDKit writers

**Reported:** 2026-11-06 during #524's optional-provider receiving under #334.
**Status:** Test-only repair and paired provider receiving complete; public delivery and board closeout follow.

## What

The TPSA and lipophilicity cross-form tests start from RDKit's V3000 writer,
then blindly append `VAL` to every atom. Supported RDKit 2024.03.4 already
writes that field for several charged atoms. The resulting fixtures contain
duplicate `VAL=1` or `VAL=4` fields. The native reader correctly rejects them;
the tests incorrectly present malformed fixtures as a provider/form failure.

## How

```bash
python -m pytest --receptor=llm -n 12 \
  tests/physchem/test_get_tpsa.py tests/physchem/test_get_lipophilicity.py
```

Use the hash-verified public RDKit 2024.3.4 cp312 wheel and the received public
support-library floors on the existing Python 3.12 interpreter. The complete
535-case runtime selection exits one with four failures, 530 passes and one
explicitly conditional SMILES-negative-case omission. Its invocation and XML
are retained as `524-rdkit-floor312-features*` in the audit cache.

Each affected test calls `MolToV3KMolBlock` then appends a computed total valence
without examining the property already emitted. The native parser supports
bounded declared valence and deliberately rejects repeated properties. No
production parser or descriptor defect is established by these counterexamples.

## Why

Invalid reference fixtures create false compatibility failures and could lead
to an unjustified higher RDKit floor or weakened parser checks. The scientific
score and state-preservation assertions must stay unchanged. Generate valid
independent reference data for both conforming writer variants instead.

## What is measured and what is assumed

The eight new native RDKit API/unit/CIP/correspondence guards pass at 2024.3.4.
Four existing SDF descriptor cases fail on duplicate fields. Current source
inspection confirms `VAL` is already accepted by the parser and native chemical
state translation. The initial conversational hypothesis of missing parser
support was corrected before any production change or issue publication.

## Intended repair and exclusions

Share a small private test-reference helper for the two consumers. Keep the
real upstream writer, add a missing explicit valence, preserve a matching
field, and reject conflicting or repeated declarations. Preserve charge,
other atom properties and fixed-state H evidence. Add a regression exercising
writer variants independently of the installed provider's omission choices.
Do not change production parsing, infer chemistry, suppress strict errors,
relax score/state assertions or raise a version floor to bypass these tests.

## Acceptance criteria

- Both ordinary omitted and already-present writer variants yield exactly one
  matching valence declaration and unchanged unrelated fields.
- Conflicting or repeated reference fields remain explicit failures.
- Native H/charge interpretation and both scientific score assertions survive.
- Minimum/newer actual provider receiving includes the guards; native exit,
  known omission and earlier failures remain in the source receipt.
- Publish the source, owning record and addressable guard and independently
  receive them before closing #627. The wider #524 review stays separate.

## Provenance

Linux x86_64; Python 3.12.12, public RDKit 2024.03.4, NumPy 2.3.5 and public
support floors. Source basis dd60ee7d6 with the pending API-grounded optional
floor declaration and the eight new native guards. No environment or native
backend was replaced; no production CTAB/descriptor implementation was changed.

## Resolution — 2026-11-06

Source `13b82905c870253ef52224ad5801d399b69db22a` shares the independent
RDKit reference writer between the descriptor tests. It adds only a missing
`VAL`, preserves a matching field and all unrelated writer bytes, and explicitly
rejects conflicting or repeated evidence. Every prior scientific score and
chemical-state assertion is unchanged. Production parsing and descriptor
implementations are untouched.

The seven-case guard forces both conforming writer variants independently of
the installed RDKit behavior, checks native H/charge interpretation and both
scores, preserves unrelated quoted properties and verifies that duplicate
properties still fail the native parser. This protects the actual fixture
failure rather than merely inspecting helper source or a formatted string.

Final minimum RDKit 2024.3.4/Python 3.12/public-support-floor receiving and
published RDKit 2025.9.5/Python 3.14 each pass 541 cases with one conditional
SMILES-negative-case omission. CCO is valid SMILES when RDKit is installed;
positive CCO parsing/conversion is separately exercised. No scientific score,
state assertion or required provider operation is skipped to fix the defect.
The original four failures remain separate in the
[receiving receipt](../../../devtools/data/rdkit_runtime_receiving_524_627_20261106.json).

The same receipt grounds the separate optional API minimum declaration in
`883e4e45ad86e065c092001dd973a02a991f227b`, retains public wheel identities,
known strided-array protection, original exploratory comparator failure and
unchanged native backend. This is source receiving, not installed-artifact,
whole-platform, Viewer or release qualification. #524 remains partial.
