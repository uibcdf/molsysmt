---
summary: Covalent paths lose integer axes and empty path width.
issue: uibcdf/molsysmt#508
status: resolved
opened: 2026-10-27
closed: 2026-10-27
severity: medium
verification: reproduced
area: [topology, interactions, molsysviewer]
guard: tests/topology/get_covalent_paths/test_empty_and_selected_paths.py
normative:
blocked_by: []
supersedes: []
---

# Covalent paths lose integer axes and empty path width.

**Reported:** 2026-10-27 during expert-addon receiving.
**Status:** resolved; native contract repair and bounded addon receiving tested.

## What

`topology.get_covalent_paths()` does not preserve its rectangular empty-result contract. A valid empty position can promote otherwise integer source atom indices to float and cause ArgumentError; disconnected nonempty positions return shape (0,) instead of (0, len(path)). The classic donor helper inherits the failure for custom donor candidates without indexed H.

## How

Reproduced independently without Viewer, native basis 40a8ac2ea4042f807c7897459183b5533126781d, Python 3.14:

```python
import molsysmt as msm
from rdkit import Chem
molsys = msm.convert(Chem.MolFromSmiles("CC=O"))
for path in [[[2], []], [[], [1]], [[0], [2]]]:
    try:
        result = msm.topology.get_covalent_paths(molsys, path=path)
        print(path, result.tolist(), result.shape, result.dtype)
    except Exception as error:
        print(path, type(error).__name__, str(error))

msm.interactions.hbonds.get_donor_atoms(
    molsys, inclusion_rules=("atom_type=='O'",),
    default_inclusion_rules=False, default_exclusion_rules=False,
)
```

Observed: [[2], []] rejects selection 2.0; [[], [1]] rejects 1.0; [[0], [2]] returns int64 array with shape (0,). The custom donor query rejects 2.0. This is a fully converted declared RDKit chemical graph, not missing source chemistry. Concatenating selected indices with an untyped empty selection promotes the union to float; final `np.array(output, dtype=int)` also loses the path-width axis when output is empty. A downstream donor sort needs a two-column result.

## Why

These are ordinary no-match outcomes for scientific graph queries. Please preserve source integer indices and shape (0, len(path)) for valid empty/disconnected paths and receive the outcome through donor-H recognition. Add native pytest cases for empty first/middle/last/all positions, string and equivalent numeric selectors, masks, disconnected graphs, hydrogen-free custom donors, valid nonempty/interleaved pairs, exact dtype/shape and source preservation. Unsupported path specifications should have explicit public validation; do not invent paths or H.

Distinct from #165 (ragged scalar normalization), #258 (donor-pair column ordering), #355 (empty bonded-to selector) and #506/#507 (rule lists/language). Consumer context: uibcdf/molsysmt#421 / uibcdf/molsysviewer#264. The thin expert addon adds no empty-array patch or graph algorithm. Closure is protected by the native guard named in the front matter; the original consumer receiving remains distinct from installed-package qualification.

## What is measured and what is assumed

The standalone native reproducer runs without Viewer. The provider source basis
is 40a8ac2ea; its scientific implementation matches the earlier 667f03b9a basis.
These are contract/shape/form observations, not new scientific methods or a
claim of universal input validity.

## What was refuted

This does not require a GUI callback, a molecular edit or consumer selection
translation. Existing reports named above have different failure mechanisms;
no duplicate was found before filing. The positive expert fixtures use supported
chemistry and valid axes; this excluded native limit stays independently visible.

## Scope and exclusions

The native helper and direct expert consumer are in scope. No wrapper graph
algorithm, index cast, result reshaping or frame policy is introduced here.

## Acceptance criteria

Resolve the public semantics and add mechanically addressable native pytest
coverage for the matrix above. Preserve source chemistry and original source
indices. Receive the owner repair separately in the addon before changing its
documented limitation; a source wrapper is not blanket scientific qualification.

## Dependencies and risks

The native scientific owner chooses and implements the contract. Consumer
compensation would hide disagreement across ordinary source forms and calls.

## Resolution — 2026-10-27

The public path digester now accepts a nonempty ordered pattern of scalar
source indices, flat integer candidate collections or selection strings. It
normalizes into a separate container, rejecting unsupported dimensions, nested
selectors, booleans and fractional indices. Empty candidate positions remain
valid. All selectors, including bounds and syntax, are checked before the
no-match return, so an empty position cannot hide a later invalid selector.
Selection syntax is forwarded consistently to both the global mask and each
string position. Numeric source indices are never interpreted as local subset
positions or cast from fractional values.

The helper returns an explicit int64 array of shape `(0, len(path))` before
union/graph construction when a candidate position is empty. Disconnected
nonempty candidates receive the same shape at traversal completion. Existing
nonempty walk traversal and ordering remain unchanged, including revisits.
The keyword-only `skip_digestion=False` adds the standard explicit trusted-call
boundary without moving or changing earlier positional arguments/defaults;
the intentional addition is recorded in the public API stability registry.

The donor helper receives the topology repair without scientific changes or
consumer array patches. The addon forwards the newly native skip control and
its focused hydrogen-free donor test confirms `(0, 2)`/int64 while preserving
the scene. Current User Guide and addon guidance no longer advertise #508 as
an unresolved limit. Other donor-rule and structure-bound defects remain in
uibcdf/molsysmt#506, #507, #509 and #511.

### Verification

- Initial native red regression: 24 failed, 11 passed, independently reproducing
  float promotion, lost width, malformed-selector errors and downstream donor
  failure. Final focused suite: 104 passed on Python 3.14 with 12 pytest workers
  and Pytest Receptor. Its independent declared-edge oracle checks nonempty
  walks, while retained TcTIM cases check established ordering.
- Equivalent MolSys, Topology, TopologyDict and H5MSM 0.5 topology-only sources;
  MolSysMT/MDTraj selector parity, source-index masks, readonly candidates,
  invalid selectors after empty positions and trusted valid calls are covered.
- Addon topology/role receiving: 77 passed. No chemistry, coordinates, stored
  analyses or scene projection are modified by these queries.
- The docstring doctest is included in the 104-case suite. The full TcTIM
  tutorial is executed successfully. Only the relevant load/path cells of
  course Module 13 are executed, retaining other stored examples/outputs and
  correcting its mistaken shortest-path description. Foundations and Toolbox
  explain source axes and valid empty results. No existing Cookbook recipe
  calls this helper; no unrelated recipe is added.
- Public API stability, docstring fidelity, dependency leakage and Ruff checks
  pass. Strict Sphinx output is checked for both warnings and notebook schema
  errors, including the separate metadata repair tracked by uibcdf/molsysmt#514.

This is contract-tested and bounded form-parity evidence, not a new chemical
recognition model or universal scientific qualification. The existing general
NetworkX traversal is reused; no new backend, dependency, unit convention,
coordinate calculation, scientific method or citation is introduced. An empty
candidate axis avoids unnecessary graph allocation; no performance benchmark
or compiled-speed claim is made. Hosted/installed candidate qualification and
both 1.0 releases remain separate.
