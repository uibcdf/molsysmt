---
summary: Topology with ChemicalStatesDict and Structures bypasses native domain composition.
issue: uibcdf/molsysmt#532
status: active
opened: 2026-11-03
closed:
severity: medium
verification: reproduced
area: [native, convert, form]
guard:
normative:
blocked_by: []
supersedes: []
---

# Explicit inventory plus dictionary chemistry cannot compose a MolSys

**Reported:** while building independent #531 regression inputs.
**Status:** correction locally qualified; hosted qualification pending.

## What

The native three-domain composition route accepts ChemicalStates but falls
through to generic attribute setters when its chemical provider is a
ChemicalStatesDict. The documented equivalent typed-domain combination fails.

```python
import numpy as np
import molsysmt as msm
from molsysmt.native import MolSys

source = MolSys(n_atoms=1)
source.structures.append(
    coordinates=msm.pyunitwizard.quantity(np.zeros((1, 1, 3)), 'nm'))
payload = msm.convert(source.chemical_states,
                      to_form='molsysmt.ChemicalStatesDict')
msm.convert([source.topology, payload, source.structures],
            to_form='molsysmt.MolSys')
```

Observed: InternalAlgorithmError and diagnostics about missing setters for
state/chemical fields on stable Topology or Structures.

## How

The explicit dictionary chemical provider is not received by the native triple
composition route. Its fallback tries to flatten chemical collection attributes
through generic setters. The public convert Notes and maintained migration
guide admit dictionary chemical providers alongside independent domains.

## Why

Consumers should not need an extra manual chemical decoding step merely because
stable inventory is also present. Preserve independent domain ownership rather
than adding state/component setters to Topology.

## What is measured and what is assumed

Reproduced on source 00abb958fb93649131d5ce5fe5e12e90cf4900e9 and rechecked
while correcting unrelated #531. The same one-atom source yields:

- Native Topology/ChemicalStates/Structures triple: succeeds with topology.
- ChemicalStatesDict/Structures pair: succeeds without topology.
- Topology/ChemicalStatesDict/Structures triple: InternalAlgorithmError.

## What was refuted

The source axes match and native composition succeeds. No chemical perception,
trajectory file, viewer, aromaticity or geometry calculation is required. The
#269 two-domain dictionary pair remains repaired; this is a different input
combination after the #255 native-model cutover.

## Scope and exclusions

Receive the explicit dictionary provider through the existing ChemicalStates
decoder and composition owner, preserving selection, source nonmutation,
reference state, units and honest structure/state associations. Do not restore
chemical facades in Topology, silently overwrite domains or infer correspondence
from equal counts. This bounded source correction does not qualify a release.

## Acceptance criteria

Public native/dictionary parity with an explicit Topology, both supported input
orders, valid selected axes, mismatched-domain refusal and source nonmutation.
Keep the already-supported native triple and topology-free pair as controls.

## Workaround

Explicitly convert the dictionary to ChemicalStates before composing the triple.

## Implementation and verification (2026-11-03)

The standalone composition owner now recognizes ChemicalStatesDict as the same
explicit chemical domain as ChemicalStates. It rejects repeated providers before
decoding, uses the existing public conversion/typed decoder once, and delegates
full-axis validation, owner binding and projection to the existing native tools.
No Topology facade, schema, public argument, scientific rule or dependency floor
changes. The coordinate-only foreign-provider and topology-free pair routes keep
their existing dispatch.

The accepted original-source replay of
`tests/basic/convert/mult_to_one/test_convert_chemical_and_structural_domains.py`
produced **16 failed / 40 passed**, exit 1, all sixteen failures from the reported
generic-setter fallback. The same 56 cases pass after the correction, exit 0,
with no omissions. Earlier test-authoring runs used a read-only coordinate buffer
and then the wrong setter keyword; those harness errors are not product evidence.
Three extra controls cover zero-state dictionaries and the optional mechanics
domain. All **59 focused cases** pass, exit 0, with no omissions. The first
broader run also exposed a test-only NumPy assertion on an object-backed mechanics
array; the final assertion reads the existing public numeric getter instead.
That harness failure does not indicate a composition or chemistry defect.

The controls compare literal atom labels, both chemical states and their bonds,
reference/provenance, nonconsecutive and repeated structure indices, zero-length
selections, nm/angstrom geometry, ps/fs time, and default result independence.
They cover all six three-domain input orders, native/dictionary chemistry,
full-axis conflict rejection before selection, duplicate/mixed chemical providers,
explicit copy policy and the public selected H5MSM round trip.

Local logs and typed receptor/JUnit evidence are retained in the ignored
`.pytest_cache/domain-composition-532/` directory. Source results do not qualify a
new installed package, consumer suite or public release.

Final local broader selection: **2,740 passed**, zero failures/omissions, exit 0,
138.14 s, with 737 visible existing warnings (mostly legacy H5MSM reads):

```bash
python -m pytest --receptor=llm -n 2 tests/native \
  tests/basic/convert/mult_to_one tests/form/molsysmt_ChemicalStatesDict \
  tests/form/molsysmt_MolSysDict tests/form/file_h5msm \
  tests/basic/test_extract.py tests/basic/test_extract_extended.py \
  tests/basic/test_permute_atoms.py
```

The existing Linux development environment uses Python 3.14.7, Pandas 2.3.3,
NumPy 2.4.6, pytest 9.1.1 and Pytest Receptor 1.2.1+22.g00a31c4. These are
editable-source results with the existing frozen Viewer runtime shim for the
audited ca7ebea60d530a7a0c65cb4d0ccea7b4288f3352 source; no new environment,
installation or Rust build was made. Receptor primary streams are complete,
session-complete and integrity-valid. The actual failing exits remain retained.

All 14 fast gates pass. Whole-repository `ruff check .` and
`ruff format --check .` pass (4,299 formatted files), as do nine test-command
controls and 507 dependency-route/notebook-schema controls. The three notebook
edits change prose only: code cells, outputs and execution metadata are unchanged.
The focused module is included in both aligned native smoke command lists so
hosted Pandas compatibility exercises the same public regression.

## Provenance

2026-11-03, Linux x86_64, existing Python 3.14.7 / Pandas 2.3.3 development
environment. Small synthetic molecular domains; no extra environment or build.
