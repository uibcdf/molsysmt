---
summary: MDTraj topology subsets lose chemical metadata and retain sparse hierarchy indices
issue: uibcdf/molsysmt#623
status: resolved
opened: 2026-11-06
closed: 2026-11-06
severity: high
verification: reproduced
area: [form, extract]
guard: tests/form/mdtraj_Topology/test_extract_metadata.py::test_selected_metadata_dense_axes_and_source_independence
normative:
blocked_by: []
supersedes: []
---

# Preserving MDTraj topology subset metadata

**Reported:** 2026-11-06, while receiving the optional-provider contract under #524/#334.
**Status:** Corrected and contract-tested in `0ea1e04d7ba59f0d3cb4e378b1667f53dc18975f`;
public-source receiving and board closure follow.

## What

Public `msm.extract(mdtraj_topology, selection=[2, 3])` loses a retained chain's
label and a known atom formal charge. Retained groups/chains can keep indices
outside the new dense domain. A four-atom source with chains A/B, group positions
0/1 and charges `[1, 0, -1, None]` yields two atoms with chain label `None`,
chain/group index `1` despite a one-chain/one-group output, and charges
`[None, None]` instead of `[-1, None]`. Source tables remain unchanged.

## How

The manual partial-extraction branch in
[extract.py](../../../molsysmt/form/mdtraj_Topology/extract.py) omits chain IDs and
formal charges. It creates parents before knowing whether they contain selected
atoms and deletes empty parents afterwards without remapping their indices.
Its `resSeq or residue.index` expression also replaces an explicit zero label.

## Why

Downstream native conversion, chemical queries and visual selection can read
incorrect identity or unknown chemistry from the extracted result. The defect
is in MolSysMT and reproduces with a current provider; raising the provider floor
alone cannot repair it. It is separate from #622's native inventory validation.

## What is measured and what is assumed

The retained `623-mdtraj-extraction-probe.json` records the exact source and result
on Python 3.14.7/MDTraj 1.11.1. Formal charges and positional indices are literal
fixture values, not inferred chemistry. The broader minimum-provider run passes
many existing assertions but did not cover these selected-subset fields.

## What was refuted

MDTraj 1.10.3 separately loses metadata when copying its own Topology. Upstream
1.11.0 repairs that copy contract, grounding the optional floor in #524. This
adapter defect remains independently reproducible on 1.11.1 and needs an owner
correction. A version declaration cannot replace that correction.

## Scope and exclusions

Preserve selected chain/group labels, atom formal charges and serials, bond
metadata, sorted source atom order and independent results. Construct only
retained parents so all target hierarchy indices are dense. Keep unknown values
unknown and explicit zero labels intact. Do not change public selection syntax,
external atom-selection deduplication, structure selection, chemistry inference,
provider storage, or native ChemicalStates ownership.

## Acceptance criteria

- Public extraction from multiple chains/groups retains correct known/unknown
  charges, serials, labels, bond endpoints/type/order and dense hierarchy indices.
- Zero group sequence labels survive; crossing a discarded parent does not leave
  a hole. Empty subsets and valid full/subset selection remain defined.
- Returned objects are independent and source metadata stay unchanged.
- Retain linear set-based membership checks; do not replace this path with a
  provider subset loop that scans an array for each source atom.
- Maintained guards fail before correction and pass with the qualified provider
  minimum and a newer published version. User-facing documentation and the
  public source/board closeout retain exact evidence and limits.

## Provenance

Linux x86_64, existing development Python 3.14.7 and MDTraj 1.11.1, 2026-11-06.
No shared environment or native backend was changed to reproduce this defect.

## Resolution and receiving

The existing adapter now creates a target chain/group only when its first
selected atom is retained. Public MDTraj construction maintains dense indices
and counters; no private table pruning or counter repair remains. Atom serials,
known/unknown formal charges, chain IDs, group sequence/segment labels and bond
type/order are preserved explicitly. Set membership retains the existing
source-order/deduplication behavior and linear source scanning, without adopting
a provider subset routine that scans an index array for each atom. No speed or
memory benchmark is claimed.

The maintained counterexamples fail eight cases before correction, while six
valid empty/full-copy controls pass. Directed receiving then passes fourteen
cases and the public adapter doctest. Final integrated source receiving passes
1,191 cases with public MDTraj 1.11.0/Python 3.13 and 1,191 with public
1.11.2/Python 3.14, with no failures or omissions. A separate 654-case profile
receives affected documentation, runtime/provider tools and workflow contracts;
these scopes overlap. The
[receipt](../../../devtools/data/mdtraj_subset_receiving_623_20261106.json)
retains actual import origins, artifacts, command scopes, native exits and
evidence limitations.

The 1.11.0 profile has 237 warnings: 201 provider parser deprecations, sixteen
legacy-H5MSM, fourteen fixture unit-cell warnings and six explicit unsupported-GPU
diagnostics. The 1.11.2 profile has the latter 36 warnings. They are not ignored
test failures. Notebook changes are confined to prose, preserving code, outputs,
IDs, metadata and cell counts. Four human autosummary edits and the native backend
remain unchanged. Ruff lint/format and the maintained documentation checks pass.
The metadata floor required for safe full copies is independently recorded under
#524 in `962b2c68e4e71d1245a293b9e7a2c5a47db00160`. This source receiving does
not qualify an installed MolSysMT artifact, full platform matrix or release.
