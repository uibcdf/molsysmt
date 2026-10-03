---
summary: SDF identity copies require native chemical interpretation
issue: uibcdf/molsysmt#302
status: resolved
opened: 2026-10-03
closed: 2026-10-03
severity: medium
verification: reproduced
area: [form, convert]
guard: tests/form/file_sdf/test_native_contract.py::test_identity_preserves_unrepresented_chemistry_without_inspection
normative:
blocked_by: []
supersedes: []
---

# SDF identity copies require native chemical interpretation

**Reported:** 2026-10-03, while validating original AutoDock Vina examples for
uibcdf/molsysmt#214/#215 and the consumer profile in uibcdf/dockingmt#33.
**Status:** Resolved; opaque identity operations no longer require semantic decoding.

## What

An unselected source-to-SDF copy rejected chemistry outside the native parser
profile, although its operation preserves bytes rather than projecting chemistry:

```python
import molsysmt as msm
msm.convert('tests/form/data/vina_examples/1iep_ligand.sdf',
            to_form='/tmp/copied.sdf', strict=True)
```

At `bbeeb72cf`, this raises for the atom valence override. The versionless
1S63 example similarly fails. Both are accepted by the independent RDKit
reference reader, but remain outside native projection's documented subset.
`msm.copy` also called the semantic parser before preserving the source bytes.

## How

`molsysmt/form/file_sdf/to_file_sdf.py` called `read_sdf` on its identity branch.
`molsysmt/_private/conversion_report.py` also audited chemical attributes before
recognizing identity; strict public conversion therefore failed during preflight.

Factor the streaming single-record reader in `molsysmt/_private/ctfile.py` and
introduce a private envelope validator. It checks header/count fields and the
`M  END` / `$$$$` boundaries without interpreting atom/bond semantics or SD
property grammar. Use it in both the identity converter and its exhaustive
byte-preservation report. Native projection, getters and explicit subsets keep
the original semantic decoder and rejection rules.

## Why

This breaks opaque source preservation needed by ligand-interchange workflows.
It also confuses an exact preservation report with evidence of chemical
interpretation. The fix permits retention without claiming that unsupported
source chemistry has become native-readable or chemically prepared.

## What is measured and what is assumed

**Reproduced:** the original reference matrix failed both identity copies at
`bbeeb72cf`. Published source bytes, upstream commit and SHA-256 are recorded in
`tests/form/data/vina_examples/manifest.json`.

**Contract-tested:** the synthetic guard replaces `read_sdf` with an assertion
failure, checks report/strict conversion/copy, verifies CRLF byte equality, and
then checks that native projection still rejects the valence override. Separate
negative envelope cases protect existing destinations from mutation.

No chemical-validity, broad CTfile compatibility or performance claim follows
from a successful copy. Full final regression evidence is recorded below.

## What was refuted

- Removing source valence/version fields would change the real control and
  conceal unsupported semantics.
- Routing identity through an optional toolkit would add interpretation to an
  operation that needs only byte preservation.
- Disabling strict reporting would leave the ordinary copy defect and the
  report's mistaken chemical dependency in place.

## Scope and exclusions

Only unselected SDF identity operations are opaque: literal `selection='all'`
and `structure_indices='all'`. Explicit index lists require native interpretation.
This does not admit valence overrides or versionless CTAB into native domains,
validate arbitrary chemical/property grammar, or support multiple records.
Those format extensions retain ownership in uibcdf/molsysmt#215.

## Acceptance criteria

- Report, strict public conversion and copy preserve unsupported single-record
  chemistry without calling its decoder.
- Malformed or multiple-record envelopes fail before destination writes.
- Native projection and selected operations retain their documented profile.
- User Guide, Toolbox, Cookbook and the introductory course distinguish byte
  identity from chemical interpretation.

## Provenance

Linux x86_64, Python 3.13.14; NumPy 2.4.6, RDKit 2025.9.5, MDAnalysis 2.10.0,
Vina 1.2.7, pytest 9.1.1, PyUnitWizard 0.25.0+7.g00d756c; 2026-10-03.
Baseline: `bbeeb72cf`. The independently installed readers are optional test
providers, not new runtime dependencies.

## Resolution — 2026-10-03

The envelope validator is shared by opaque copies and their reports. The guard
proves that none calls the semantic decoder, preserves exact source bytes, and
retains rejection for native projection and explicit selections. The malformed
single-record controls also preserve existing destinations on failure.

The following focused regression passed **418 tests in 104.48 seconds**, with
nine reported warnings (MDAnalysis mass guessing, structural-attribute drops in
existing composition controls, and a NumPy binary-size runtime warning):

```bash
python -m pytest --receptor=llm tests/form/file_sdf tests/form/file_pdbqt \
  tests/topology/test_get_rigid_fragments.py \
  tests/topology/test_rigid_fragments_real_vina_examples.py \
  tests/basic/test_get_conversion_report.py \
  tests/basic/convert/test_conversion_preflight.py
```

After adding explicit-selection assertions, the addressable guard passed again
(1 test, 3.42 seconds). The SDF adapter doctest passed independently (1 test,
3.62 seconds). These selections overlap; their counts are not a full-suite total.
Ruff, dependency validation, public docstring validation and course validation
passed. User-facing documentation distinguishes byte preservation from chemical
interpretation. Native SDF admission of the two reference chemistries remains
pending in #215; no implicit parser fallback or chemical preparation was added.
