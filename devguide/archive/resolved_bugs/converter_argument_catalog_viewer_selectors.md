---
summary: Generated converter argument catalog omits current ViewerJSON selectors.
issue: uibcdf/molsysmt#416
status: resolved
opened: 2026-10-22
closed: 2026-10-22
severity: low
verification: reproduced
area: [tests]
guard: tests/test_argument_contract.py::test_the_converter_table_still_matches_the_converters
normative:
blocked_by: []
supersedes: []
---

# Generated converter argument catalog omits current ViewerJSON selectors

**Reported:** 2026-10-22, during the complete local suite requested after #411.
**Status:** Resolved and locally contract-tested.

## What

The committed generated argument union for molsysmt.ViewerJSON lacks atom_indices and structure_indices from current converter signatures.

## How

Run python devtools/scripts/generate_converter_arguments.py --write and review its output. The sole generated diff adds those two names to the existing target union. Do not change the producer or weaken the public keyword domain.

## Why

The argument catalog must agree with the converter signatures it represents. Its exact-derivation guard is retained unchanged.

## What is measured and what is assumed

Both the complete test and a fresh python devtools/scripts/generate_converter_arguments.py --check fail before regeneration. The generated diff changes only two entries; 94 other target unions remain unchanged.

The initial command `python -m pytest --receptor=llm -n 12` records 15,046
passes, 13 failures and two skips in 459.36 seconds. Its other failure themes
are separate: #411 and #414–#417. The intended closing guard is `tests/test_argument_contract.py::test_the_converter_table_still_matches_the_converters`.

The combined affected command passes 138 cases:

```bash
python -m pytest tests/physchem/test_chemical_template_context.py tests/physchem/test_normalize_aromatic_bond_orders.py tests/physchem/test_chemical_preparation_evidence.py tests/heavy/test_native_modular_sources.py tests/test_argument_contract.py tests/test_form_plugin_conventions.py tests/interactions/test_h5msm05.py tests/basic/convert/one_to_one/test_h5msm_handler_version_boundary.py tests/native/test_chemical_states.py --receptor=llm -n 12
```

The final complete command `python -m pytest --receptor=llm -n 12` passes
**15,066 cases with two skips**, exit 0, in 416.96 seconds (1,726 warnings,
52 warning groups). The skips are the CuPy path without CuPy and the
without-RDKit SMILES fallback when RDKit is present. This is a local
Linux/Python 3.14 development result, not a platform matrix or installed-pair
qualification. Source includes the combined #411/#414–#417 repairs.

## What was refuted

The initial failure does not by itself demonstrate a regression in scientific
results or higher memory use. Diagnose the actual contract and guard before
changing production behavior to satisfy an outdated expectation.

## Scope and exclusions

This is bounded stabilization of the local suite and its derived argument
contract. It does not change scientific methods, native invalidation policy,
public form support, dependency floors or release approval. Scientific and
installed-candidate qualification remain separately required under #334.

## Acceptance criteria

The named guard and adjacent affected tests pass without dropping their
scientific/ownership checks or allowing arbitrary unknown converter keywords.
The complete local suite is rerun after the bounded repairs.

## Provenance

Linux x86_64, Python 3.14.7, NumPy 2.4.6, h5py 3.16.0, pytest 9.1.1,
pytest-xdist 3.8.0, Pytest Receptor 1.2.1+22.g00a31c4, 2026-10-22.
Source baseline 70103677841fba359c7e1ca9b092d04d41e5807e plus the #411 change.
