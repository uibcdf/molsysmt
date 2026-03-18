# Testing Strategy

## Framework
Use `pytest`. Tests live under `tests/` and should mirror package structure.

## 🥇 Contract Testing (The 1.0.0 Standard)
Contract tests are the primary defense against regressions in interoperability.

The support contract is defined in `devguide/support_tiers.ipynb`. Testing must derive from that document rather than from informal expectations.

Two parity axes must remain explicit:

- **Form parity**: equivalent molecular content represented in different supported forms must produce equivalent observable results where such equivalence is part of the declared support scope.
- **Execution parity**: eager and heavy execution paths must produce equivalent results for operations that officially support both.

For Tier 1 forms, the default contract-testing expectation is:
- `msm.get`, `msm.info`, `msm.select`, and `msm.convert` must preserve the documented supported scope of the form;
- coordinates and box vectors must match within $10^{-5}$ nanometers where structural parity is part of the contract;
- selection strings must resolve to the same atom indices across Tier 1 forms when selection parity is part of the documented scope;
- lossy formats (for example PDB or viewer-oriented forms) must be tested against their documented limits, not against impossible full-fidelity expectations.

Tier 2 and Tier 3 forms may still have valuable tests, but their parity obligations must be weaker and explicitly tied to their documented scope.

## Contract-driven test prioritization

The support contract is not only a list of forms. It also includes the `Contractual capability matrix` in `devguide/support_tiers.ipynb`. Test priorities must therefore follow both axes:

- the tier of the form;
- the contractual capability being claimed for that tier.

When choosing what to test next, prioritize in this order:

1. Tier 1 contract tests for the capabilities marked as `Full` in the capability matrix;
2. Tier 1 form parity tests inside the documented supported scope of those capabilities;
3. execution parity tests for any operation entering the heavy-processing contract;
4. Tier 2 best-effort regressions for capabilities marked as partial or lossy;
5. Tier 3 or legacy coverage only when it reveals real risk or blocks cleanup.

Coverage percentage alone must not drive test priorities. The first objective is to harden the contractual support surface defined in `devguide/support_tiers.ipynb`.

## Capability-driven parity obligations

The capability matrix in `devguide/support_tiers.ipynb` should be read as the source of truth for parity obligations. In practice, each capability implies a characteristic family of tests:

- **Basic introspection**
  - contract tests for `msm.get`, `msm.info`, and `msm.compare`;
  - scope-preserving checks on topology and structures for Tier 1 forms.

- **Selection semantics**
  - `msm.select` agreement tests across Tier 1 forms wherever selection parity is part of the supported scope;
  - explicit lossy or partial expectations for Tier 2 forms.

- **Structural analysis**
  - numerical parity tests for distances, centers, RMSD, and related Tier 1 analyses;
  - eager-only parity for forms not yet in the heavy contract.

- **Topology editing**
  - builder-driven tests for `MolSysBuilder` and `msm.build.editable(...)`;
  - no obligation to preserve legacy editing helpers that are already removed from the public API.

- **Coordinate updates**
  - `msm.set` and builder setter tests on the forms whose contractual scope includes structural updates.

- **Format conversion**
  - round-trip or truth-preserving tests inside the documented lossy/lossless scope of each form;
  - deterministic builder-based fixtures should be preferred whenever a converter needs an external-format oracle.

- **Visual interaction**
  - smoke and regression tests only for the viewer-facing scope that is explicitly claimed in the support contract;
  - no hidden assumption of full topology parity for visualization-only forms.

- **Heavy / chunked execution**
  - eager vs heavy parity tests;
  - `MSM-*-HVY-*` telemetry contract tests;
  - failure-policy tests for unsupported combinations and recoverable frame-skipping behavior.

This separation matters because `contract verification`, `form parity`, and `execution parity` are related but not identical obligations.

## pytest marks and useful -m combinations

### Registered marks

| Mark | Applied by | Meaning |
|------|-----------|---------|
| `tier1` | `conftest.py` (automatic) | Form is Tier 1 — contractual, 1.x stable |
| `tier2` | `conftest.py` (automatic) | Form is Tier 2 — best-effort |
| `tier3` | `conftest.py` (automatic) | Form is Tier 3 — experimental / niche |
| `network` | test author (manual) | Requires a live network connection |
| `redundant` | test author (manual) | Exercises a delegation path already covered by a lower-level suite |

Tier marks are applied automatically by `tests/conftest.py` to all tests under
`tests/form/<form_dir>/`.  The source of truth is `FORM_TIERS` in
`molsysmt/_private/form_tier.py` — updating a form's tier there propagates to
tests automatically.  Tests outside `tests/form/` (e.g. `tests/basic/`,
`tests/build/`) receive no tier mark.

`redundant` is applied manually with `pytestmark = pytest.mark.redundant` at the
module level (or `@pytest.mark.redundant` on individual functions).  Use it when a
test exercises a pure delegation path that is already comprehensively covered by the
delegatee's own suite.

### Useful -m combinations

```bash
# Development — fast, contractual surface, no network
pytest -m "tier1 and not network and not redundant"

# Full Tier 1 — contractual surface with network smoke tests
pytest -m "tier1"

# Tier 1 + Tier 2, no network
pytest -m "(tier1 or tier2) and not network"

# Only network smoke tests
pytest -m "network"

# Everything except redundant delegation tests
pytest -m "not redundant"

# Full suite (default, no -m flag needed)
pytest
```

## Collaborative testing workflow

The standard working pattern for raising test coverage is:

1. **User runs the suite and identifies low-coverage areas** — using
   `pytest --cov=molsysmt --cov-report=term -q tests` or targeted coverage sweeps;
   the user decides which uncovered module or capability is the next priority.

2. **User opens a conversation describing the target** — e.g., "write tests for
   `get_topological_attributes` in `mdtraj.Topology`"; the user supplies any known
   constraints (which attributes are supported, known bugs, reference system to use).

3. **Claude reads the implementation before writing tests** — always read the form
   adapter, the `attributes.py`, and any relevant element API code before proposing
   tests; never write tests against a function without first verifying its signature,
   return type, and documented behaviour.

4. **Tests are written to reveal bugs, not just to pass** — when a test fails, the
   failure is investigated: if it is a test bug, fix the test; if it is an
   implementation bug, fix the implementation first, then confirm the test passes.
   Do not suppress failures by weakening assertions.

5. **Implementation bugs discovered during testing are fixed immediately** — do not
   commit broken implementations and mark tests as `xfail`. Fix the bug, then confirm
   the tests are green.

6. **Coverage is checked after each new test file** — after adding a test file,
   compare the new coverage percentage against the prior baseline. Coverage should
   only move upward across commits that add test files.

7. **Guidance from each test implementation session is captured in devguide** — new
   patterns, discovered conventions, and corrected misconceptions should be added to
   `devguide/testing_form_adapters.md` or this file, not left as ephemeral chat
   context.

See `devguide/testing_form_adapters.md` for the concrete implementation patterns (builder
fixture, parametrize structure, None handling, convert-then-delegate, etc.).

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

## Heavy-mode parity policy

The heavy-trajectory roadmap is defined in `devguide/scalability_and_heavy_trajectories_v2.md`.

When an operation enters the committed heavy slice, it must gain:
- eager vs heavy parity tests;
- telemetry contract tests for the reserved `MSM-*-HVY-*` codes;
- failure-policy tests for unsupported combinations and recoverable frame-skipping behavior where applicable.

Heavy-mode support is not inferred from ordinary form support. Tests must reflect the heavy-status declarations in `devguide/support_tiers.ipynb`.

## Peptide Builder Validation Policy
`build_peptide(engine="MolSysMT")` must be validated against `engine="LEaP"`
using two tiers:

- **Default CI/local tier (fast):** focused regression cases (including PRO-heavy
  junctions) plus a small deterministic random set of length-10 sequences.
- **Extended parity tier (slow/manual/nightly):** 40 deterministic random
  length-10 sequences compared against LEaP with explicit topology and geometry
  tolerances.

## Coverage scope for 1.0 stabilization

- `molsysmt/molecular_dynamics/**` is intentionally omitted from the local and
  Codecov coverage baselines during the `1.0.0` stabilization pass.
- This is a support-contract decision, not an accident: the module remains in
  the repository, but it is outside the supported `1.0.0` line.
- Coverage targets for the 1.0 stabilization work therefore apply to the rest of
  the repository, not to `molecular_dynamics`.

### Piped getter files are excluded from coverage

All `get_topological_attributes.py` files belonging to forms that set
`piped_topological_attribute` are excluded from the coverage baseline
(via `.coveragerc`).  The pipe target may be `molsysmt.Topology` or another
intermediate form such as `openmm.Topology` — the exclusion rationale is the
same in both cases.

**Rationale:** these files are generated delegation code — every getter function
does exactly this:

```python
tmp_item = to_<piped_form>(item, skip_digestion=True)
output = <piped_form_module>.get_X(tmp_item, indices=indices, skip_digestion=True)
return output
```

Covering them individually would require calling all ~463 getters per form,
producing thousands of redundant tests with zero additional defect-detection
power.  The real implementation under test is always the piped-to form.  Once
the conversion path `form → piped form` is verified (which IS tested), the
getter delegation is correct by construction.

The excluded forms as of March 2026 are (24 total):

*Piped to `molsysmt.Topology` (21 forms):*
`string:pdb_id`, `string:alphafold_id`, `string:pdb_text`, `string:smiles`,
`file:pdb`, `file:bcif`, `file:bcif_gz`, `file:cif`, `file:cif_gz`,
`file:prmtop`, `file:psf`, `file:smi`, `file:topology_yaml`,
`MDAnalysis.AtomGroup`, `mmcif.PdbxContainers.DataContainer`,
`mmtf.MMTFDecoder`, `molsysmt.GROFileHandler`, `molsysmt.TopologyDict`,
`nglview.NGLWidget`, `openff.Molecule`, `openff.Topology`.

*Piped to `openmm.Topology` (3 forms):*
`pdbfixer.PDBFixer`, `openmm.Simulation`, `openmm.Modeller`.

When a new piped form is added, its `get_topological_attributes.py` must also
be added to the `omit` list in `.coveragerc`.
