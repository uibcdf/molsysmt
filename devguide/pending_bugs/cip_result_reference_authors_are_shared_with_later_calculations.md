---
summary: CIP result reference authors are shared with later calculations.
issue: uibcdf/molsysmt#503
status: open
opened: 2026-10-27
closed:
severity: medium
verification: reproduced
area: [physchem, metadata, attribution]
guard:
normative:
blocked_by: []
supersedes: []
---

# CIP result reference authors are shared with later calculations

**Reported:** 2026-10-27, while receiving the expert chemical readers under
uibcdf/molsysviewer#264. Opened with the principal maintainer's authorization.
**Status:** open; native ownership repair is separate from expert forwarding.

## What

`physchem.get_cip_stereochemistry()` returns a shallow copy of its reference dictionary: the nested `authors` list is shared with the canonical Hanson reference. Editing a completed result changes bibliography in later results and their otherwise detached attribution items. Numerical CIP labels need not change for provenance to become contaminated.

## How

Reproduced without MolSysViewer on source `f9ca3e1b0328d2463492f0969fec6805dfc7ca5b`, Linux/Python 3.14.7, RDKit 2025.09.5, using `molsyssuite@uibcdf_3.14`:

```python
import molsysmt as msm
from rdkit import Chem
molsys = Chem.MolFromSmiles('CCO')
first = msm.physchem.get_cip_stereochemistry(molsys)
first['references'][0]['authors'].append('consumer-edit')
second = msm.physchem.get_cip_stereochemistry(molsys)
assert second['references'][0]['authors'] is first['references'][0]['authors']
assert 'consumer-edit' in second['references'][0]['authors']
assert any('consumer-edit' in item.get('authors', [])
           for item in second['attribution']['items'])
```

Run the reproduction in a short-lived process; it intentionally edits returned metadata. The public function constructs `references=[dict(REFERENCE)]` and `_private/stereochemistry.py` spreads the canonical `ARTICLES['hanson_2018']` dictionary without detaching its nested authors. `cip_attribution_items()` deep-copies the already polluted reference, so subsequent credits also contain the edit. This is independently reproduced rather than inferred from #490, which repaired different feature readers.

## Why

The expert addon under #421 / uibcdf/molsysviewer#264 must retain native results and provenance without consumer-specific metadata repairs. Editing one completed report must not modify canonical bibliography or unrelated future calculations.

## Acceptance criteria

Detach the small mutable reference metadata at its owning native boundary, without copying whole molecular systems or trajectories or altering chemical labels, selections, state resolution or scientific method definitions. Add native pytest guards for nested mutation in a positive result and an evaluated-empty result, verifying earlier results, later results, canonical reference data and later attribution remain unchanged. Audit other CIP reference consumers where applicable without assuming all have the same defect. Keep #490's scope separate and do not add a Viewer workaround.

Record: `devguide/pending_bugs/cip_result_reference_authors_are_shared_with_later_calculations.md`.


## What is measured and what is assumed

The isolated native-only reproduction confirms shared author-list identity and
pollution of later plain references and later attribution. It restores the list
before process exit. It does not show numerical label changes, molecular-system
mutation, or the same defect in every scientific reader. Source f9ca3e1b0,
Python 3.14.7, Linux, RDKit 2025.09.5. No Viewer import or workaround is needed.

## Scope and exclusions

Small reference metadata ownership at the native CIP boundary. No whole-system
copy, new chemical algorithm, provider version change, consumer deepcopy or
scene edit. Native #490 fixed different feature readers; this reproduction is
separate. Positive and empty source outputs need independent reference guards.
