---
summary: CIP result reference authors are shared with later calculations.
issue: uibcdf/molsysmt#503
status: resolved
opened: 2026-10-27
closed: 2026-11-03
severity: medium
verification: reproduced
area: [physchem, metadata, attribution]
guard: tests/physchem/test_get_cip_stereochemistry.py::test_nested_reference_edits_cannot_change_canonical_or_other_results
normative:
blocked_by: []
supersedes: []
---

# CIP result reference authors are shared with later calculations

**Reported:** 2026-10-27, while receiving the expert chemical readers under
uibcdf/molsysviewer#264. Opened with the principal maintainer's authorization.
**Status:** native result ownership repaired and locally qualified; no expert
forwarding or scientific-method change is needed.

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

Record: `devguide/archive/resolved_bugs/cip_result_reference_authors_are_shared_with_later_calculations.md`.


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

## Resolution — 2026-11-03

The result builder now uses the standard library's `deepcopy` for the small
reference dictionary, rather than a shallow `dict` copy. No molecular system,
coordinate array or trajectory is copied by this correction. The method,
labels, selected axes, software provenance and optional Ackredit integration
remain unchanged. Public docstring and Toolbox scope explicitly include nested
author-list ownership. The existing foundation/history contracts and course
module 20's nested-metadata guarantee are reviewed and remain applicable;
no code cell or output changes are needed.

Two independent regression cases cover a positive declared S center and an
evaluated-empty selection. They edit a returned author list, then check an
earlier result, a later result, the private reference, canonical article data
and all three detached attribution records. Source bytes and the scientific
labels/empty shapes must remain unchanged. A `finally` restores canonical lists
even in the intentionally failing run, preventing cross-test contamination.
Both cases fail before the correction (**two failures**, exit 1, 1.99 s) and
pass afterwards. The complete CIP module and public doctest pass **26 cases**,
zero skips/failures, exit 0, 8.85 s.

The related SDF stereochemistry, fixed-state hydrogen, preparation-history and
Ackredit receiving selection passes **119 tests**, zero skips/failures, exit 0,
23.42 s, with 17 disclosed existing warnings. Canonical receptor streams are
complete; JUnit independently agrees. This uses the existing Linux/Python 3.14.7
development installation and actual optional providers, not a clean installed
package or platform matrix. Raw evidence remains in ignored
`.pytest_cache/stabilization-503/`.

The audit also inspects the other CIP-reference consumers. `cip_attribution_items`
already deep-copies its inputs, including the SDF writer's credits. Fixed-state
hydrogen output/history own deep copies of their reports, and the Ackredit
bridge copies records before registration. None requires a blanket reference
rewrite. The defect is the direct public CIP result boundary, which now owns
its nested bibliography.

Routine hosted qualification remains separately pending; no source, installed
matrix, public package or release gate is relabelled as passing by this local
fix. The native ownership defect has an addressable regression and is closed
on that scoped evidence; the wider candidate/CI obligation remains explicit.
