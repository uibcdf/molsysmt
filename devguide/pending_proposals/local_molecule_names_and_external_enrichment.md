---
summary: Separate supported local molecule labels from future database enrichment.
issue: uibcdf/molsysmt#25
status: partial
opened: 2026-10-05
closed:
verification: inspected
area: [attribute, docs]
guard:
normative:
blocked_by: []
supersedes: []
---

# Local molecule names and external enrichment

**Reported:** Historical naming request, reviewed during S1 stabilization on 2026-10-05.
**Status:** Local naming is implemented and contract-tested; remaining enrichment is post-1.0.

## What

The original issue asks for protein, small-molecule and entity names, including
names obtained from databases through Sabueso. Its maintainer comment explicitly
declines reliable identity resolution until an enrichment provider can supply it.
These are two distinct capabilities: a local label and a verified chemical identity.

## How

Native rebuilds preserve consistent explicit metadata and synthesize deterministic
local labels when names are absent. The owning rules are in
[`molsysmt/element/AGENTS.md`](../../molsysmt/element/AGENTS.md) and
[`molsysmt/native/AGENTS.md`](../../molsysmt/native/AGENTS.md).
`native/_topology_infer.py` supplies molecule/entity defaults; the native PDB
adapter preserves polymer names declared in COMPND. Public helpers expose these
labels without requiring an online provider. `redefine_names=True` intentionally
requests local reconstruction rather than identity enrichment.

## Why

Names such as `protein 0`, `small molecule 0`, `water` and source-supplied labels
are useful for local selection. They must not be advertised as authenticated
database identities. Neither a repeated label nor the entity fallback grouping
proves chemical equivalence.

## Evidence and remaining work

**Contract-tested:** On source `0efb14144`, Python 3.14.7, the seven existing
molecule/entity naming tests passed in the 35-test S1 baseline selection.
`tests/element/molecule/test_get_molecule_name_from_molsysmt_MolSys.py`
checks preservation of `VILLIN`, water and ion labels and explicit redefinition;
`tests/element/entity/test_get_entity_name.py` checks local entity labels.
This is not database matching or exhaustive naming coverage across every form.

The remaining work is to specify optional enrichment with an owning provider,
explicit source/provenance, ambiguous and unmatched results, offline behavior,
and preservation of user labels. No online lookup or new dependency is admitted
by the current [frozen scope](../release_1_0_scope.md).

## What was refuted

The old issue does not establish that every unnamed input is a runtime defect.
Current supported native workflows already expose local names; absence of a
database-derived name is an accepted capability boundary. Removing local name
queries would break supported selections without solving identity resolution.

## Acceptance criteria

Keep #25 open, classified as a post-1.0 proposal for its enrichment remainder.
Before implementation, define the provider boundary and independent identity
fixtures, including ambiguity and absence. S1 only requires documenting and
checking the existing local convention; it does not certify rich identification.
