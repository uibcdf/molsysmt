# MolSysMT 1.0 Execution Plan

**Role:** pending operational plan
**Decision date:** 2026-07-26
**Target:** a clean, Rust-only MolSysMT 1.0 release on Python 3.11–3.13
**Status:** accepted direction; implementation and release gates remain open

## Purpose

This document is the ordering guide for the remaining work toward 1.0. It does
not replace the detailed bug reports, proposals, or the normative
[`release_gate.md`](../release_gate.md). It links them into one executable
sequence and defines when work may advance to the next segment.

The plan deliberately separates:

- work that blocks an honest 1.0 release;
- expensive work that can continue after 1.0;
- independent investigations that must not destabilize the release candidate.

## Maintainer Decisions

### 1. MolSysMT 1.0 Will Not Maintain Two CPU Kernel Implementations

The long-term runtime is Rust. Numba is a temporary migration oracle, not a
second supported backend.

The previous plan proposed shipping 1.0 with `kernel="auto"` and removing Numba
later. That decision is superseded. The 1.0 target is now:

- the Rust extension is installed with MolSysMT and is the only CPU kernel
  implementation;
- Numba is not a hard, soft, test, documentation, or build dependency;
- the runtime has no `numba` fallback;
- `configure.kernel`, the `kernel=` override, and backend-selection code are
  removed unless they are redesigned as a genuinely backend-independent future
  device contract;
- JIT warmup, cache management, and Numba diagnostics are removed;
- the scientific and property tests, rather than a second implementation,
  become the permanent correctness authority.

There is no deprecation window because MolSysMT has not released a stable 1.x
contract and has no external user base requiring a compatibility transition.
The migration must nevertheless preserve scientific behavior and update every
declared public contract before the 1.0 tag.

### 2. Packaging Is a Precondition for Deletion

Numba must not be deleted first and replaced with an unproven packaging
assumption. Rust-only installation must work before the fallback disappears.

The preferred distribution is one MolSysMT wheel containing a private extension
such as `molsysmt._rust`, rather than a separately versioned public
`msm_rust_kernels` package. A single wheel avoids version skew and presents one
installable product. This preference must be confirmed by an implementation
spike because the repository currently uses setuptools while the pilot crate
uses maturin.

If an embedded extension proves unsuitable, a required, exactly compatible
kernel wheel is the fallback packaging design. It is not acceptable to publish
MolSysMT successfully while leaving users to discover at runtime that its
required kernels are absent.

### 3. Removing Numba Includes the CUDA Surface

Removing the CPU fallback while retaining eleven Numba-CUDA modules would not
remove Numba as a maintenance front.

The generic concepts `use_gpu`, `gpu_mode`, and a future device backend are not
intrinsically tied to Numba and may remain only if they have an executable,
supported implementation. Before the cut:

1. audit the current CUDA and Taichi capability by public operation;
2. remove the Numba-CUDA backend and the `"cuda"` value that denotes it;
3. retain a generic GPU API only if the remaining backend meets declared
   scientific, dependency, failure, and fallback contracts;
4. otherwise remove the unfulfilled GPU surface before 1.0 and reopen GPU
   acceleration later as a focused capability proposal.

Numba must not survive merely to preserve an experimental GPU claim.

## Current Evidence and Scope

The expensive mathematical port is already substantially complete:

- all 97 recorded CPU Numba kernels have Rust counterparts;
- high-level consumers are wired through the coexistence seam;
- the Rust suite records 175 passes and 3 documented skips;
- forced Rust and forced Numba full-suite runs produced the same 9,489 passes
  and the same 48 unrelated WIP failures at the 2026-07-24 checkpoint;
- parity is exact on many inputs and tolerance-bound where compiler,
  accumulation, or eigensolver behavior necessarily differs;
- the Rust implementation deliberately corrects known behavior in triclinic
  minimum image, broadcast dihedral editing, and principal-axis signs.

The remaining removal surface is still broad:

- 48 Python files currently import Numba;
- 101 `@lazy_njit` sites remain;
- 11 Numba-CUDA modules remain;
- Numba appears in package, development, test, documentation, and conda
  dependencies;
- warmup, diagnostics, configuration, API registry, tests, and active guides
  still describe JIT behavior;
- the crate still lives under `experiments/rust_kernels/`;
- multiplatform production wheel CI is not implemented.

These counts are an audit checkpoint, not a permanent manifest. The cut must
create an executable zero-Numba validator rather than relying on these numbers
remaining current.

## Progress Accounting

Progress must be reported at the end of every segment using the exit gates
below. A green test count alone does not complete a segment whose packaging,
documentation, or installed-product evidence is still missing.

| Segment | Weight | Completion rule |
| --- | ---: | --- |
| A — conversion-fidelity coherence | 25% | all four conversion stages and their audit gate are green |
| B — final Numba oracle | 10% | inventory, parity artifact, and deliberate divergences are complete |
| C — Rust packaging | 20% | every declared wheel and source artifact installs and passes |
| D — Rust-only cut | 20% | zero-Numba validator and API cleanup are green |
| E — scientific and ecosystem validation | 15% | full scientific, suite, wheel, and consumer gates are green |
| F — lifecycle and release candidate | 10% | documentation, course, release matrix, and clean-candidate gates are green |

The weighted total is the sum of completed exit gates. Work inside an open
segment must be reported separately as local progress, not converted into
optimistic global credit. Update this table or a dated checkpoint after every
segment, including evidence links and the exact commit tested.

These weights measure closure of the **remaining 1.0 plan**, not total historical
MolSysMT development. The completed Rust port and earlier consolidation are
prerequisite evidence and must not be misreported as zero progress on the
library itself.

Every segment report must contain:

- segment and local stage status;
- evidence and exact commands;
- failures or accepted omissions;
- files or contracts changed;
- regressions and downstream impact;
- completed weighted total;
- the next approved action.

The living state and evidence log are maintained in
[`release_1_0_status.md`](../release_1_0_status.md). Update that ledger rather
than inserting transient status throughout this plan.

## Critical Path to 1.0

### Segment A — Restore Conversion-Fidelity Coherence

**Status:** completed. The text below preserves the decision boundary and exit
criteria that governed the work.

Segment A is **not** a requirement to make every registered conversion
exhaustive before any other 1.0 work can continue. Conversion routes must be
triaged by contract and impact:

1. **Systemic blockers:** audit machinery, scope semantics, strict-mode
   correctness, selection/structure alignment, and silent corruption. These
   block Segment A.
2. **Advertised Tier 1 routes:** fix the contractual direction, explicitly
   reject unsupported input, or narrow the advertised contract. Silent loss is
   not acceptable, but full native fidelity is not required when the target
   model cannot represent it.
3. **Accepted non-exhaustive debt:** known losses with executable reporting,
   stable baseline classification, and no regression. These do not block 1.0.
4. **Tier 2/3 or low-priority edges:** defer explicitly unless they expose a
   shared correctness defect. They must not consume the critical path merely
   because the conversion graph contains them.

The gate is therefore **contract coverage plus zero new unclassified debt**, not
“all conversion edges are lossless.” A route that cannot be supported honestly
before 1.0 may be narrowed or removed from the advertised Tier 1 surface.

Follow
[`conversion_fidelity_wip_contract_gaps.md`](../archive/resolved_bugs/conversion_fidelity_wip_contract_gaps.md)
in its declared order:

1. establish the audit-scope contract;
2. implement exhaustive native-dictionary auditing and strict loss handling;
3. resolve the independent schema and adapter defects;
4. resolve PDB fidelity as its own workstream.

**Exit gate:**

- the fidelity audit imports and executes;
- the formerly failing WIP modules are tracked and green;
- no systemic or advertised Tier 1 correctness failure remains;
- tracked conversion contracts remain green;
- the WIP can be partitioned into reviewable commits;
- normal pytest remains the result authority.

This segment is first because deleting a compute backend while unrelated tests
are red makes it harder to distinguish migration regressions from pre-existing
conversion failures.

### Segment B — Freeze Numba as the Temporary Oracle

Once Segment A is green:

1. forbid new Numba kernels and new direct Numba consumers;
2. produce a generated inventory of Numba imports, JIT sites, CUDA modules,
   configuration, public API, diagnostics, dependencies, docs, and tests;
3. map every CPU kernel to:
   - its Rust implementation;
   - its high-level consumers;
   - parity tests;
   - independent scientific or property evidence;
4. record every deliberate numerical divergence and its tolerance;
5. run the final two-backend comparison and preserve the result as a dated
   migration artifact.

Numba may be corrected during this segment only when necessary to make the
oracle scientifically valid. It must not receive new features or performance
work.

**Exit gate:**

- no CPU consumer lacks a Rust route;
- no Numba-only CPU capability remains;
- every deliberate divergence has independent justification;
- the final parity artifact is reproducible;
- the inventory is complete enough to detect residual Numba after deletion.

### Segment C — Productize Rust Packaging

This segment must finish before runtime deletion.

1. Move production Rust source out of `experiments/` to its accepted permanent
   location.
2. Spike and select one packaging design:
   - preferred: mixed Python/Rust MolSysMT wheel with private
     `molsysmt._rust`;
   - fallback: required version-locked private kernel distribution.
3. Build `cp311-abi3` wheels for:
   - Linux x86_64 and aarch64;
   - macOS x86_64 and arm64;
   - Windows x86_64.
4. Test each artifact in a clean environment rather than the development
   worktree.
5. Exercise Python 3.11, 3.12, and 3.13 and the supported NumPy range.
6. Define the source-distribution policy explicitly. An sdist that requires a
   Rust compiler is acceptable only when documented and when supported binary
   wheels cover the release platforms.
7. Add wheel-build and installed-wheel smoke tests to CI.
8. Preserve all current Python-package behavior during the build-backend
   change:
   - versioning derived from Git tags;
   - `molsysviewer.addons` entry points;
   - bundled `molsysmt.data` resources and `py.typed`;
   - lazy public imports and form discovery;
   - hard/soft dependency declarations.
9. Build with the committed `Cargo.lock` and a pinned Rust toolchain. Run
    formatting, Clippy, Rust unit tests, and dependency, security, and license
    audits in CI.
10. Select and test explicit binary compatibility floors, including the Linux
    manylinux/glibc target, macOS deployment target, Windows runtime, and a
    portable CPU instruction baseline. Do not build developer-machine-specific
    instructions into release wheels.

### Rust–Python Boundary Contract

Before the extension becomes mandatory, every exported binding family must
define and test:

- accepted NumPy dtype, dimensionality, shape, and contiguous/non-contiguous
  layouts;
- whether inputs are borrowed, copied, or made contiguous;
- output dtype, ownership, mutability, and shape;
- behavior for empty arrays, missing optional arrays, non-finite values, and
  invalid indices;
- preservation of the configured single/double precision contract;
- typed Python exceptions for invalid input or internal failure;
- containment of Rust panics so no panic unwinds across the Python boundary;
- GIL-release behavior for expensive kernels and safety of borrowed arrays
  while the GIL is released;
- Rayon thread-pool behavior under `num_threads`, xdist, BLAS, and nested
  MolSysSuite callers, including oversubscription tests;
- deterministic behavior where the public scientific contract requires it.

Public wrappers remain responsible for units, digestion, selection alignment,
and user diagnostics. Rust bindings receive prepared unit-free arrays and must
not create a second public validation vocabulary.

**Installed-wheel smoke contract:**

- `import molsysmt` succeeds;
- `convert`, `get`, `select`, representative PBC operations, distances, RMSD,
  PCA, SASA, and topology component discovery execute;
- no repository checkout, local `target/`, or development installation is
  visible;
- the extension is private and version-compatible with the Python package;
- a missing or unloadable required extension fails at import or installation
  with an actionable error, never by silently selecting another algorithm.
- wheel contents include the required package data, typing marker, metadata,
  and entry points;
- execution does not depend on an in-tree shared library, `LD_LIBRARY_PATH`, or
  a developer Rust installation.

**Exit gate:** every target platform produces and installs a passing artifact.

Conda publication is a separate delivery lane. It must reproduce the same
Rust-only runtime before the Conda package is published, but sibling-package
availability on the `uibcdf` channel does not block scientific consolidation,
wheel validation, the 1.0 source/tag decision, or manuscript work.

### Segment D — Perform the Rust-Only Runtime Cut

Make the cut as a reviewable series, not one opaque deletion.

#### D1. Remove CPU Dispatch Ambiguity

- make high-level consumers call the Rust implementation directly;
- remove the `auto`/`rust`/`numba` resolution seam and fallback imports;
- remove `configure.kernel` and the uniform `kernel=` override;
- preserve `parallel_mode`, `num_threads`, and workload thresholds only when
  they have backend-independent Rust semantics and tests;
- remove Numba-only global runtime state.

#### D2. Delete the CPU Numba Implementation

- delete CPU JIT kernel modules or reduce mixed modules to genuinely reusable
  Python preparation code;
- delete `_private/jit.py` and `make_numba_signature.py`;
- remove `lazy_njit`, compilation registries, cache handling, and JIT warning
  machinery;
- retire parity tests only after their final artifact is recorded;
- retain and strengthen independent property, analytical, curated-system, and
  external-oracle tests.

#### D3. Resolve the GPU Boundary

- remove the Numba-CUDA modules and availability checks;
- remove `"cuda"` from active configuration and digestion;
- retain Taichi or another backend only if its public scope passes the same
  scientific and failure-contract gate;
- otherwise narrow or remove the GPU API for 1.0 and preserve the desired
  future design in a post-1.0 proposal.
- update every affected public signature, docstring, API classification,
  User Guide page, Cookbook recipe, course module, and GPU-specific test in the
  same lifecycle-complete change.

#### D4. Remove Runtime and Packaging Residue

- remove Numba, Numba-CUDA, and direct `llvmlite` requirements from
  `pyproject.toml`, conda recipes, development, test, docs, and production
  environments;
- remove `warmup(numba=...)`, `warmup_numba()`, Numba cache controls, and
  Numba-specific diagnostics;
- retain or redesign `warmup()` only for backend-independent lazy module loading
  if that behavior remains useful and contract-tested;
- update the public API stability registry before 1.0;
- remove active documentation and course instructions that prescribe JIT
  warmup;
- keep historical Numba measurements only in clearly archived records.

**Zero-Numba gate:**

- an executable validator finds no active Numba imports, decorators,
  configuration values, diagnostics, dependencies, or release documentation;
- the validator also rejects direct active `llvmlite` and Numba-CUDA coupling;
- allowed occurrences are restricted to archive history and the dated
  migration record;
- a clean environment without Numba installs and passes the Rust-only tests;
- no public operation has a hidden fallback to a removed implementation.

### Segment E — Rust-Only Scientific and Ecosystem Validation

Run validation after deletion, not only before it:

1. Rust unit and property tests;
2. focused scientific-truth suites for every kernel family;
3. the complete MolSysMT suite through pytest-receptor, with normal pytest as
   authority;
4. the release fast gates;
5. installed-wheel tests on the complete Python and platform matrix, with
   sibling dependencies preinstalled from controlled sources when the Conda
   channel is not yet current;
6. smoke workflows in direct MolSysSuite consumers, applying release gates in
   proportion to consumer maturity:
   - MolSysViewer is a foundational MolSysSuite component and its direct
     MolSysMT integration smoke is blocking;
   - earlier-stage consumers such as TopoMT and PharmacophoreMT are diagnostic
     probes. Their workflows must be executed and incompatibilities classified,
     but consumer-local adaptation debt does not block MolSysMT 1.0;
7. cold-start, steady-state, memory, and thread-count benchmarks;
8. explicit verification that there is no JIT warmup or cache creation.
9. Rust `fmt`, Clippy, unit, dependency, and panic/error-boundary gates.
10. oversubscription checks under serial execution, xdist, and representative
    nested MolSysSuite workloads.

Numerical expectations must be updated only when supported by independent
scientific evidence. The former Numba result is not sufficient evidence by
itself after the oracle is retired.

**Exit gate:** the Rust-only runtime is scientifically green, wheel-green, and
usable by the foundational MolSysSuite consumer. Earlier-stage direct
consumers have been probed and any incompatibility is assigned to the owning
project rather than silently transferred to MolSysMT.

### Segment F — Complete the Remaining 1.0 Lifecycle Work

After the conversion and Rust-only blockers are green:

1. resolve the Four Paths numbering defect and add its structural validator;
2. execute the Common Core and every course notebook affected by current API or
   behavior changes;
3. clarify function support-tier policy without creating a competing registry;
4. archive completed proposals and move durable rules into normative guides;
5. rebuild demos and documentation affected by conversion or runtime changes;
6. run the exact release procedure in [`release_gate.md`](../release_gate.md);
7. tag only the clean commit that passed the full Python 3.11–3.13 matrix and
   installed-wheel tests.

## Work That Must Not Block 1.0

The following remain valid post-1.0 work unless they reveal a correctness
defect:

- new native PDB, XTC, DCD, or other third-party-independent parsers;
- Arrow or optional-column memory experiments;
- reactive chemical states and interaction datasets beyond the accepted 1.0
  boundary;
- fused Rust multi-observable passes and speculative GPU redesign;
- broad Tier 2 and Tier 3 adapter expansion;
- further kernel micro-optimization after release thresholds are met;
- paper extensions that do not alter the released scientific contract.

The coordinated publication of sibling dependencies and MolSysMT on the
`uibcdf` Conda channel is an independent delivery track. It may run during
manuscript writing or review. It blocks only the claim that the Conda package
is available and validated; it does not block the library, source release,
scientific validation, or article.

These items may proceed in separate branches or with independent collaborators,
but they must not be merged into the release candidate without satisfying the
same review and test gates.

## Commit and Integration Discipline

The current dirty tree is not a release artifact. Each segment must be landed in
coherent commits whose subject identifies the contract being closed.

Recommended commit boundaries:

1. conversion scope contract;
2. native dictionary exhaustive audit;
3. each independent schema or adapter repair;
4. PDB fidelity causes in focused groups;
5. permanent Rust crate layout and packaging;
6. each CPU consumer family cut;
7. Numba CPU deletion;
8. GPU boundary decision and deletion;
9. dependencies, warmup, diagnostics, API registry, and documentation cleanup;
10. release lifecycle and gate updates.

Do not mix unrelated dirty files merely to reduce the working-tree count. A
temporary compatibility seam may exist between commits on a feature branch, but
every commit merged to the release branch should have an interpretable test
result.

## Required Design Checkpoints

Implementation must pause for an explicit concept and plan review before:

- changing the root build backend or choosing a separate required Rust wheel;
- fixing the permanent crate/module location and public/private naming;
- deciding whether any GPU API survives the Numba-CUDA removal;
- removing or changing public warmup, kernel, GPU, parallel, or precision
  arguments;
- accepting a numerical divergence or changing a scientific tolerance;
- narrowing a platform, architecture, Python, NumPy, or installation contract.

These reviews are decisions, not invitations to reopen the Rust-only direction.
Their purpose is to choose the safest implementation of that direction.

## Stop Conditions

Stop the cut and investigate before continuing if:

- an installed Rust wheel cannot reproduce a result that passes in the
  development worktree;
- a target platform cannot build or import the required extension;
- scientific truth fails outside an explicitly justified tolerance;
- Rust-only execution loses a Numba-only public capability that was intended
  for 1.0;
- a direct MolSysSuite consumer requires undocumented internal Numba symbols;
- pytest-receptor and normal pytest disagree on verdict, counts, or exit code.

Rollback means reverting the current focused migration commit while preserving
the final parity evidence. It does not mean restoring a permanent runtime
backend switch.

## Definition of Done

MolSysMT is ready for the 1.0 release candidate only when:

- conversion fidelity is coherent and the release audit executes;
- the Rust extension ships and installs on every declared platform;
- Numba is absent from the active runtime, dependencies, build, tests,
  diagnostics, public API, and current documentation;
- the Rust–Python array, error, GIL, and threading boundary is executable and
  documented;
- the wheel preserves versioning, entry points, data resources, typing metadata,
  and lazy discovery;
- CPU and any retained device capabilities have independent scientific
  evidence;
- the full suite and release gates pass on the exact committed candidate;
- applicable User Guide, Cookbook, API, demo, and Four Paths material is
  accurate and verified;
- the working tree is clean and no release blocker remains open.
