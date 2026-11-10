---
summary: Selected composite conversion applies trajectory positions to a reference-only provider.
issue: uibcdf/molsysmt#698
status: resolved
opened: 2026-11-10
closed: 2026-11-10
severity: high
verification: reproduced
area: [convert, selection]
guard: tests/basic/convert/mult_to_one/test_convert_mult_to_molsysmt_MolSys.py
normative:
blocked_by: []
supersedes: []
---

# Selecting a composed trajectory must not index its reference

## What / How / Why

During #695's native Iterator integration, both reference/trajectory input orders
fail with h5py IndexError: trajectory position one is used to read a reference
provider with only position zero. The protected 363-case intermediate receiving
has 361 passes and these two failures. The input is the bundled one-structure
villin H5MSM inventory plus its twenty-structure DCD; both components describe
one molecular system, rather than independent systems to concatenate.

The shared converter already prunes off-axis structural attributes, but still
passes the global structure selection into its chosen base converter. Filtering
attribute contributions alone does not protect that base read or remove the
reference's already materialized series. This is a general conversion defect,
not a Viewer-specific issue or a scientific ring/interaction calculation.

## Correction and exclusions

The existing axis resolver still rejects two different multi-structure lengths.
Its pruning helper now returns off-axis counts to the conversion owner. A chosen
reference base reads at most its one representative (or all of a zero-structure
provider), not selected trajectory positions. A native result discards that
reference structure payload together before receiving the on-axis observations.
Stable inventory and system-level assembly metadata remain available. Existing
association reconciliation and selected conversion continue to own chemistry,
other structural observations, named analyses and units.

No coordinate matching, implicit reference broadcasting, new data model, unit
policy or public argument is introduced. The existing off-axis warning remains.
The earlier archived structure-axis report explains provider choice; this record
tracks the additional selected-base read missed by that original correction.

## Receiving

The public direct regression selects positions [11, 2, 11] from both input orders
and compares exact trajectory coordinates, missing reference-only labels/time,
and the single-state association. Neighboring native Iterator tests verify
nonconsecutive/repeated positions, shorter final chunks, caller-owned native
outputs, other observations and evaluated-empty coverage/state maps.

After the correction, all 535 affected builder/iterator/PDBQT/composite-conversion
cases pass without omissions. The broader clean source, registered science,
documentation and receiving gates remain separate until their results are
recorded. Supplemental #698 adds no original milestone weight or release authority.

Module 05 also incorrectly described the first provider as query precedence.
Its explanation and paired content contract now match the maintained eligible-
provider rule: among on-axis providers carrying a value, the last wins. A direct
query regression protects both orders, without allowing a reference to replace
its trajectory. Existing executed course cells and outputs remain unchanged.

## Matching counts are not correspondence

A private closeout probe on 14f6420e9 also reproduces a subtler error: a selected
one-structure trajectory chunk retains the off-axis reference's explicit
state link, or its evaluated-empty named analysis. Length-only reconciliation
does not detect that the observations belong to a different structure.

The shared converter now retires the reference association with its geometry.
Multiple chemical states acquire unknown trajectory links, including a selected
count of one. Off-axis reference analyses reject through StructuralInconsistencyError
until the caller supplies explicit structure correspondence. This preserves
the source instead of silently transporting or dropping scientific evidence.
Both provider orders and one/repeated structure selections are guarded. The
283-case association/composition receiving passes without omissions.

## Resolution — 2026-11-10

Selected composition no longer indexes an off-axis reference with trajectory positions. It retires reference observations and state links together and rejects named reference analyses without explicit correspondence, including coincident one-structure counts. Both provider orders, repeated/nonconsecutive structures and public Iterator callers are guarded.

Qualified final source: `cdf6e878ffa53ef045ee3c9c568efd61cf9dcb61`. The [combined owner receipt](../../../devtools/data/construction_native_owner_receiving_421_695_696_697_698_699_20261110.json) preserves the original failing controls, failed intermediate integration attempts, source identities and bounded resources. The predecessor native cohort passes 8,813 cases. Final receiving retains 8,955 passes and one failed unit-context test oracle in the expanded 8,956-case cohort; the 415-case corrected focused cohort passes with byte-identical product source. All 116 registered scientific cases/74 nodes, 76 public/native doctest examples, strict seven-notebook validation, ten inspected HTML pages, twenty-six actual Jupyter checks and twenty-four representative native Qt checks pass on the explicitly recorded cohorts.

This is guarded Linux/Python 3.14 source resolution, not clean installed, other-platform, human or exact-candidate acceptance. The supplemental fix adds no original milestone weight. Public delivery and owning issue closure use the repository closeout route after independent blob verification.
