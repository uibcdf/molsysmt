# Library engineering and scientific audit — 4 November 2026

> **Document role:** Archived assessment, recorded at the maintainer's request.
> This is a dated review of source `93d29bf23e2c54f238f7ada984a4b23420b4b3b0`,
> not a normative specification, independent external certification, release
> approval, or replacement for the active issue queue. Future corrections should
> be appended with their date. Implementation and issue states below refer to
> this review date.

## Overall judgment

MolSysMT has a sound architectural direction and a valuable scientific purpose.
Recent changes have substantially improved its ability to represent molecular
information and preserve its meaning across operations and components. Maturity
is uneven: core geometry and data contracts are more consolidated than some
chemical interpretation and preparation tools.

The appropriate conclusion is neither that every operation is correct nor that
another wholesale redesign is needed. Preserve the architecture, resolve concrete
inconsistencies, strengthen independent scientific evidence, and keep supported
scope explicit. More functions alone would not establish greater reliability.

## Scope and method

This was a directed maintainer-assisted review of representative implementations,
contracts, tests and open issues, followed by bounded local execution. It was not
a line-by-line audit of every module, security review, performance campaign,
complete test run, or qualification of installed public artifacts.

Inspected areas included:

- native `MolSys`, `Topology`, `ChemicalStates` and native query delivery;
- sparse `Interactions` storage, inverse indexes, queries and attribution;
- public distance execution, numerical backend organization and unit boundaries;
- pi-pi and metal-coordination scientific definitions and limitations;
- reference properties and group-template/name helpers;
- form discovery, conversion contracts, dependencies and scalability guidance;
- the scientific evidence registry, representative analytic/reference tests and
  curated interaction comparisons;
- the README and relevant active issues.

Sources included [the native model](../../CORE_SPECIFICATION.md),
[form contracts](../../forms_and_conversions.md),
[interaction contracts](../../interactions_api.md),
[scientific validation](../../scientific_validation.md),
[the evidence matrix](../../scientific_evidence_matrix.md) and
[scalability](../../SCALABILITY.md). These maintained documents, executable code
and their owning issues remain authoritative after this snapshot.

No runtime source, scientific table, API, issue state or release reference was
changed by the audit. The local uncommitted #548 work was not treated as delivered
behavior on main.

## Executed evidence and provenance

Execution used the existing Linux development environment with Python 3.14.7,
the repository source above, the existing compiled backend and published
Pytest Receptor reporting. The receptor override came from the existing local
published-tool payload; the existing controlled Viewer runtime was available on
the test import path. This was not a clean installation of a public package pair.

Four pre-existing generated API documentation edits remained in the checkout.
Consequently, the scientific execution certificate correctly reports
`tracked_source_dirty=true` and `release_eligible=false`. Passing development
checks must not be recast as an exact clean release certificate.

| Check | Observed outcome | Scope |
| --- | --- | --- |
| Registered scientific evidence executor | 79 passed, 59 registered nodes, zero failures/errors/skips; one legacy-H5MSM warning | Independent evidence for the registered claims and bounded cases, not every possible input |
| Curated metal coordination, curated cation-pi and public MolSys/H5MSM interaction workflow | 60 passed | Reference comparison and public integration behavior for the selected cases |
| Dependency validator | Passed; no top-level optional-dependency imports found; OpenFF CI bounds complete | Static dependency checks, not proof of every runtime dependency path |

The original scientific execution certificate is retained alongside this report:
[scientific execution certificate](library_engineering_and_scientific_audit_20261104_scientific.json).
Its SHA-256 is
`a054fecdd34df09729dd9fa411b597ab8a2310a759f15c48cf7e59ff3a35e455`.
The other outcomes were observed in command output; no separate retained
machine-readable receipt is claimed for them.

Commands, from the repository root in the configured development environment:

```bash
python devtools/scripts/execute_scientific_evidence.py --receptor=llm \
  --certificate /tmp/molsysmt-review-scientific-20261104.json

python -m pytest --receptor=llm -n 2 \
  tests/scientific_truth/curated/test_metal_coordination.py \
  tests/scientific_truth/curated/test_cation_pi_interactions.py \
  tests/interactions/test_public_molsys_h5msm_workflow.py

python devtools/scripts/validate_dependencies.py
```

The executed environment also set `MPLBACKEND=Agg`, `OMP_NUM_THREADS=1`, and
disabled Git filesystem monitoring for certificate source inspection. Runtime
dependencies were not newly installed or frozen by this review. The certificate
records source, interpreter, platform and exact registered test nodes; it is not
a complete dependency-lock record. Test durations are deliberately not used as
performance benchmarks.

At this date, the generated evidence matrix classified 42 of 43 Stable scientific
APIs as validated and one as partial. Its separate Claimed scope contained one
validated, six partial and one gap entry. These are bounded registry
classifications, not percentages of all scientific behavior proved correct.
Some experimental interaction comparisons exist outside that reviewed registry
scope; unreviewed does not mean untested or incorrect.

## Architectural strengths

### Explicit ownership of molecular information

Separating stable identity (`Topology`), chemical assignments/connectivity
(`ChemicalStates`), coordinates (`Structures`) and calculated observations
(`Interactions`) is a substantive improvement. Connectivity can change without
silently redefining stable molecule membership. A geometric observation need not
be confused with a declared covalent bond. Unknown information, known empty
collections and unevaluated structures can remain distinguishable.

The form-agnostic API and direct native queries serve complementary uses:
interoperation for diverse inputs and lighter repeated access by MolSysSuite
clients, with familiar query arguments. Their common behavior still needs guards;
architectural intent alone does not establish equivalence.

### Results that retain their meaning

`Interactions` separates sparse relations from their structure-specific
occurrences, supports composite participants and roles, and retains evaluated
coverage, producer provenance and source maps. H5MSM preserves associated domains
instead of reducing every system to coordinates and labels. These are useful
foundations for downstream scientific work, not merely serialization conveniences.

### Shared infrastructure

ArgDigest, DepDigest, SMonitor, PyUnitWizard and Ackredit provide appropriate
owners for validation, optional engines, diagnostics, quantities and attribution.
The inspected interaction boundaries use conditional dependency enforcement and
record method/profile definitions and producer versions. Attribution distinguishes
reference implementations and scientific criteria. These providers improve
consistency when correctly adopted; a decorator or passing static check does not
prove that every contract is complete.

## Concrete inconsistencies and known limitations

| Finding | Evidence and consequence | Existing owner |
| --- | --- | --- |
| Legacy group names disagree with native protonation vocabulary | Reproduced: `GLH` maps to `GLN`/`Q`; `HID` raises `KeyError`. Native template vocabulary differs. No incorrect prepared molecular graph was demonstrated. Resolve naming context rather than guessing a universal substitution. | [#549](https://github.com/uibcdf/molsysmt/issues/549) |
| Reference bond helpers accept malformed index maps | Reproduced: NAG names `['C1','C2','C3']` with indices `['a','b','c']` return string endpoint pairs. Integer-map validation is not uniform. | [#554](https://github.com/uibcdf/molsysmt/issues/554) |
| Bond-helper return documentation is inconsistent | Main still contains atom-name return descriptions for index results; the prepared local documentation patch was not yet published. | [#548](https://github.com/uibcdf/molsysmt/issues/548) |
| Collantes descriptor meaning remains incompletely established | Source and reports inspected: provisional surface-area units and legacy ECI charge/aggregation behavior are not primary-reference certification. Unit typing alone cannot establish the correct physical dimension. | [#473](https://github.com/uibcdf/molsysmt/issues/473), [#475](https://github.com/uibcdf/molsysmt/issues/475) |
| Public presentation lags the chemical-domain move | README's structure-analysis example calls `msm.topology.get_dihedral_quartets`; inspection and export probes confirm that the supported owner is `msm.chemical_states`. | [Presentation review #378](https://github.com/uibcdf/molsysmt/issues/378); this audit records the specific remaining example |
| Conversion execution/fidelity coverage is incomplete | Inspected conversion coverage work distinguishes declared routes, executable routes and preserved information. Static admission cannot prove runtime fidelity. | [#181](https://github.com/uibcdf/molsysmt/issues/181) |
| Raw mutation can escape controlled invalidation | Documented boundary: arbitrary writable arrays/tables and retained aliases are not universally observed. This review did not reproduce a new failure of a supported setter. | [#407](https://github.com/uibcdf/molsysmt/issues/407) |
| Input streaming is not universal bounded-memory execution | Inspected contracts: some routes remain eager; detector results may remain resident; memory estimates do not cover complete process RSS. No new memory benchmark was run. | [#336](https://github.com/uibcdf/molsysmt/issues/336), [scalability contract](../../SCALABILITY.md) |

Reproduction of the bounded naming/index/export observations:

```python
import molsysmt as msm

aa = msm.element.group.amino_acid
print(aa.get_standard_name('GLH'), aa.get_1_letter_code_from_name('GLH'))
# GLN Q
aa.get_1_letter_code_from_name('HID')  # KeyError

msm.element.group.saccharide.get_bonded_atom_pairs(
    'NAG', ['C1', 'C2', 'C3'], atom_indices=['a', 'b', 'c'])
# [['a', 'b'], ['b', 'c']]

hasattr(msm.topology, 'get_dihedral_quartets')  # False
hasattr(msm.chemical_states, 'get_dihedral_quartets')  # True
```

These observations do not establish that the incorrect maps are legitimate
supported inputs, that GLH has one universal meaning in every naming dialect,
or that every reference helper has the same failure behavior.

## Maintainability and performance assessment

Newer, carefully specified boundaries coexist with older helpers whose validation,
exceptions and empty/unknown returns are less uniform. Improving that consistency
is more valuable than adding decorators mechanically.

Central modules such as `MolSys`, `Structures`, `Interactions`, `get` and `convert`
contain many responsibilities. Size alone does not demonstrate bad design, but
it increases the cost of understanding and preserving invariants. Extract private
responsibilities when concrete changes justify it; this review does not recommend
another broad refactor merely for stylistic uniformity.

Rust kernels, sparse indexes and chunked execution are appropriate foundations.
No claim of globally optimal performance, complete out-of-core execution or a
whole-process memory bound follows. Future measurements should include first
index construction, repeated queries, conversions, copies, edits, output
accumulation and serialization, not only isolated numerical kernels. Preserve
the distinction between numeric array bytes, Python allocation peaks and RSS.

## Scientific assessment

Three different questions require different evidence:

1. Does the implementation correctly evaluate the declared mathematical rule?
2. Does it reproduce a reference method under the same conventions?
3. Is that method appropriate for the scientific question and chemical domain?

MolSysMT has useful evidence for the first two. The third requires broader,
explicitly scoped campaigns. Matching a metal-ligand distance criterion does not
prove physical coordination. Plausible local hydrogen geometry does not establish
environment-optimized orientation. More detected hydrogen bonds is not by itself
a physically justified optimization target.

Recent interaction docstrings make these limitations explicit. Keep scientific
profiles experimental where evidence is bounded, independently of the reliability
of their result container or persistence route. The inspected secondary-structure
assignment remains a gap in the governed independent-evidence registry; this
does not assert that the implementation is wrong.

Historical physicochemical scales need not be removed merely because they are
old. The useful distinction is between a tabulated descriptor, a property of a
chemical state, a coordinate-derived observable and a model prediction. Their
units, aggregation, assumptions and applicability should be explicit.

## Scientific growth priorities

These are recommendations, not implemented capabilities, new release gates or
an expansion of the accepted 1.0 scope. Existing owner issues retain their plans.

| Direction | Scientific value | Ownership or prerequisite |
| --- | --- | --- |
| Explicit chemical-state alternatives | Compare protonation/tautomer assignments without losing atom correspondence. | [#220](https://github.com/uibcdf/molsysmt/issues/220), [#229](https://github.com/uibcdf/molsysmt/issues/229), [#230](https://github.com/uibcdf/molsysmt/issues/230) |
| Environment-aware preparation | Separate hydrogen inventory, local placement, orientation and relaxation; preserve fixed atoms and state. | [#323](https://github.com/uibcdf/molsysmt/issues/323); general tools in their MolSysMT owners, composite protocol registration/orchestration coordinated with Praxis |
| Chemically specific recognition | Improve delocalized charge-center coverage and metal-specific coordination criteria. | [#262](https://github.com/uibcdf/molsysmt/issues/262), [#337](https://github.com/uibcdf/molsysmt/issues/337) |
| Detector robustness and applicability | Measure sensitivity to methods, cutoffs, hydrogen geometry and chemical state, including negative cases and disagreements. | [#271](https://github.com/uibcdf/molsysmt/issues/271) provides an existing bounded comparison owner; other families require their own reviewed scope |
| Ensemble interpretation | Derive occupancy, persistence and variability with explicit evaluation coverage and statistical assumptions. | Future design/owner review; an arbitrary structure collection is not necessarily a time-ordered trajectory |

Reference conventions must remain visible. For example, RDKit documents multiple
aromaticity models, so disagreement between tools is not automatically an
implementation defect: [RDKit Book](https://www.rdkit.org/docs/RDKit_Book.html).

Ensemble analysis should consider sampling quality and uncertainty rather than
only producing more averages. The distinction between sample count and independent
information is discussed in [Grossfield et al., Best Practices for Quantification
of Uncertainty and Sampling Quality in Molecular Simulations](https://pmc.ncbi.nlm.nih.gov/articles/PMC6286151/).
Reusable statistical capabilities should be placed with their appropriate
MolSysSuite owner, not duplicated merely because MolSysMT produces their inputs.
These references informed recommendations; no literature-wide comparison or new
scientific method validation was performed in this audit.

## Recommended disposition

Before 1.0, prioritize demonstrated inconsistencies in names, index validation,
physical interpretation and public documentation, and clearly distinguish stable
contracts from experimental scientific profiles. Unresolved scientific provenance
needs an explicit bounded disposition, not an unsupported claim of correctness.
The existing release scope and gates still determine acceptance; this assessment
does not freeze a candidate or authorize publication.

After stabilization, prioritize representative independent scientific validation,
environment-aware preparation tools and measured scalability over indiscriminate
API growth. MolSysMT's strongest opportunity is a dependable molecular foundation
for MolSysSuite whose results retain their identity, meaning, provenance and
limitations throughout a workflow.

## Addendum — 4 November 2026: completeness and evaluation priorities

**Purpose:** At the maintainer's request, extend the assessment with explicit
coverage limits and a more actionable evaluation design. This addendum preserves
the original observations and certificate. It adds no executed tests, benchmark
results, defect closures, implementation commitments or release requirements.

The original audit is sufficient to discuss architectural direction and identify
bounded risks. It is not complete enough to certify the entire library or to
demonstrate how much work it saves its users. The reviewer participated in the
development process: knowledge of design intentions can conceal difficulties that
an unfamiliar developer would encounter. An independent review or usability study
has not been conducted here.

### Evaluate the library against its objectives

The [strategic vision](../../competitive_landscape_and_vision.md) and
[core specification](../../CORE_SPECIFICATION.md) motivate the following questions.
This table is an audit design, not a second capability or scientific registry.

| Objective | Evidence inspected in the original audit | Evidence still needed for a stronger conclusion |
| --- | --- | --- |
| Interoperate without losing molecular meaning | Form/conversion contracts, source maps and selected persistence tests | Representative complete conversion routes with independently specified retained, transformed, missing and rejected information |
| Make molecular work easier | Uniform public verbs, native queries and documented examples | Tasks completed by developers unfamiliar with the implementation, recording undocumented assumptions, private API use and required assistance |
| Deliver scientifically interpretable results | Registered analytic/reference evidence and bounded interaction comparisons | Broader chemical applicability, negative/ambiguous cases and sensitivity to scientific choices |
| Serve as reusable MolSysSuite infrastructure | Domain ownership and inspected client-facing result contracts | Representative client workflows demonstrating that clients need neither duplicated chemistry nor private storage access |
| Handle large systems efficiently | Sparse result design, Rust kernels and bounded-execution contracts | End-to-end measurements including conversions, copies, index construction, result accumulation, edits and persistence |
| Remain maintainable as capabilities grow | Shared providers, modular contracts and documented validation | Trace representative changes across code, tests, data and documentation; identify duplicated invariants and sources of drift |

No overall quality percentage or maturity score is justified by this review.
Unknown coverage should remain unknown, rather than being scored as success or
failure. A broader audit should name excluded modules, input classes and optional
engines and assign a confidence level to each bounded conclusion.

### 1. Qualify representative complete workflows

Use existing fixtures and public tests first. Define a small set of workflows
whose completion demonstrates an actual user or client objective:

| Workflow | Required observations |
| --- | --- |
| Inspect and prepare a partially described system, then export it | Missing chemistry stays explicit; only authorized transformations occur; atom maps, retained coordinates and preparation provenance agree with an independent specification; conversion losses are reported |
| Calculate interactions, extract/reorder atoms and structures, save and reload | Participant membership, occurrence identity within the documented scope, evaluated-empty versus unevaluated coverage, units and associations remain consistent; unsupported remappings reject explicitly |
| Query small selections repeatedly from a large system | Selected outputs are correct; first-call and repeated costs are distinguished; any whole-source materialization is measured and explained |
| Operate on sequence-only or coordinate-only information | Supported operations work without inventing absent atoms, topology, chemistry or observations; unsupported operations explain the missing requirement |

For each workflow, declare the input identity and supported scope, expected
results and permitted losses before execution. Record failures as well as
successes. A workflow can share input assets with documentation, but a test that
only executes the same example without independent outcome assertions is not
scientific validation.

This develops the existing
[technical/scientific quality program](../../pending_proposals/technical_and_scientific_quality_improvement_program.md),
conversion work under [#181](https://github.com/uibcdf/molsysmt/issues/181) and
client qualification under [#408](https://github.com/uibcdf/molsysmt/issues/408).
It does not assume that those issues own every proposed workflow. Select and
file bounded implementation work with the responsible component before starting.

### 2. Explain operation readiness without silently repairing input

`has_attribute`, capability reporting and `physchem.get_chemical_readiness`
already answer parts of this question. Evaluate whether their existing results
can provide a coherent operation-specific explanation before designing another
public function or registry.

Keep these conditions distinct:

- the form cannot represent the required information;
- the form supports it, but this instance does not contain it;
- information is present, but its consistency or provenance is unassessed;
- an optional engine is missing or incompatible;
- the method does not support this chemical or geometric case;
- a necessary conversion has declared information loss;
- the requested execution mode or output exceeds a supported memory boundary.

A useful outcome is an actionable explanation with the affected scope and
remaining unknowns. It must not certify chemistry merely because fields exist,
perform an implicit preparation, or replace authoritative argument/dependency
checks at execution. Readiness can become stale after mutation. Any preliminary
check therefore needs an explicit freshness scope rather than permission to
bypass later validation.

ArgDigest should own applicable input constraints, DepDigest optional-engine
availability, and SMonitor diagnostic delivery. Scientific prerequisites remain
owned by the scientific operation. Do not duplicate provider registries or add
unused dependencies to satisfy a checklist.

### 3. Extend invariant and composition tests

The quality program already proposes property and metamorphic tests. Expand
them around risks that cross modules, using deterministic constructions or
recorded seeds and conventions:

- rigid transformations preserve quantities that are invariant under them;
- changes of presentation units preserve the physical result;
- atom permutation plus correct remapping preserves declared relationships;
- eligible block partitions preserve the result of the corresponding whole
  calculation;
- persistence preserves every field promised by its schema;
- extraction preserves the documented local/source axes, including empty and
  nonconsecutive selections.

Do not assert these properties indiscriminately. Some reference criteria depend
on participant order, ensembles need not have a time axis, and conversions may be
intentionally lossy. Specify the mathematical property and its exceptions first.
These guards strengthen, but never replace, an independent numerical or chemical
oracle. Their value is detecting combinations omitted by hand-written examples,
not maximizing test counts or introducing a particular testing dependency.

### 4. Test failure integrity at modification and storage boundaries

Existing controlled edits and transactional guards provide a starting point.
Inventory their coverage before proposing a universal transaction API.

For selected operations, inject failures after staging work but before publication
and verify the declared outcome: unchanged input, explicit partial-result status,
or another documented behavior. Check source/copy independence, interaction
validity, resource closure and whether a target file becomes visible prematurely.
Use independently specified before/after states; do not treat successful
completion of a cleanup callback as proof of restored consistency.

In-memory exception safety, file replacement and crash recovery are different
claims. Process-interruption tests belong only to a storage route that promises
recovery; they must not retroactively imply that H5MSM already supports resumable
analysis append. Relevant existing boundaries are
[#407](https://github.com/uibcdf/molsysmt/issues/407) and
[#336](https://github.com/uibcdf/molsysmt/issues/336).

### 5. Build a stratified scientific reference corpus

Extend the shipped analytic and curated fixtures by scientific phenomenon, not
only by number of molecules. Candidate strata include localized/delocalized
charge, fused aromatic systems, explicit/implicit/absent hydrogens, alternative
chemical assignments, metals, incomplete connectivity, periodic participants and
geometries near decision thresholds.

Each case needs a versioned input, provenance and redistribution permission,
the precise question tested, expected outcome and tolerance, and a statement of
what is unknown. Include positive, negative, unsupported and ambiguous cases.
A correct rejection or explicit unassessed result can be the expected outcome.
Published structures or another program's preparation are not automatically
chemical ground truth.

Keep cases used to tune a new method separate from cases used to evaluate it.
Track whether comparisons share data, recognition rules or implementation so
agreement is not mistaken for independent corroboration. Do not adjust expected
values or tolerances merely to accommodate the implementation.

This corpus would serve preparation, physicochemical interpretation, interactions
and conversions. Reuse existing evidence assets and owners such as #262, #271,
#323 and #337; do not create a competing scientific-evidence registry.

### 6. Evaluate sensitivity of scientific conclusions

Correct implementation of a cutoff does not establish robust classification.
For a bounded detector family, compare outcomes under documented alternatives
in method/profile, thresholds, chemical state and hydrogen geometry. Retain
continuous measurements alongside the resulting classifications where supported.
Report disagreements and excluded cases, not only aggregate agreement.

Sensitivity is not automatically a probability or statistical uncertainty.
Alternative states do not acquire equal physical populations merely because
they were enumerated. Occupancies require an explicit evaluated denominator;
unevaluated structures cannot count as negative observations. Lifetimes require
valid temporal ordering and a stated continuity convention. Review reusable
statistics ownership across MolSysSuite before implementing these analyses.

MolSysMT should provide comparable molecular calculations and their evidence.
Composite preparation/search protocols can be registered and orchestrated with
Praxis under the established division of responsibility. No new protocol has
been implemented or qualified by this addendum.

### 7. Measure the cost of using the library as infrastructure

Benchmark complete selected workflows, including validation, selection,
conversion, calculation, mutation and saving. Separate cold discovery/index
construction from repeated calls, and retained memory from transient peaks.
Include several resident systems and repeated queries, not only one kernel call.

Record exact inputs, versions, thread configuration, hardware, repetitions,
statistics, output size and cache policy. Compare alternative routes only when
their semantics and fidelity agree. The existing
[optional native-column proposal](../../pending_proposals/optional_native_columns_memory_model.md)
is a candidate investigation, not an established optimization.

Further Rust work should follow a measured bottleneck. Compiling a kernel will
not remove costs dominated by copying, conversion or result materialization.
Do not promise one memory budget for the entire process when only numeric
workspace is accounted for.

### 8. Review developer experience independently

Ask a developer who did not implement the feature to complete one small client
integration using only public documentation. Record unclear names, contradictory
help, undocumented prerequisites, necessary maintainer assistance and any use of
private APIs. Distinguish a documentation failure from a missing capability or an
implementation defect.

The useful outcome is a workflow that can be repeated without undocumented
knowledge. No user study, external adoption measurement or comparison against
another library has been performed here. If a later comparison is commissioned,
use equivalent tasks, supported scope and pinned versions; this audit establishes
no superiority over specialist libraries.

### Proposed sequence and stopping criteria

The highest-priority audit extensions are representative complete workflows,
failure integrity and the stratified scientific corpus: each strengthens several
existing capabilities at once. Readiness explanations, sensitivity studies,
performance and independent developer review can then use those same workloads.

Before each campaign, choose its bounded question, responsible owner, evidence
source and stopping criterion. A campaign closes with recorded outcomes,
limitations and issue dispositions, not with a statement that all future
chemistry or usage is covered. Do not turn this list into an indefinitely growing
release gate.

The [1.0 admission rule](../../release_1_0_scope.md#admission-rule) still separates
corrections within accepted scope from new scientific or performance features.
Link work to existing issues where appropriate; independently actionable new
work requires its own reviewed issue under the reporting protocol. This addendum
records evaluation ideas for subsequent scoping and does not itself authorize
implementation, alter API stability or change the release queue.
