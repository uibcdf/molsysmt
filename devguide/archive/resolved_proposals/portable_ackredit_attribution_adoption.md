---
summary: Adopt portable Ackredit attribution in the existing interaction result wrapper
issue: uibcdf/molsysmt#292
status: resolved
opened: 2026-11-17
closed: 2026-11-17
verification: reproduced
area: [api, deps, docs]
guard: tests/interactions/test_portable_attribution.py
normative: devguide/interactions_api.md
blocked_by: []
supersedes: []
---

# Portable attribution in the interaction pilot

**Reported:** Ackredit's incoming #292, reviewed during #334's B0 follow-up.
**Status:** resolved for the bounded interaction-pilot portable adoption.

## What

Interaction results currently carry detached `molsysmt.scientific_attribution@1`
records, while the optional provider observes successful operations through its
public scopes and credit API. The result wrapper itself is not an
`ackredit.attribution@1` payload and cannot be passed directly to that reader.
The older #27 pilot report also retains outdated provider-publication statements.
Ackredit #22/#75 and MolSysSuite #68 are closed; that does not establish local
adoption of their released portable contract.

## How

Retain the existing wrapper, target and bibliography, adding a portable field
that projects this result's original references into the published schema-1
reader contract. Encode only known result uses and original producer context;
do not claim to reconstruct a full observed workflow or child-call trace.
The projection is deterministic host-owned metadata even when Ackredit is absent.
Use its real public `Attribution.from_dict` reader to verify interoperability.
Keep rendering and workflow capture in Ackredit rather than duplicating them.

Credit the reached interaction branch with the same scientific/reference/software
roles and original context through the existing lazy optional boundary. Loading,
querying, copying and rendering saved attribution must not credit another
calculation or replace its producing software versions. Existing observation
arrays, units, method semantics and H5MSM codecs remain unchanged.

## Why

Applications need each saved result's original bibliography as well as a combined
workflow report. Session deduplication cannot identify a reused result's
references. A portable projection permits detached reporting without installing
the original scientific engines or guessing today's bibliography.

## Acceptance and limits

- Two real calculations, including evaluated-empty coverage and reused references,
  have independent original bibliographies and contribute to an enclosing workflow.
- The actual public Ackredit reader accepts each portable result projection;
  detached rendering adds no credit and preserves original versions.
- Typed and H5MSM round trips retain both legacy fields and the portable projection.
- Actual absence, provider failure, fresh-process lazy import and fresh readers
  preserve scientific results and host provenance. Provider failure remains diagnosed.
- Use the existing environment/support composition with recorded origins. No
  shared-prefix installation, public extra, core dependency or provider release
  qualification is selected here. Ackredit >=0.9.0 is the published reader
  capability floor; this is not certification of every supported installed minor.
- Update the result contract and its User Guide/Cookbook/course explanations.
  Keep #27's wider rollout and optional call observation outside this bounded adoption.

## Evidence

Inspected `molsysmt/_ackredit.py`, the interaction attribution adapter, existing
result/persistence tests, the synchronized Ackredit guide and the owning suite
policy. The native REST paginated acquisition returned five comments for #292;
the service's issue metadata reports thirteen. The connector returned the same
five. This discrepancy is retained, not interpreted as proof that other comments
never existed. The selected acceptance is the visible issue body and received
provider policy.

Five new public-reader/persistence cases fail on the original source with
`KeyError: 'portable'`. After the additive implementation, 33 focal cases pass
with Ackredit source `6421d573600a1bb7f9a4a3be18481f27e460a957` (clean worktree),
including the existing real MolSysViewer session/metadata consumer guard.
The strengthened selection adds detached portable/legacy ownership and passes
34 cases with the exact public Ackredit 0.9.0 payload extracted into owned
storage. Its archive SHA-256 is
`37661090f6ad19a74b8155d8a4d4b4a068c9099f4ceba0743b3abfe887e97fe1`.
No shared-prefix installation or new environment is used. The floor run's
single pytest assertion-rewrite warning comes from importing Ackredit before
pytest in the launcher; no case is skipped. A preceding launcher SyntaxError
is retained as an unsuccessful tooling attempt, not a provider/scientific bug.

These runs retain lazy import, actual provider-blocked absence, diagnosed failure,
reused/empty results, original versions, typed conversion, named and standalone
H5MSM, remapping, fresh detached readers and source-consumer compatibility.
They do not qualify browser geometry, a clean installed client, other Python
minors, a new native binary or the final release pair. Documentation receiving
and final source checks remain to be recorded before closure.

## Resolution — 2026-11-17

The existing host wrapper keeps `schema`, `target` and `items`, with an additive
`portable` field that the real public Ackredit reader accepts. Known result uses
retain their original records, roles, method/profile and software versions even
without the provider. The projection explicitly has result-bibliography scope,
while the actual provider observes contextual credit in application-owned captures.
No full workflow graph is invented and no scientific observations, schema codec,
public signature, dependency classification or Python range change.

All 1,933 selected interaction/curated/composition controls pass with no skips;
the final public-floor selection passes 42 cases without skips. These scopes
overlap. Five original missing-field failures and the interrupted first broad
run remain recorded. The source consumer session/metadata guard passes; no
browser molecular-canvas, installed-pair or cross-Python acceptance follows.
Provider-dependent reader tests remain optional in an ordinary environment,
while the admitted receiving selection explicitly requires the real provider
and rejects a skip-based acceptance. Host-only metadata coverage remains runnable
without it.

The public docstring's seven examples, all fifteen cheap offline gates, Ruff,
the strict complete documentation and the final sixteen-article/four-view static
receiving pass. The four course modules retain their scientific examples and
explain the portable result scope. Original producer metadata and diagnostic
behavior are unchanged. The broader #27 library rollout remains partial.

[Supplemental receiving](../../../devtools/data/supplemental_pre1_work_334_20261117.json)
contains runtime/import identities, exact public archive, original failures,
source hashes, resource limits and the distinction from final qualification.
The durable contract is [Interactions](../../interactions_api.md).
