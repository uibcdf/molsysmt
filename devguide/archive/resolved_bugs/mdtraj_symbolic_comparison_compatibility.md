---
summary: The installed MDTraj parser rejects symbolic non-strict comparisons.
issue: uibcdf/molsysmt#484
status: resolved
opened: 2026-10-26
closed: 2026-10-26
severity: medium
verification: reproduced
area: [selection, dependencies]
guard: tests/basic/select/test_mdtraj_comparisons.py::test_public_mdtraj_comparison_populations
normative:
blocked_by: []
supersedes: []
---

# The installed MDTraj parser rejects symbolic non-strict comparisons.

## What
The installed MDTraj 1.11.1 / PyParsing 3.3.3 pair rejects `index >= 0` and `index <= 0` directly on a valid one-atom MDTraj topology. `ge`/`le` aliases and the other tested comparisons work. MolSysMT exposes the same upstream parsing failure through its external-syntax route. This is a dependency-compatibility record, separate from #482's chemical-state normalization.

## How
```python
import mdtraj as md
molecular_topology = md.Topology()
group = molecular_topology.add_residue('LIG', molecular_topology.add_chain())
molecular_topology.add_atom('C', md.element.carbon, group)
for expression in ['index >= 0', 'index <= 0']:
    molecular_topology.select(expression)  # ValueError from parser
assert molecular_topology.select('index ge 0').tolist() == [0]
assert molecular_topology.select('index le 0').tolist() == [0]
```
The [official MDTraj selection reference](https://mdtraj.readthedocs.io/en/latest/atom_selection.html#operators) lists these symbolic comparisons as supported. A 12-operator native-provider audit reproduces failures only for <= and >= in this environment. No molecular preparation, Viewer or MolSysMT import is necessary to reproduce it.

## Why
External selections are a public MolSysMT capability used by the expert Viewer addon (uibcdf/molsysmt#421; uibcdf/molsysviewer#264). Compatibility and upstream routing belong to the scientific provider; consumers must not silently rewrite selectors.

## Acceptance criteria
Determine the affected provider/dependency range and an upstream or compatible-version resolution; do not infer it from this single environment. Add a native public-selection pytest matrix covering symbolic and alias comparisons with intended populations, using an explicitly complete target hierarchy. Keep underlying diagnostic cause and make any actual compatibility limits visible. No consumer monkeypatch or automatic selector rewrite.

Measured Linux/Python 3.14.7, MDTraj 1.11.1 and PyParsing 3.3.3, existing shared development environment. This is not a clean installed-pair or cross-platform qualification.

## What is measured and what is assumed

The reported behavior was executed in the existing Python 3.14 environment.
No clean-install or full compatibility-range conclusion is inferred.

## Alternatives and refuted paths

The reproduction excludes the molecular viewer. Native authority and the direct
provider remain separate from the compact or consumer presentation. The caller
will not rewrite inputs or reinterpret successful/failed exits to hide the gap.

## Scope and exclusions

The initial report requested a provider-owned guard without changing the
runtime. The resolution below adds optional dependency constraints and a
reviewed one-package development-environment correction. Release tags and
publication state remain unchanged.

## Diagnosis and upstream resolution — 2026-10-26

The installed MDTraj selection grammar delegates comparisons to PyParsing's
`infix_notation`; its sorted operator list places `<` before `<=` and `>` before
`>=`. PyParsing 3.3.3 introduced an iterative infix implementation that accepts
the shorter prefix in this case. This is the upstream regression reported in
[pyparsing/pyparsing#672](https://github.com/pyparsing/pyparsing/issues/672),
also confirmed by the MDTraj maintainer in
[mdtraj/mdtraj#2190](https://github.com/mdtraj/mdtraj/issues/2190). No duplicate
upstream issue or local provider patch is needed.

Official PyPI metadata inspected on this date still lists PyParsing 3.3.3 as
latest; a promised 3.3.4 fix is not treated as a published or tested artifact.
MDTraj 1.11.2 is published and declares `pyparsing!=3.3.3`, but also requires
Python >=3.12. Raising MolSysMT's global MDTraj minimum to that version would
remove the supported Python 3.11 adapter route. MolSysMT instead adopts the
provider's exact transitive-parser exclusion in its optional `soft` extra and
maintained development/test Conda environments. Neither MDTraj nor PyParsing
becomes a hard dependency; no MolSysMT runtime selector is rewritten or patched.

Pinned primary metadata:

- https://pypi.org/pypi/mdtraj/1.11.1/json
- https://pypi.org/pypi/mdtraj/1.11.2/json
- https://pypi.org/pypi/pyparsing/3.3.3/json

## Bounded parser matrix

Five official `py3-none-any` wheels were downloaded to a temporary directory and
verified against their PyPI SHA-256 digests. Each was selected through PYTHONPATH
in a fresh subprocess; no package was installed or dependency solved for this
comparison. MDTraj remained the actual installed 1.11.1 in every subprocess.

| PyParsing | Correct populations / twelve symbolic and alias comparisons |
| --- | --- |
| 3.2.5 | 12/12 |
| 3.3.0 | 12/12 |
| 3.3.1 | 12/12 |
| 3.3.2 | 12/12 |
| 3.3.3 | 10/12; only `<=` and `>=` fail |

The oracle is the explicit expected four-atom population at an interior
comparison boundary. A one-atom empty/nonempty control alone would be weaker.
This is Linux/Python 3.14.7 evidence for those five parser artifacts, not a
claim about every earlier/future version or another platform/interpreter.

## Public regression and metadata controls

`tests/basic/select/test_mdtraj_comparisons.py` checks twelve operators, compound
AND/OR/NOT expressions, empty results, group projection and provider-error cause
through MDTraj Topology/Trajectory and native Topology/MolSys. The native fixture
has explicit atom/group/chain data and complete component/molecule/entity
hierarchy. Expected populations are declared independently of provider output.

An initial fixture incorrectly requested the undeclared direct
MDTraj Topology-to-MolSys conversion. That authoring error is excluded from
defect evidence; MolSys receives an actual MDTraj Trajectory instead. With the
corrected fixture the original parser yields 28 failures and 44 passes in
12.35 seconds. With the 3.3.2 wheel, the 72 public cases and three dependency
metadata controls pass (75 cases, 10.31 seconds). The broader selection,
chemical-reference and dependency-audit selection passes 292 cases in 12.85
seconds with 18 expected legacy-H5MSM warnings. All runs use pytest-receptor and
twelve workers; the compatible runs explicitly select the temporary wheel.

The metadata controls reject 3.3.3 while admitting measured compatible 3.2.5 and
3.3.2 across the optional extra and both maintained Conda specifications. They
check admitted versions rather than merely the spelling of a requirement.
No xfail, query rewrite, provider monkeypatch or fallback syntax hides the bug.

Foundations, the selection tutorial, the conversion Cookbook and shared course
Module 07 explain the exact exclusion and existing-environment update. Notebook
changes are prose-only; code cells, outputs and metadata are unchanged.

## Reproducible evidence and scoped checks

The [compatibility receipt](../../../devtools/data/mdtraj_parser_compatibility_20261026.json)
records exact wheel URLs/digests, all twelve expected/observed populations per
parser, environment, metadata and source hashes. Raw temporary logs are not
committed. The dependency-contract and soft-import audits pass. All 491 raw
notebook-schema cases pass (8.05 seconds), as do all fourteen fast release gates.
Incremental Sphinx compilation finishes with zero errors and fifty warnings
under the existing uibcdf/molsysmt#144 debt; warning counts are not compared
against a fresh build baseline. No full scientific/platform/installed-pair
qualification or publication authorization is inferred.

## Resolution and installed development-runtime check

A frozen-dependency Mamba dry run rejected the requested downgrade with
conflicting requests. A normal targeted dry run then proposed only replacing
PyParsing 3.3.3 build pyh5ded981_0 with 3.3.2 build pyhcf101f3_0. After reviewing
that exact one-package plan, the change was applied in the existing shared
development environment. The actual transaction changed only PyParsing. No
auxiliary environment, MDTraj update, parser monkeypatch or sibling code change
was needed. The installed Conda archive URL and SHA-256 are in the receipt.

Without a wheel overlay or custom PYTHONPATH, the same broad regression passes
**292 cases in 12.13 seconds**, with sixteen expected legacy-H5MSM warnings.
All fourteen fast release gates pass again in that actual development runtime.
These results do not describe a clean installed MolSysMT/Viewer package pair.

The guard asserts actual selected populations for every symbolic/alias operator
and supported fixture form. Re-admitting the defective parser makes the
non-strict population cases fail; the separate manifest controls prevent the
maintained solve routes from accepting that demonstrated version again. The
exclusion remains bounded to 3.3.3; a promised future release is not certified
without testing it. The existing provider issue owns the upstream repair.
