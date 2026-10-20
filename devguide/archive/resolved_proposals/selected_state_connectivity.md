---
summary: Resolve explicit chemical states before selecting stored connectivity.
issue: uibcdf/molsysmt#348
status: resolved
opened: 2026-10-20
closed: 2026-10-20
verification: reproduced
area: [api, basic, selection, docs]
guard: tests/topology/test_selected_state_connectivity.py
normative:
blocked_by: []
supersedes: []
---

# State-aware selected connectivity

**Reported:** DockingMT, consumer uibcdf/dockingmt#17 and uibcdf/dockingmt#6.
**Status:** Resolved with source-state resolution, induced selections and general spatial delegation.

## What

Add keyword-only chemical_state, structure_indices and skip_digestion to
get_bondgraph and get_covalent_blocks. Preserve original positions/defaults,
stored-bond semantics and full source atom indices. A selected induced graph
must not connect atoms through omitted atoms.

## How

Reuse public get/select chemical-state resolution and inner_bonded_atom_pairs;
do not create a second chemical-state resolver or infer bonds. External forms
are converted through their existing native routes for explicit state queries.
Unknown/mixed structure associations and unavailable state indices reject
without reference fallback. Reference queries retain existing incomplete-graph
support. The graph's nodes are sorted unique source atom indices; connected
components consequently have deterministic minimum-index order. Empty set
results have object dtype; label arrays retain -1 at unselected source atoms.

During composition, a spatial request exposed get's failure to forward
structure_indices into its internal select calls, including the mask-only path.
The general owner now forwards it. A separate small basic/get guard checks
two structures with independently specified, different spatial neighbors.

## Why

DockingMT must validate connectivity on its actual retained atom inventory in
the state assigned to the relevant structure. Full-system rigid-fragment
projection cannot answer that induced-subset question. The consumer's temporary
local traversal can be removed after its own adoption checks.

## What is measured and what is assumed

Tests declare a six-carbon reference chain and a second state with its middle
edge absent, assigned to nonconsecutive structures 0 and 2. Literal expected
blocks are {0,1,2}/{3,4,5}. Selecting [5,1,0,3,1] instead expects {0,1}/{3}/{5},
without subset renumbering. Tests cover copies, coordinates, invalid requests,
spatial scope, cuts, empty results and native/H5MSM forms. Native 0.1 dictionary
forms contain a reference graph, not a multi-state domain; tests require explicit
state 0 and reject unavailable state 1. No dictionary schema extension is implied.

## What was refuted

- A new state resolver duplicates existing general tools.
- Full-component projection silently connects a subset through omitted atoms.
- Requiring complete connectivity would break supported stored-graph queries.
- Silently filtering relationship types would change legacy graph semantics.
- Converting to a legacy dictionary cannot preserve states its schema lacks.

## Scope and exclusions

State-aware stored connectivity and propagation of the existing structure scope.
No torsion classifier, relationship reclassification, chemistry completion,
dictionary format redesign, copy protocol or native fast-path redesign.

## Acceptance criteria

Assigned-state and induced-subset guards, compatible reference behavior,
form parity where the form contains the requested state, immutable input,
general get spatial delegation, doctests and executed guide/course additions.

## Provenance

Linux, existing development Python 3.14.7, 2026-10-20. Existing NumPy/NetworkX
operations are reused. The sibling checkout remains unchanged.

## Resolution and validation

**Contract-tested:** 1,249 cases pass with
`python -m pytest tests/basic tests/topology
 tests/native/test_molsys_shortcut_validation.py -n 12 --receptor=llm`.
The broad regression caught mixed Python/NumPy node scalars introduced by sorting;
converting sorted nodes to a list preserves the established native-int contract.
The final rerun is fully green. Two public get/connectivity doctests pass.
The two new general spatial-scope guards fail with the previous get implementation
loaded in-process: a query for structure 1 incorrectly returns structure 0's neighbor.
Both pass with the corrected delegation.

The guard's literal assigned-state/subset blocks and separate general spatial
neighbor oracle protect behavior, not just return shapes. All fourteen fast
release checks, docstring fidelity, whole-repository Ruff lint/format and the
public-signature guard pass (two accepted keyword-only extensions). No new
scientific algorithm or reference is introduced. Existing warning classes from
legacy H5MSM, optional providers and attribute-loss policies remain visible.

The two Toolbox notebooks and Common Core 13 contain a newly executed six-atom
example, [0,0,-1,1,-1,2], using the existing development interpreter. A focused
Sphinx build renders their added sections and both actual API docstrings with
no diagnostics. All older cell sources, results and metadata are preserved;
missing cell IDs in the older course notebook are assigned deterministically.
Foundations, the preparation recipe, paired contracts and manifest are updated.
This qualifies source behavior, not replacement release artifacts or consumer
adoption; DockingMT retains responsibility for its own integration checks.
