# Proposal: Technical and Scientific Quality Improvement Program

**Status:** accepted direction; Phase 1 implementation started 2026-07-13
**Owner:** MolSysMT
**Scope:** public API, form contracts, scientific validation, developer experience,
documentation, release engineering, and community-facing reference workflows
**Primary objective:** raise MolSysMT from a strong pre-stable scientific library to
a demonstrably reliable, independently validated, and easier-to-adopt platform
**Related work queue:**
`form_attributes_declared_without_getters.md`,
the archived `is_a_molecular_system_swallows_missing_getters.md` and
`merge_per_system_arguments_collapse.md` resolutions, and the archived
resolution records for single-attribute piping and form-delivery linting.

## 1. Executive Summary

MolSysMT already has a distinctive scientific purpose and a strong architecture. It
provides a uniform molecular-system API across native objects, molecular file formats,
trajectory libraries, simulation engines, viewers, and cheminformatics tools. Its main
technical strengths are the native `Topology`-`Structures`-`MolSys` model, the form
adapter ecosystem, the `get`/`set`/`convert`/`select` API, explicit physical-unit
handling, optional dependency isolation, structured diagnostics, and broad contract
testing.

The next quality increase does not require a broad architectural rewrite. The highest
return will come from making existing contracts mechanically enforceable, validating
scientific results against independent truth sources, improving static discoverability,
and converting representative scientific workflows into executable product evidence.

This proposal records a deferred improvement program organized into six workstreams:

1. public API and form contract integrity;
2. independent scientific validation;
3. static typing and developer experience;
4. declarative form conformance and maintenance automation;
5. reference scientific workflows and adoption assets;
6. operational robustness and release readiness.

The work should be executed incrementally. Contract integrity and scientific truth have
priority over new performance backends, large storage migrations, or broad feature
expansion because they improve confidence in every existing capability.

## 2. Why This Program Is Needed

### 2.1 The architecture is strong, but some declared contracts are not enforced

MolSysMT's core promise is that users can operate on many molecular forms through one
API. A form may currently declare an attribute without implementing a direct getter or
providing a valid pipe to a form that can deliver it. The conformance linter verifies
adapter structure but does not verify this end-to-end promise. In addition, the
single-attribute optimization in `get()` may bypass a required pipe and leak a raw
`AttributeError`.

These are localized implementation defects, but they affect the central product claim.
The correct response is to encode the promise as an executable contract so that the same
bug family cannot recur silently.

### 2.2 Internal parity is necessary but not sufficient scientific evidence

The test suite provides substantial cross-form parity. This protects interoperability,
but two implementations can agree because they share a convention, code path, or defect.
Stable scientific algorithms also need analytic cases, curated molecular references,
and independent external oracles. Without those, confidence in numerical and scientific
correctness remains lower than confidence in software consistency.

### 2.3 Runtime validation is stronger than static discoverability

ArgDigest gives MolSysMT a sophisticated runtime contract, but users and developers also
depend on IDE completion, Pyright or Mypy, signature inspection, and explicit return
types. Dynamic dispatch, decorator stacks, and return values controlled by keyword
arguments make the stable API difficult for static tools to understand. Improving the
small stable surface first will produce much more value than attempting to annotate the
entire adapter matrix.

### 2.4 The form matrix is becoming expensive to maintain manually

The number of supported forms is a major strength and an increasing maintenance cost.
Metadata, getters, pipes, conversion edges, tests, support tiers, and documentation can
drift because they are expressed in several places. A declarative conformance layer can
turn much of this drift into generated checks and reports.

### 2.5 Community success requires executable evidence

Technical breadth alone does not guarantee adoption. Users need a small number of
complete, reproducible workflows that show why MolSysMT is useful, how its results were
validated, what it costs in time and memory, and how it interoperates with established
tools. Those workflows can simultaneously serve the User Guide, Cookbook, course,
benchmarks, demonstrations, and a methods publication.

## 3. Baseline Assessment and Conditional Targets

The following scores are engineering estimates, not formal measurements. They record the
reason this program was created and provide direction for future evaluation.

| Category | Baseline | Conditional target |
|---|---:|---:|
| Overall technical quality | 8.4/10 | 9.0-9.2/10 |
| Scientific vision | 9.4/10 | Maintain at or above 9.4/10 |
| Architecture | 8.8/10 | 9.1/10 |
| Interoperability | 9.3/10 | 9.5/10 |
| Public API design | 8.5/10 | 9.0/10 |
| Scientific validation | 7.5/10 | 8.8-9.0/10 |
| Testing | 8.6/10 | 9.1/10 |
| Maintainability | 7.8/10 | 8.7/10 |
| Static typing and IDE support | 6.8/10 | 8.0-8.3/10 |
| Developer experience | 7.8/10 | 8.6/10 |
| Stable-release maturity | 7.9/10 | 8.8-9.0/10 |
| User documentation | 8.0/10 | 8.8/10 |

The original conditional success estimates were:

| Success dimension | Baseline estimate | Conditional target |
|---|---:|---:|
| Enabling laboratory projects | 93% | 97% |
| Novel and valuable community tool | 76% | 84-87% |
| Well-constructed scientific library on its own merits | 87% | 92-94% |

These percentages assume sustained maintenance, closure of the current contract defects,
independent validation of stable scientific functions, reproducible releases, and clear
communication. They must be revisited using evidence after the program is implemented.

## 4. Program Goals

### 4.1 Primary goals

- Make every Tier 1 capability claim executable and mechanically verified.
- Prevent internal adapter errors from leaking through stable public APIs.
- Establish independent scientific truth for stable numerical operations.
- Improve IDE and static-analysis support for the stable public surface.
- Reduce the marginal cost and risk of maintaining each form adapter.
- Demonstrate MolSysMT's value through reproducible end-to-end workflows.
- Harden file resources, JIT initialization, dependency compatibility, and release gates.
- Keep code, docstrings, User Guide, Cookbook, and the Four Paths course synchronized.

### 4.2 Non-goals

- Replacing the native topology engine as part of this program.
- Migrating the project to Rust, Arrow, DuckDB, Polars, or another storage backend.
- Adding new forms before the current Tier 1 contract is coherent.
- Typing every internal or form-specific function in one pass.
- Treating coverage percentage as a substitute for contract or scientific validation.
- Promoting all Tier 2 and Tier 3 forms to Tier 1.
- Guaranteeing community adoption through engineering metrics alone.

## 5. Guiding Principles

1. **Contract before expansion.** Existing Tier 1 promises must be reliable before
   increasing the supported surface.
2. **Independent truth before self-consistency.** Cross-form agreement must be backed by
   analytic or external reference results where possible.
3. **Public boundaries must be professional.** Raw adapter, NumPy, HDF5, or dependency
   exceptions must not leak where a MolSysMT diagnostic can provide context.
4. **Measure before optimizing.** Performance migrations require representative
   benchmarks and must preserve scientific and API semantics.
5. **Generate repeated evidence.** Form metadata should drive conformance checks, tests,
   documentation, and capability reports whenever practical.
6. **Lifecycle integrity is part of completion.** Public behavior changes are incomplete
   until docstrings, doctests, User Guide, Cookbook, and relevant course modules agree.
7. **Local evidence remains the native rebuild boundary.** This program must preserve the
   existing separation between native reconstruction and external enrichment.

## 6. Workstream A: Public API and Form Contract Integrity

**Priority:** P0
**Expected effort:** medium
**Expected impact:** very high

### 6.1 Why

The uniform public API is MolSysMT's primary value proposition. A declared attribute that
cannot be delivered, a pipe that is ignored, or an incomplete validation result that is
treated as success undermines that proposition. The known bug documents already provide
a focused starting inventory.

### 6.2 How

**Quick-win closure checkpoint (2026-07-13): complete.** A1's correctness floor is
implemented for single attributes, including preservation of cheap direct
getters and a MolSysMT exception when no route exists. A3 stages 1 through 3 are
implemented with a committed exact-set baseline and CI ratchet. The audited
delivery debt has fallen from 882 unreachable declarations across 70 forms to
489 across 29 forms after direct getters, shared derivations, verified pipes,
and a semantic review of the final Tier 1 gaps. Tier 1 now has zero unreachable
declarations; any new Tier 1 gap fails the ratchet. Mixed-element semantics are
also implemented and contract-tested. Exhaustive Tier 2 and Tier 3 remediation
and the later A3 stage remain pending, but they are explicitly outside the
quick-win block because they require broad adapter-by-adapter contract decisions
rather than a bounded mechanical change.
Workstream A5 is complete and contract-tested for both `merge()` and
`concatenate_structures()`.

**Post-quick-win delivery checkpoint (2026-07-15).** The curated scientific
validation work restored HDF5 structural getters and exercised additional
adapter routes. Direct CHARMM CRD atom-count delivery and subsequent adapter
repairs bring the audit to 430 unreachable declarations across 29 forms, 59
fewer than the 489-declaration quick-win checkpoint, with zero Tier 1
violations.

#### A1. Correct single-attribute piping in `get()`

- Preserve the direct-getter optimization when the relevant direct getter exists.
- If the getter does not exist, follow the appropriate topological, structural, or mixed
  pipe.
- Resolve pipe reachability transitively and protect against cycles.
- If neither a direct getter nor a pipe can deliver the attribute, raise a catalog-backed
  MolSysMT exception naming the form, attribute, requested element, and attempted pipe.
- Preserve the cost advantage of direct reads for inexpensive scalar attributes such as
  `n_atoms`.
- Add regression tests for single- and multi-attribute calls on every affected Tier 1
  form.

#### A2. Reconcile declared and deliverable attributes

**Implementation checkpoint (2026-07-13):** complete for Tier 1. Eighteen
remaining intentions were implemented from retained native data and nine
unsupported claims were removed after source-object inspection. Tier 2 and Tier
3 reconciliation remains pending.

For every Tier 1 form and every attribute declared `True`, choose explicitly among:

- implement a direct getter because the attribute is native and inexpensive;
- configure a valid pipe because conversion is the canonical delivery path;
- implement a derived getter where the attribute is computable from other data;
- stop declaring the attribute when the form cannot honestly support it.

Tier 2 should follow after Tier 1. Tier 3 may retain documented limitations, but its
declarations must still be honest.

#### A3. Extend adapter conformance validation

Add a transitive attribute-delivery check to
`devtools/scripts/validate_form_adapters.py`:

- read each declared attribute;
- inspect valid `get_from` elements in the central attribute catalog;
- search for a direct getter;
- otherwise follow the relevant pipes;
- identify pipe cycles, missing targets, incompatible elements, and unreachable
  attributes;
- emit a machine-readable report grouped by support tier and form.

Adopt it in stages:

1. report-only with a committed baseline;
2. hard failure for new regressions;
3. hard failure for all Tier 1 forms after remediation;
4. hard failure for Tier 2 after its declared contract is reconciled.

#### A4. Separate classification from validation

**Implementation checkpoint (2026-07-13):** complete and contract-tested. The
private assessment distinguishes single, multiple, and unsupported inputs, and
records validation as valid, invalid, or unverified. Public digestion raises
classification-specific catalog exceptions.

Refactor the responsibilities currently mixed in `is_a_molecular_system()`:

- classify whether multiple items represent complementary parts of one molecular system
  using form capabilities;
- validate consistency, including atom counts, only after classification;
- distinguish `valid`, `invalid`, and `could not verify` internally;
- ensure public boolean helpers never silently map failed verification to success;
- give ArgDigest enough structured information to report multiple systems separately
  from inconsistent components of one system;
- avoid remote downloads when static form capabilities are sufficient for
  classification.

#### A5. Preserve per-system intent in `merge()`

**Implementation checkpoint (2026-07-13):** complete and contract-tested for
`merge()` and the equivalent `concatenate_structures()` argument contract.

- Define an unambiguous internal representation for scalar, shared collection, and
  per-system values.
- Add caller-aware digesters for `selections` and `structure_indices` used by `merge()`.
- Preserve the outer per-system structure through argument digestion.
- Reject genuinely ambiguous input with an actionable MolSysMT exception.
- Update examples to show scalar, shared, and per-system forms explicitly.

#### A6. Audit stable public error boundaries

**Implementation checkpoint (2026-07-13): complete for the quick-win public
surface.** The `get()` boundary handles mixed atom/system attribute requests
through catalog-driven element partitioning. Both functions now reject negative and
out-of-range element or structure indices with `ArgumentError`, validate index and
Boolean masks, and translate selection-parser failures while preserving their causes.
The declared MDAnalysis syntax path was repaired to select on `MDAnalysis.Universe`
and return 0-based atom positions rather than topology IDs. Regression coverage includes
native MolSysMT, MDTraj, MDAnalysis, NumPy-backed native forms, and H5MSM input.
The same structure-index contract is enforced before dispatch by `convert()`,
`extract()`, `remove()`, `set()`, `view()`, `info()`, and `Iterator`. This prevents
raw indexing failures, silently ineffective removals, and empty iterators caused by
invalid frame requests.

Any remaining raw-exception audit concerns lower-frequency domain APIs, form-specific
adapter failures, or inconsistent multi-item edge cases. That work is not classified as
a quick win: it needs operation-specific semantics and must not wrap getter internals
indiscriminately because doing so could hide implementation defects.

- Exercise stable public functions with unsupported forms, unreachable attributes,
  malformed selections, inconsistent multi-item systems, and invalid indices.
- Replace raw user-facing `AttributeError`, `KeyError`, NumPy indexing errors, and HDF5
  errors with catalog-backed exceptions at the public boundary.
- Preserve the original exception as a cause and attach structured evidence through
  SMonitor.

### 6.3 Acceptance criteria

- Every Tier 1 declared attribute is reachable from at least one valid catalog element.
- Every Tier 1 attribute can be requested individually without an internal exception.
- The adapter validator fails on a newly introduced unreachable Tier 1 attribute.
- Piping cycles and invalid pipe targets are detected automatically.
- Inconsistent topology/structure item pairs fail with a specific diagnostic.
- `merge()` accepts and correctly applies documented per-system arguments.
- Stable public APIs do not leak raw missing-getter or third-party indexing errors in the
  covered scenarios.
- Relevant docstrings, doctests, User Guide, Cookbook, and course modules are updated.

### 6.4 Quick-win block closure

The quick-win block is closed at 100% on 2026-07-13. Its completed scope is:

1. direct topology gathering in place of the avoidable pandas merge path;
2. caller-aware `merge()` and `concatenate_structures()` digestion;
3. explicit molecular-system classification and validation outcomes;
4. correct single-attribute pipes, mixed-element `get()`, and derivable attributes;
5. an exact adapter-delivery baseline with a no-regression ratchet and zero Tier 1 gaps;
6. remediation of every audited Tier 1 declared attribute;
7. stable selection parsing, mask handling, and element/structure index boundaries across
   the basic public workflow surface.

The block is closed because each item offered high leverage through a bounded change,
reused existing architecture, and could be covered with deterministic repository tests.
The following work remains valuable but is deliberately excluded because its cost,
design surface, or scientific validation burden is materially larger:

- reconciling 232 Tier 2 and 257 Tier 3 delivery declarations;
- enabling an all-Tier-2 delivery gate;
- capability-level evidence for every form beyond the explicit tier registry;
- independent scientific truth suites and flagship workflows;
- comprehensive lower-frequency domain-API exception translation;
- Arrow, Rust, Polars, DuckDB, or other backend migrations.

Future work must not reopen this block merely because one of those larger workstreams is
pending. A newly discovered small regression may be fixed directly, but new architecture
or broad adapter reconciliation belongs to its own proposal and acceptance criteria.

## 7. Workstream B: Independent Scientific Validation

**Priority:** P1
**Expected effort:** medium to high
**Expected impact:** very high

### 7.1 Why

Interoperability tests demonstrate consistency across representations. Scientific
reliability additionally requires results whose expected values originate outside the
implementation under test. Stable operations should have a documented scientific
contract and at least one independent source of truth.

### 7.2 How

#### B1. Create a Scientific Truth Suite

**Implementation checkpoint (2026-07-15): in progress.** The executable suite
now covers analytic box geometry and MIC, external and curated molecular
geometry, centers and weighted centers, radius of gyration, RMSF, rigid fitting,
orthorhombic/triclinic temporal unwrapping, and covalent reconstruction during
PBC/MIC wrapping. It now also covers geometric and inertia principal axes,
mass-weight equivalence, principal-axis alignment, explicit proper rotations,
per-frame rotation broadcasting, and underdetermined least-RMSD fits. Rg and
RMSF have chunked execution with eager parity on the bundled pentaalanine
trajectory. Degenerate weighted, principal-axis, and rigid-fit inputs are
rejected at the public boundary. Periodic covalent reconstruction is also
validated on three frames of the curated solvated chicken villin trajectory,
where deliberate image shifts in distinct solvent molecules are recovered to
MDTraj's independently computed periodic bond distances. This closes the
planned structural slice; broader scientific coverage remains a continuing
program rather than an unbounded extension of this block.

Introduce a clearly identified test layer, for example under `tests/scientific_truth/`,
with three evidence classes.

**Analytic systems**

- exact Cartesian distances, angles, and dihedrals;
- known rotations and translations for alignment and RMSD;
- simple mass distributions for center of mass and radius of gyration;
- orthorhombic and triclinic boxes with exact lengths, angles, volumes, and MIC results;
- simple bonded graphs with known components, chains, and dihedral quartets.

**Curated molecular systems**

- a small peptide;
- a globular protein;
- a nucleic acid;
- a protein-ligand-ion-water system;
- a periodic solvated system;
- a small molecule with explicit bond orders and multiple conformers.

The systems must be bundled, versioned, small enough for deterministic CI, and described
with provenance.

**Independent external oracles**

- MDTraj or MDAnalysis for selected geometric analyses;
- OpenMM for topology, periodic boxes, energies, and forces where appropriate;
- RDKit for small-molecule connectivity, bond orders, and conformers;
- DSSP-compatible reference output for secondary structure;
- published or standard reference values when a well-defined source exists.

External-oracle tests must avoid circular validation. A converter and its oracle must not
derive their expected value from the same MolSysMT code path.

**Implementation checkpoint (2026-07-13).** The suite infrastructure and the first
analytic PBC slice are implemented under `tests/scientific_truth/`. The initial cases
cover exact orthorhombic and triclinic box geometry, construction, volume, and minimum
image distances. This slice exposed intermediate six-decimal box rounding in
`get_volume_from_lengths_and_angles`; the function now evaluates the closed-form volume
directly while preserving units and vectorization. The evidence hierarchy, tolerance
policy, box convention, and validation index are recorded in
`devguide/scientific_validation.md`.

The first external slice is also implemented against both MDTraj and MDAnalysis. Ten
tests compare distances, angles, signed dihedrals, raw or least RMSD as supported by
each oracle, and triclinic minimum-image distances. Both external tools and MolSysMT
consume the same independently declared NumPy fixtures; no MolSysMT converter constructs
the oracle input. The initial provenance and tolerance rationale are recorded in
`devguide/scientific_validation.md`.

The first curated molecular layer is implemented with pentaalanine,
Met-enkephalin, the 38-model Trp-cage NMR ensemble, and the periodic `md_1u19`
demo trajectory. It validates real peptide geometry, trajectory phi/psi angles,
least-RMSD, coordinates, boxes, time, and multiframe MIC distances. Artifact
identity is protected by SHA-256 provenance records. This work also restored
declared structural delivery for `file:h5` and corrected XTC box parsing, which
had mistaken step indices for cell lengths.

OpenMM, RDKit, and DSSP-compatible references remain subsequent domain-specific
layers. These comparisons are benchmarks of scientific agreement; runtime
performance benchmarks must remain separately labeled.

#### B2. Define a scientific contract template

For every stable scientific function, record:

- mathematical quantity and convention;
- accepted input shapes;
- output shape;
- physical units;
- default weighting or masses;
- periodic-boundary behavior;
- missing-data behavior;
- dtype and precision expectations;
- absolute and relative tolerances;
- degenerate and empty-input behavior;
- independent reference used for validation.

The template should be reflected in docstrings and a developer-facing validation index.

#### B3. Add property and metamorphic tests

Candidate properties include:

- distance symmetry and non-negativity;
- invariance of internal distances under rigid translation and rotation;
- RMSD identity and known transformation behavior;
- idempotence or defined repeat behavior for PBC wrapping;
- inverse relationships between box and length/angle conversions;
- graph component consistency after bond addition or removal;
- preservation of topology under documented lossless round trips;
- stable string IDs after conversion, extraction, merging, and rebuilding;
- eager/chunked parity for operations in the heavy execution contract.

Use deterministic generators and bounded sizes. Property testing must complement, not
replace, explicit reference examples.

#### B4. Establish tolerance governance

- Centralize tolerance policy by scientific operation and dtype.
- Avoid arbitrary loosening of tolerances to make tests pass.
- Document whether tolerance reflects floating-point propagation, an external tool's
  convention, or an intentionally approximate algorithm.
- Require review when a tolerance increases.

### 7.3 Initial validation order

1. PBC construction, lengths, angles, volume, wrapping, and MIC.
2. Distances, centers, RMSD, alignment, angles, and dihedrals.
3. Native topology hierarchy, components, molecules, entities, and bonds.
4. Tier 1 lossless and intentionally lossy conversion contracts.
5. Mass, charge, radii, SASA, and other physicochemical calculations.
6. Structure preparation, energies, forces, and secondary structure.

### 7.4 Acceptance criteria

- Every stable PBC and structural-analysis function has an analytic or independent oracle.
- Every stable scientific function documents units, conventions, and tolerances.
- External-oracle provenance is recorded and reproducible offline where licensing allows.
- Eager/chunked parity is verified for every operation that claims both modes.
- Scientific regressions fail independently of form-parity tests.
- Validation results are summarized in user and developer documentation.

## 8. Workstream C: Static Typing and Developer Experience

**Priority:** P2
**Expected effort:** medium
**Expected impact:** high

### 8.1 Why

MolSysMT provides strong runtime argument handling but limited static assistance. The
stable API should be discoverable in editors and analyzable without requiring a full
understanding of dynamic dispatch.

### 8.2 How

#### C1. Define the first typed surface

Prioritize root-level and stable native APIs:

- `get`, `set`, `convert`, `select`, `extract`, `copy`, `merge`, and `compare`;
- `get_form`, `has_attribute`, `info`, `view`, and `Iterator`;
- `MolSys`, `Topology`, `Structures`, and `MolSysBuilder`;
- stable PBC and structural functions.

#### C2. Define reusable typing vocabulary

Candidate types and protocols include:

- `MolecularSystemLike`;
- `FormName` and support-tier-aware `Literal` subsets where practical;
- `SelectionLike`;
- `StructureIndicesLike` and `AtomIndicesLike`;
- `QuantityLike`;
- coordinate, box, and time array aliases;
- protocols for closeable resource forms and iterators.

Types must describe supported behavior without importing soft dependencies at module
load time.

#### C3. Handle dynamic returns deliberately

- Use overloads for common `get()` and `convert()` cases only when they remain
  maintainable.
- Document cases whose return type depends on runtime form metadata.
- Consider focused `.pyi` files when source annotations cannot express the public
  contract cleanly.
- Avoid a combinatorial overload matrix that becomes another manual registry.

#### C4. Verify decorator transparency

Add tests ensuring that stacked `@signal` and `@arg_digest` decorators preserve:

- `inspect.signature()`;
- `__doc__`;
- `__annotations__`;
- `__wrapped__`;
- Sphinx-visible parameter documentation.

#### C5. Add a bounded static-analysis gate

- Select Pyright or Mypy after a short comparison against the dynamic API.
- Start with the explicitly typed stable surface.
- Commit a configuration and prohibit new errors within that surface.
- Expand the boundary incrementally after the initial target is clean.

### 8.3 Acceptance criteria

- The selected stable functions expose useful editor signatures and return hints.
- Decorated public signatures match their undecorated contracts.
- Static analysis passes for the declared typed surface.
- Soft dependencies remain lazily imported.
- Sphinx displays the intended signatures and docstrings.
- Typing policy and limitations are documented for contributors.

## 9. Workstream D: Declarative Form Conformance and Maintenance Automation

**Priority:** P3
**Expected effort:** medium
**Expected impact:** high

### 9.1 Why

Form capabilities are currently distributed across module variables, attribute maps,
getter modules, conversion dictionaries, support tiers, tests, and documentation. This
allows declarations and delivery to drift. A declarative contract can act as the source
for repeated validation without replacing lazy runtime discovery.

### 9.2 How

#### D1. Design a form contract schema

The schema should be additive and should include:

- canonical form name and type;
- backing dependency and installation key;
- support tier;
- native, derived, and intentionally unsupported attributes;
- direct getters and supported elements;
- topological, structural, and mixed pipes;
- direct conversion edges;
- lossy and lossless conversion notes;
- selection syntax support;
- eager and chunked capabilities;
- resource ownership and close behavior;
- bond availability and computation policy;
- optional conversion arguments.

The initial implementation may construct this schema from existing modules. A later
decision can determine whether adapters declare it directly.

#### D2. Generate conformance evidence

Use the schema to produce:

- attribute reachability reports;
- conversion graph validation;
- invalid or cyclic pipe reports;
- support-tier capability tables;
- parameterized contract tests;
- documentation tables;
- resource-lifecycle checks;
- stale declaration detection.

#### D3. Ratchet rather than freeze current debt

- Capture the initial report as a baseline.
- Fail on newly introduced regressions immediately.
- Remove baseline exceptions as forms are repaired.
- Keep Tier 1 at zero exceptions once it becomes clean.

### 9.3 Acceptance criteria

- A single machine-readable report describes every discovered form.
- Tier, dependency, attributes, pipes, and conversion edges are cross-validated.
- Contract tests can be parameterized from form metadata without importing every soft
  dependency at startup.
- User-facing supported-form documentation is generated or checked against the same
  evidence.
- Adding a form with declared but unreachable attributes cannot pass conformance CI.

## 10. Workstream E: Reference Scientific Workflows and Adoption Assets

**Priority:** P4
**Expected effort:** medium
**Expected impact:** high for laboratory and community outcomes

### 10.1 Why

MolSysMT's breadth is easier to understand through complete outcomes than through an API
inventory. A small set of polished workflows can show scientific utility, exercise
multiple subsystems, reveal integration regressions, and provide material for teaching
and publication.

### 10.2 Proposed flagship workflows

#### E1. Structure to simulation

PDB or BinaryCIF input to diagnosis, repair, protonation, solvation, conversion to
OpenMM, and a minimal reproducible simulation or energy evaluation.

#### E2. Large-trajectory analysis

Chunked trajectory iteration, molecular selection, PBC-aware analysis, aggregation, and
comparison with eager execution on a bounded reference subset.

#### E3. Protein-ligand interaction analysis

Topology validation, ligand selection, contacts, hydrogen bonds, SASA or buried area,
and a machine-readable interaction summary.

#### E4. Cross-library fidelity

MolSysMT to MDTraj to MDAnalysis to OpenMM and back where meaningful, with explicit
checks of topology, coordinates, box, units, bonds, and known lossy fields.

#### E5. Native construction and declarative persistence

Create or edit a system with `MolSysBuilder`, validate native hierarchy, serialize to a
declarative form, reload it, and compare the result.

### 10.3 Required content for each workflow

- a small bundled or reproducibly generated input;
- an executable test or validation script;
- a concise User Guide or Cookbook narrative;
- relevant Four Paths course coverage;
- expected scientific output and interpretation;
- explicit unit and topology assumptions;
- runtime and peak-memory measurements;
- comparison with the equivalent workflow using underlying libraries directly;
- common failure modes and their MolSysMT diagnostics;
- offline CI coverage for the stable core of the workflow.

### 10.4 Acceptance criteria

- All five workflows run from a clean supported environment.
- Stable portions execute offline and are covered by tests.
- Documentation output agrees with executable output.
- Time and memory measurements are reproducible within documented bounds.
- Each workflow states where MolSysMT adds value and where it delegates to another tool.

## 11. Workstream F: Operational Robustness and Release Readiness

**Priority:** P5
**Expected effort:** medium
**Expected impact:** medium to high

### 11.1 Why

Scientific correctness is insufficient if long-running workflows leak resources,
parallel initialization is unsafe, dependencies drift silently, or generated
documentation hides decorated signatures. Stable releases need explicit operational
contracts.

### 11.2 How

#### F1. Resource lifecycle

- Inventory adapters and iterators that open HDF5, XTC, DCD, TNG, or other resources.
- Define ownership: who opens, who closes, and when ownership is transferred.
- Prefer context managers or `try/finally` at ownership boundaries.
- Add repeated-open tests that monitor file descriptor growth where supported.
- Make `form.close()` diagnostics visible instead of silently swallowing unexpected
  closure failures.

#### F2. JIT and parallel startup

- Audit mutable global state in lazy compilation and warmup paths.
- Decide whether to protect compilation state with locks or require main-thread warmup.
- Test the supported policy with multiple threads and processes.
- Use `warmup(strict=True, return_report=True)` when QA requires an auditable
  precompilation result.
- Evaluate the Rust AOT proposal before expanding long-term reliance on Numba
  warmup.

#### F3. Dependency compatibility

- Define a compatibility matrix for Python, NumPy, Numba, PyUnitWizard, ArgDigest,
  DepDigest, SMonitor, OpenMM, MDTraj, MDAnalysis, and other Tier 1 dependencies.
- Test both minimum-supported and current-supported dependency sets where practical.
- Record known incompatibilities rather than relying on accidental environment pinning.
- Keep soft dependencies behind `@dep_digest` and lazy imports.

#### F4. Platform policy

- Maintain Linux and macOS validation for the stable contract.
- Make an explicit supported/not-supported decision for Windows and ARM.
- Add platform-specific tests only where the support contract requires them.

#### F5. Release gates

Before a stable release, require:

- Tier 1 conformance;
- Scientific Truth Suite pass;
- stable-surface static analysis;
- Ruff correctness checks;
- doctests and documentation build;
- representative flagship workflow smoke tests;
- dependency audit;
- package build and clean-environment import test.

### 11.3 Acceptance criteria

- Repeated resource workflows do not show unbounded descriptor growth.
- JIT behavior has a tested and documented parallel-use policy.
- The compatibility matrix is published and exercised in CI at defined intervals.
- Platform support is explicit.
- A release candidate can be evaluated from one documented checklist.

## 12. Documentation Lifecycle Requirements

Every public behavior change in this program must satisfy the repository's Lifecycle
Integrity rule.

### 12.1 Required surfaces

- NumPy-style docstrings with deterministic doctests;
- API reference;
- User Guide Foundations where the concept or contract changes;
- User Guide Toolbox for affected functions;
- Cookbook for end-to-end usage;
- relevant modules of the Four Paths of the MolSysMT's Master course;
- developer documentation and conformance reports;
- release notes and deprecation notices when applicable.

### 12.2 Documentation verification

- Execute all new examples.
- Use bundled data and avoid network dependencies.
- Cross-link concepts, toolbox entries, and workflows with the established MyST pattern.
- Treat generated capability tables as checked artifacts, not manually copied claims.
- Verify that examples expose the same units, shapes, forms, and errors as the code.

## 13. Proposed Delivery Sequence

### Phase 0: Baseline and issue decomposition

- Freeze current Tier 1 capability and attribute-delivery reports.
- Create one implementation issue per independently reviewable defect.
- Record current test, import, workflow, and documentation baselines.
- Decide the initial static-analysis tool and Scientific Truth Suite layout.

### Phase 1: Tier 1 contract reliability

- Fix single-attribute piping.
- Reconcile Tier 1 attribute declarations.
- Extend the form validator and enable the no-regression ratchet.
- ~~Separate multi-item classification from validation.~~ Completed 2026-07-13.
- ~~Fix per-system argument digestion in `merge()`.~~ Completed 2026-07-13.
- Audit covered public error boundaries.

**Exit gate:** Tier 1 declared capabilities are mechanically deliverable and covered by
regression tests.

### Phase 2: Scientific confidence

- Add analytic PBC and geometry truth cases.
- Add curated reference molecular systems.
- Add independent topology and conversion oracles.
- Define tolerance governance.
- Extend eager/chunked execution parity.

**Exit gate:** stable core scientific operations have independent, documented evidence.

### Phase 3: Developer experience and adoption

- Type the stable public surface.
- Verify decorator transparency and Sphinx signatures.
- Implement the five flagship workflows.
- Add compatibility and performance summaries.

**Exit gate:** new users and developers can discover, run, and validate the principal
workflows from a clean environment.

### Phase 4: Maintenance automation and Tier 2 ratchet

- Formalize the declarative form contract.
- Generate conformance evidence and parameterized tests.
- Reconcile Tier 2 declarations.
- Enable additional CI gates after the baseline is clean.

**Exit gate:** form growth no longer depends primarily on manual cross-checking.

### Phase 5: Stable-release audit

- Execute the full release checklist.
- Recalculate the technical scorecard from collected evidence.
- Reassess support tiers and public stability classifications.
- Publish remaining limitations explicitly.

## 14. Suggested Issue Decomposition

The future implementation should use small, independently reviewable issues or pull
requests. Suggested initial units are:

1. single-attribute pipe fallback and regression tests;
2. Tier 1 attribute reachability report;
3. Tier 1 declaration remediation by form family;
4. form linter reachability mode and baseline;
5. multi-item system classification model;
6. multi-item atom-count validation and diagnostics;
7. `merge()` caller-aware per-system digestion (completed 2026-07-13);
8. stable public raw-exception inventory (high-frequency `select()`/`get()` batch
   completed 2026-07-13; lower-frequency APIs remain);
9. Scientific Truth Suite infrastructure;
10. analytic PBC oracle set;
11. analytic geometry and alignment oracle set;
12. native topology truth fixtures;
13. tolerance policy;
14. stable API typing vocabulary;
15. typing of root-level basic functions;
16. decorator signature preservation tests;
17. form contract schema prototype;
18. flagship workflow implementation, one issue per workflow;
19. resource ownership audit;
20. compatibility matrix and release checklist.

Each issue should state affected support tiers, scientific conventions, required tests,
documentation surfaces, and rollback implications.

## 15. Metrics and Evidence

Progress should be measured using evidence rather than the subjective scores alone.

### 15.1 Contract metrics

- Tier 1 declared attributes unreachable: target `0`.
- Tier 1 invalid pipe targets or cycles: target `0`.
- Stable public raw internal exceptions in contract tests: target `0`.
- Documented `merge()` argument modes covered: target `100%`.

### 15.2 Scientific metrics

- Stable scientific functions with independent or analytic oracle: target `100%` for the
  declared stable surface.
- Stable functions with documented units and tolerance: target `100%`.
- Heavy-contract operations with eager/chunked parity: target `100%`.

### 15.3 Developer-experience metrics

- Stable typed surface passing the selected checker: target `100%`.
- Decorated stable functions preserving inspectable signatures: target `100%`.
- Documentation build and doctest pass rate: target `100%`.

### 15.4 Operational metrics

- Representative repeated file workflows with unbounded descriptor growth: target `0`.
- Declared compatibility jobs passing: target `100%`.
- Flagship workflows executable offline at their stable core: target `5/5`.

### 15.5 Adoption evidence

Community success should later be evaluated using observable indicators such as:

- successful installation rate in supported environments;
- completion rate of flagship workflows;
- external issues and pull requests resolved;
- independent projects using MolSysMT;
- citations, tutorials, or downstream integrations;
- time-to-first-success for a new user;
- time saved in laboratory projects compared with direct multi-library glue code.

## 16. Risks and Mitigations

| Risk | Consequence | Mitigation |
|---|---|---|
| Program scope becomes too broad | Long-lived branch and delayed value | Deliver by workstream and small pull requests, beginning with Tier 1 contracts |
| Generated form contracts duplicate existing metadata | New source of drift | Derive the first schema from current modules and establish one authority before migration |
| External oracle tests are fragile | CI instability | Pin reference outputs, keep tests offline, and separate compatibility jobs from core truth tests |
| Typing becomes combinatorial | High maintenance burden | Type the stable surface first and use conservative protocols and overloads |
| Tolerances are loosened to hide failures | False scientific confidence | Centralize tolerance governance and require justification for increases |
| Performance work changes scientific semantics | Silent result drift | Require Scientific Truth Suite and eager/chunked parity before and after optimization |
| Documentation lifecycle becomes a bottleneck | Incomplete public changes | Assign documentation surfaces in each issue and reuse executable workflow assets |
| Tier 2 cleanup consumes Tier 1 effort | Delayed contract reliability | Complete the Tier 1 exit gate before broad Tier 2 remediation |
| Success percentages are treated as guarantees | Misleading planning | Recalculate estimates from evidence and report uncertainty explicitly |

## 17. Dependencies and Ordering Constraints

- Single-attribute piping should be corrected before treating pipes as a general remedy
  for missing direct getters.
- Tier 1 attribute declarations should be reconciled before the linter becomes a hard
  zero-exception gate.
- Scientific Truth Suite coverage should precede major kernel, Rust, Arrow, or topology
  storage migrations.
- Decorator transparency should be verified before relying on public annotations or
  generated API documentation.
- Reference workflows should use the stabilized Tier 1 contract.
- Tier 2 ratcheting should begin after Tier 1 is clean.
- Release score reassessment should happen only after all collected evidence is current.

## 18. Definition of Program Completion

This proposal is complete only when:

- all Phase 1 Tier 1 contract exit criteria pass;
- stable scientific operations have independent truth evidence;
- the declared stable API surface passes static analysis and signature inspection;
- form conformance evidence is generated or mechanically cross-checked;
- all five flagship workflows are executable and documented;
- resource, JIT, compatibility, platform, and release policies are explicit and tested;
- all required documentation and course surfaces are synchronized;
- the scorecard and success estimates are recalculated from the resulting evidence;
- remaining limitations are documented rather than implied to be solved.

## 19. Deferred Decision Record

Several Phase 1 decisions and quick wins have already been implemented, as recorded in
their checkpoints above. Before the remaining workstreams start, the maintainers must
still decide:

- the evolution policy for the implemented private multi-item assessment model;
- whether form contracts remain distributed and inspected or move to an explicit schema;
- the static-analysis tool and supported strictness level;
- the initial independent oracle set and dependency policy for oracle generation;
- which platforms belong to the stable support contract;
- whether resource closure failures should warn or raise in each ownership context;
- the release milestone to which each phase belongs.

Until those decisions are made, this document serves as the complete rationale,
implementation outline, sequencing guide, and acceptance framework for future work.
