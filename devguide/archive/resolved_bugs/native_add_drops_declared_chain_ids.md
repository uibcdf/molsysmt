---
summary: Native add clears declared chain IDs despite keep_ids=True
issue: uibcdf/molsysmt#353
status: resolved
opened: 2026-10-09
closed: 2026-10-09
severity: high
verification: reproduced
area: [basic, native, form]
guard: tests/basic/add/test_chain_identifiers.py::test_add_preserves_duplicate_chain_ids_and_names
normative:
blocked_by: []
supersedes: []
---

# Native add clears declared chain IDs despite keep_ids=True

**Reported:** 2026-10-09 by DockingMT during uibcdf/dockingmt#17/#33.
**Status:** Resolved; preserving explicit chain metadata during native addition.

## What

Public detached strict `msm.add` retains prepared mechanics and the two chain
indices but changes explicit input chain IDs `A` / `A` to missing labels.
PDBQT serialization consequently emits blank chain fields.

```python
import molsysmt as msm
molsys = msm.convert('5x72_receptor.pdbqt', to_form='molsysmt.MolSys')
part = msm.extract(molsys, selection=[0, 1])
msm.set(part, element='atom', atom_id=[1482, 1483])
combined = msm.add(molsys, part, in_place=False, keep_ids=True,
                   attribute_policy='strict')
print(msm.get(combined, element='chain', chain_id=True))
# Before correction: ['<NA>', '<NA>']
```

The exact fixture and SHA-256 are recorded in the related resolved mechanics
report for uibcdf/molsysmt#352; this defect is independently reproduced after
that mechanics correction, without rewriting source labels.

## How

`Topology.add` already offsets atom chain indices and concatenates the explicit
chain tables. Its subsequent `rebuild_chains` call defaults to rebuilding indices;
that resets the chain table. With ID/name regeneration disabled, the reset leaves
the supposedly preserved fields missing.

Keep the already aligned chain table and indices during addition by passing
`redefine_indices=False` to this metadata rebuild. Retain explicit ID/name
columns and existing type inference; `keep_ids=False` still deliberately
regenerates IDs. This uses the existing native rebuild controls without a
PDBQT-specific repair or a new interpretation of standalone chain rebuilding.

## Why

Chain IDs are labels, not positional indices. Two distinct chains may carry the
same declared label. Public composition must preserve those declarations when
requested, including in detached systems and molecular file output. Downstream
clients should not restore known labels after a provider operation discards them.

## What is measured and what is assumed

The original fixture reproduces `['A']`, `['A']` inputs and
`['<NA>', '<NA>']` output in the shared Python 3.14 environment after the #352 fix.
No downstream docking calculation is executed. Qualification of newer packaged
artifacts remains separate from these source regressions.

## What was refuted

This is not a collision requiring renamed chain IDs: the independent positional
chain indices remain valid. The writer faithfully projects the missing fields
it receives; parser/writer special cases cannot repair the native data loss.

## Scope and exclusions

Preserve IDs/names in native topology addition and public MolSys addition,
including selected source chains and explicit `keep_ids=False` regeneration.
General chain inference, chemical-state alignment and collision handling in
other domains are unchanged. Do not modify the frozen candidates or their files.

## Acceptance criteria

- Preserve duplicate explicit string IDs and names while offsetting chain indices.
- Preserve source input tables and detached target data.
- Retain the selected source's chain label after atom/chain remapping.
- Continue deliberate ID regeneration with `keep_ids=False`.
- Preserve chain labels through the supported native PDBQT writer.
- Verify the exact original fixture and relevant hierarchy/composition regressions.
- Update the affected User Guide, Cookbook, course and public docstrings.

## Provenance

2026-10-09, Linux, Python 3.14.7, Pandas 2.3.3,
ArgDigest `0.15.0+1.g5c6711e`, preserved native extension; starting source
`739395d7e` already includes the separate #352 fix.

## Resolution and validation — 2026-10-09

The native chain rebuild now retains the already offset indices and concatenated
chain table. Its existing flags continue type inference and deliberate ID
regeneration. The public wrapper, native class, Foundations, Toolbox, Cookbook
and Common Core Module 17 document the distinction between labels and indices.
Notebook code cells and outputs are unchanged.

Contract-tested in the shared development environment:

- The initial regression run showed four preservation failures (two public
  in-place modes, selected-chain remapping, and PDBQT output). A fifth failure
  was an existing native argument-digestion limitation, not this metadata bug.
  The direct native test now uses the same controlled, typed delegation as
  existing native topology tests; public `msm.add` tests keep digestion enabled.
- `python -m pytest tests/basic/add tests/basic/merge
  tests/native/test_topology_operations.py tests/native/test_hierarchy.py
  tests/native/test_component_metadata_rebuild.py
  tests/native/test_molsys_chemical_state_association.py --receptor=llm -n12`:
  **151 passed**, including the five new regression cases and #352 tests.
- `python -m pytest molsysmt/basic/add.py molsysmt/native/topology.py
  --doctest-modules --receptor=llm -n12`: **2 passed**.
- The exact 5X72 fixture now produces 1,483 atoms, aligned charges and parameter
  types, and chain IDs `['A', 'A']`. Public PDBQT conversion writes 1,483 atom
  records, all with chain field `A`; the source labels remain unchanged.
- Repository-wide `ruff check .` and `ruff format --check .` pass. The preceding
  #352 remote Ruff and suite-policy failures were solely formatting of its new
  test file; formatting is corrected without changing test assertions here.

- `python devtools/scripts/release_gate.py`: **14/14 fast gates passed**,
  including dependency, developer-guide, course (156 notebooks), citation,
  resource, Rust hot-path and public-API smoke checks. This script does not run
  or waive the paused heavy release campaign.

The named guard verifies both declared IDs/names and distinct offset atom-chain
indices, and checks source/detached-target preservation. Additional tests cover
selection, intentional ID regeneration and the supported native writer.
The full release/platform campaign remains paused; these are source regression
results, not qualification of a replacement release artifact.
