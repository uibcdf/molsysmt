---
summary: Rigid-fragment tutorial uses retired Topology chemical attributes
issue: uibcdf/molsysmt#648
status: resolved
opened: 2026-11-08
closed: 2026-11-08
severity: medium
verification: reproduced
area: [docs]
guard: tests/chemical_states/test_public_graph_tutorials.py::test_rigid_fragment_tutorial_uses_complete_public_chemical_state
normative:
blocked_by: []
supersedes: []
---

# Retired chemical attributes in the rigid-fragment tutorial

## What

The Python example in [the tool page](../../../docs/content/user/tools/chemical_states/get_rigid_fragments.md)
uses `Topology(n_atoms=4)`, assigns `molsys.bonds` and accesses
`molsys._chemical_states`. Topology deliberately has no chemical facade after
#255. The page's explanatory text correctly mentions ChemicalStates, but its
example has not followed that contract.

## Evidence and limits

Source inspection on main `4cafe7af25d626729c58df67adf30a788d2e0630`
confirms the stale calls and the native chemical-attribute refusal. The old
example has not been executed in this review. No rigid-fragment algorithm defect
or numerical result is established. HTML success alone cannot prove that a
Markdown Python block runs. This was found while reading adjacent tools for
#645; the new indexed-H policy is independently received.

## Intended outcome and acceptance

Execute the old example first. Replace its chemical authority with the supported
ChemicalStates/explicit-context route, and state complete connectivity or the
supported explicit assumption without inferring bonds through Topology. Preserve
the existing anchor, source atom/bond indices, cut/bridge restrictions and packed
fragment expectations. Add an executable public-example guard for every Python
block, then check the adjacent graph examples at the documentation checkpoint.
This is a bounded pre-1.0 repair, not completion of #378's whole discoverability
proposal or a reason to change the scientific algorithm.

## Reproduction and correction — 2026-11-08

The unmodified Python block fails once on source `3de256e1c` with AttributeError
at its retired `_chemical_states` access. A direct Python assignment of `bonds`
does not restore a Topology chemical facade. The corrected example constructs
standalone ChemicalStates, appends a state and uses public add_bonds/basic.set.
It declares complete connectivity in the public ChemicalStatesDict transport
and validates that payload by converting back. No private mutation or new graph
algorithm is introduced. The original cut index and all packed outputs remain.

The directed battery passes 48 cases, including all Python blocks in this page,
the chemical-state portal and the adjacent rotatable-bond page. The guard also
checks the literal atom/bond axes, packed memberships, int64 types and retained
source bonds independently of the example's own assertions. Its first authored
version incorrectly expected `bonded_atoms` to return pairs; that query returns
the atom union. One failed/47 passed attempt preceded correction to the public
get_bonds table. This was a test-authoring mistake, not a product defect. The
corrected attempt peaks at 339,165,184 bytes under a 2 GiB/one-CPU/no-swap cap,
without OOM or host-reserve violation. Exact clean-source receiving and shared
documentation gates remain pending before closure.

## Resolution — 2026-11-08

Clean source `d2ce182a46cf247fa466f31606402cf3734ba8d4` passes 89 combined cases,
including twenty new example/axis controls and the changed public getter
doctest; zero skips/failures/errors. Fourteen fast gates and the incremental
HTML build pass on the same source with no changed hashed inputs. Actual
Tool/Cookbook/course HTML content is checked separately from Python execution.
No scientific algorithm or dependency changes. The
[receiving record](../../../devtools/data/public_graph_xyz_receiving_648_610_20261108.json)
retains exact commands, negative controls, authoring mistakes, checksums,
notebook preservation and bounded memory measurements. Broader #378 and
installed/full-source/final-candidate acceptance remain separate.
