---
summary: Physchem property readers have inconsistent element scope contracts.
issue: uibcdf/molsysmt#471
status: resolved
opened: 2026-10-26
closed: 2026-10-26
severity: medium
verification: reproduced
area: [physchem, api, selection]
guard: tests/physchem/test_property_selection_contract.py
normative:
blocked_by: []
supersedes: []
---

# Physchem property readers have inconsistent element scope contracts

**Reported:** 2026-10-26 during addon receiving under uibcdf/molsysmt#421,
consumer uibcdf/molsysviewer#264. Filing explicitly authorized by the maintainer.
**Status:** resolved at the native boundary; consumer reception is separate.

## What

Four property readers ignore their declared element parameter and always resolve
the selection on a fixed axis. Hydrophobicity rejects non-group levels as an
internal algorithm failure. Parameter documentation lists broader structural
levels despite the actual atom/group return contracts.

```python
import molsysmt as msm
molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'])
for element in ['atom', 'group', 'system']:
    print(msm.physchem.get_atomic_radius(molsys, element=element, selection=[1]))
# all three: [0.17] nm, selecting atom 1
```

Electronegativity similarly returns [2.55] for all three scopes. Polarity returns
[8.1] and transmembrane tendency [0.38], always selecting group 1. Hydrophobicity
returns [0.62] at group scope and raises InternalAlgorithmError at atom/system.

## How

Radius/electronegativity explicitly call basic.get(element='atom');
polarity/transmembrane explicitly call basic.get(element='group'), ignoring the
public argument. Hydrophobicity explicitly rejects element != 'group' with an
internal algorithm exception. The bound addon preserves these native calls and
has no alternative aggregation formula or argument rewriting.

## Why

Integer selections can address different populations at atom/group scope. A
successful call can therefore be interpreted as a different requested population,
without an explicit rejection. This is a contract issue even if the per-atom or
per-group default is scientifically correct. It is separate from syntax
propagation in uibcdf/molsysmt#470.

## What is measured and what is assumed

Fifteen native calls were executed: five tools times atom/group/system with
selection=[1]. The values/rejections above were observed. Other hierarchy
levels follow inspected fixed-axis code but were not individually executed.
No scientifically meaningful universal aggregation is assumed.

## What was refuted

No Viewer synchronization or result conversion is involved. The native functions
reproduce this directly. Supporting every hierarchy by an arbitrary sum or mean
is not a justified repair.

## Scope and exclusions

Define each function's supported levels. Prefer an explicit public argument error
for unsupported levels before interpreting selection. If broader aggregation is
deliberately supported, document its scientific meaning, selection axis and output
shape. Do not change the default property tables or hide unknown chemistry.

## Acceptance criteria

Native pytest guards cover all five functions and supported/unsupported levels,
string and integer selections with distinct atom/group populations, empty,
repeated/reordered inputs, definitions, units/container/shape and source
nonmutation. Documentation must agree. Invalid public choices must not look like
internal algorithm failures or silently use a different scope. Receive that
native contract through the addon afterwards.

## Provenance

Linux, Python 3.14.7, molsyssuite@uibcdf_3.14, frozen native e395e5264.
Native-only calls use the bundled pentalanine MolSys without importing Viewer.


## Additional receiving scope — 2026-10-26

On frozen native d7c82e92f, get_surface_area, get_area_buried and
get_buried_fraction also ignore their declared element and always use the
group axis. Each returns the same one-group value with selection=[1] for
element atom, group or system. Treat these in the same native scope contract,
with explicit rejection of unsupported axes rather than invented aggregation.
get_volume and both ProtOr helpers have no element argument, so their fixed
axis is not classified as ignoring an argument. Concurrent working-tree
repairs are not qualified by this frozen-baseline observation.

## Resolution — 2026-10-26

Eight readers with fixed population semantics now reject other element levels
with ArgumentChoiceError before interpreting selection: atomic-radius and
electronegativity on the atom axis; hydrophobicity, polarity, transmembrane
tendency, surface area, buried area and buried fraction on the group axis.
No scientifically arbitrary aggregate is introduced. Group reference charge
keeps its documented higher-level sums and definition-specific atom restriction;
an unsupported bond population now gets an explicit argument-choice diagnostic
instead of an uninitialized or empty result.

The actual volume and ProtOr signatures expose no element argument and are not
silently expanded. get_area_buried still has no syntax argument. Existing table
values, raw-score/quantity containers, valid definitions and unknown-group
errors are preserved. The Collantes surface-area docstring no longer certifies
unverified nm-squared units: the raw result and still-open primary-reference
review remain explicit under uibcdf/molsysmt#473. No physical rescaling or new
scientific validation is claimed.

The 435-case native guard checks exact literal values and independently resolved
populations, all supported empty/repeated scopes and all unsupported public
hierarchy choices, including an invalid selector that must never reach population
lookup. It exercises actual MolSys and Topology paths without Viewer and
preserves source scientific tables. The receiving-scope extensions above are
retained as frozen-baseline evidence, not retroactively relabeled as success.


## Qualification — 2026-10-26

The full physchem and argument selection passes **976 tests** in 81.59 seconds
with `--receptor=llm -n 12`, without skips. Its 87 warnings are existing legacy
H5MSM, future pandas fillna and explicit unsupported-GPU diagnostics. All forty
new source doctest examples pass. The original generic group example selected
an unparameterized ACE cap and correctly raised UnknownGroupInTableError; it
was corrected to known amino-acid groups, without weakening that diagnostic.
Ten property tutorials and course Module 20 execute successfully. The named
charges Cookbook and Foundations were updated as prose; their unrelated
pre-existing chemical-preparation examples were not rerun by this checkpoint.

The [normative query contract](../../physchem_query_contract.md) records current
scope and units. Commands, environment, source hashes and remaining limits are
retained in the [query qualification receipt](../../../devtools/data/physchem_queries_20261026.json).
No installed-consumer, full scientific/release matrix or new attribution-method
qualification is claimed. Consumer receiving remains separately owned by
uibcdf/molsysmt#421 and uibcdf/molsysviewer#264.
