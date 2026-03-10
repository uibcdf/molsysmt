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

Default execution mode for broad validation is now distributed:
- use `pytest -n 12 --dist loadfile ...` for large validation batches and full
  suite confirmation when the environment supports `pytest-xdist`;
- keep the sequential directory-by-directory order, but run each batch in
  distributed mode to reduce wall-clock time without saturating the whole
  workstation;
- reserve fully sequential execution for debugging a specific failure, for
  narrow reproduction, or if coverage instrumentation becomes unstable under
  `xdist`.

Coverage-specific rule:
- the reliable coverage baseline is the full-package sweep, for example
  `pytest -n 12 --dist loadfile --cov=molsysmt --cov-report=term -q tests`;
- targeted coverage sweeps using multiple `--cov=...` module or file selectors
  are currently unreliable in this environment and may fail with either
  `No data was collected` or `ImportError: cannot load module more than once
  per process`;
- when targeted coverage is needed, prefer a normal distributed test batch plus
  a full-package coverage sweep, then inspect the module-level report from that
  full run instead of trying to instrument only a subset.

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
- `tests/supported`
- full-suite confirmation with `pytest -q tests -x`

Current status:
- the full `tests/` tree passes in the current environment;
- the sequential rule remains recommended for stabilization work because it
  produces better checkpoints and faster diagnosis when the suite is not yet
  green;
- broad validation and coverage sweeps should prefer `-n 12` in the reference
  workstation, which has enough physical cores to support that level of
  parallelism without interfering with other active tasks;
- targeted coverage instrumentation remains a known tooling limitation and
  should not be used as the default workflow until the `numpy`/coverage import
  issue is understood and resolved.

## Peptide Builder Validation Policy
`build_peptide(engine="MolSysMT")` must be validated against `engine="LEaP"`
using two tiers:

- **Default CI/local tier (fast):** focused regression cases (including PRO-heavy
  junctions) plus a small deterministic random set of length-10 sequences.
- **Extended parity tier (slow/manual/nightly):** 40 deterministic random
  length-10 sequences compared against LEaP with explicit topology and geometry
  tolerances.
