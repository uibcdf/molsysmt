# Testing Strategy

## Framework
Use `pytest`. Tests live under `tests/` and should mirror package structure.

## Fixtures
- Prefer shared molecular systems from `tests/conftest.py`.
- Avoid ad hoc downloads unless explicitly testing remote forms.
- Assert fixtures are not `None` to fail early.

## Optional Dependencies
Tests that require soft dependencies must guard availability and skip cleanly.

## Determinism
Tests must be deterministic and reasonably fast. Use bundled systems in
`molsysmt.systems` when possible.

## Peptide Builder Validation Policy
`build_peptide(engine="MolSysMT")` must be validated against `engine="LEaP"`
using two tiers:

- **Default CI/local tier (fast):** focused regression cases (including PRO-heavy
  junctions) plus a small deterministic random set of length-10 sequences.
- **Extended parity tier (slow/manual/nightly):** 40 deterministic random
  length-10 sequences compared against LEaP with explicit topology and geometry
  tolerances.

The extended suite is controlled by:

```bash
MSM_RUN_EXTENDED_PEPTIDE_PARITY=1 pytest -q tests/build/build_peptide/test_build_peptide_molsysmt_MolSys.py -k test_build_peptide_molsysmt_MolSys_12_extended_random_parity
```
