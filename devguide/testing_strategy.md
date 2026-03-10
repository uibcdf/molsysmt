# Testing Strategy

## Framework
Use `pytest`. Tests live under `tests/` and should mirror package structure.

## 🥇 Contract Testing (The 1.0.0 Standard)
Contract tests are the primary defense against regressions in interoperability. 
- **Identity Goal**: Ensure that `msm.get`, `msm.select`, and `msm.convert` return structurally and mathematically identical results regardless of the input form (Native, OpenMM, MDTraj, etc.).
- **Parity Tolerance**: Coordinates and box vectors must match within $10^{-5}$ nanometers.
- **Selection Consistency**: Selection strings must return the exact same atom indices across all Tier 1 forms.

## 🧹 Legacy Cleanup Policy
The 1.0.0 transition (specifically Lazy Loading 2.0) has rendered many old tests obsolete or broken due to changed import patterns.
- **Rule**: If a test in `tests/form/` or `tests/basic/` fails because of architectural changes, do not "patch" it with dirty hacks. If the test is redundant with a new Contract Test, **delete it**. If it tests unique logic, **refactor it** to use absolute imports and ArgDigest-compliant calls.

## Fixtures
- Prefer shared molecular systems from `tests/conftest.py`.
- Avoid ad hoc downloads unless explicitly testing remote forms.
- Assert fixtures are not `None` to fail early.

## Optional Dependencies
Tests that require soft dependencies must guard availability and skip cleanly.

## Determinism
Tests must be deterministic and reasonably fast. Use bundled systems in
`molsysmt.systems` when possible.

## Sequential validation rule for stabilization sprints

When the suite is in broad stabilization mode, prefer sequential validation by
top-level test directories over a single very large `pytest` invocation. This
gives cleaner checkpoints and isolates the next blocking failure without
discarding useful progress from earlier slices.

Current validated sequence in the March 2026 pass:
- `tests/basic`
- `tests/build`
- `tests/form`
- `tests/structure`
- `tests/thirds`
- `tests/topology`
- `tests/native`
- `tests/cross_repo`
- `tests/hbonds`
- `tests/molecular_mechanics`
- `tests/pbc`
- `tests/physchem`

Next slice to resume:
- `tests/supported`

## Peptide Builder Validation Policy
`build_peptide(engine="MolSysMT")` must be validated against `engine="LEaP"`
using two tiers:

- **Default CI/local tier (fast):** focused regression cases (including PRO-heavy
  junctions) plus a small deterministic random set of length-10 sequences.
- **Extended parity tier (slow/manual/nightly):** 40 deterministic random
  length-10 sequences compared against LEaP with explicit topology and geometry
  tolerances.
