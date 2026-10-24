---
summary: Minimum distances reuse first-population weights for the second center.
issue: uibcdf/molsysmt#444
status: resolved
opened: 2026-10-24
closed: 2026-10-24
severity: medium
verification: reproduced
area: [structure, weights]
guard: tests/structure/test_distance_family_contract.py
normative: docs/content/user/tools/structure/distance_family.md
blocked_by: []
supersedes: []
---

# Minimum distances reuse first-population weights for the second center.

**Reported:** 2026-10-24 during addon receiving under uibcdf/molsysmt#421 /
uibcdf/molsysviewer#264. Filing explicitly authorized by the maintainer.
**Initial status:** open. The MolSysMT scientific team owns the correction; Viewer keeps
this new wrapper pending rather than altering native parameters or formulas.


## What

Independent second-population weights are accepted but ignored in the minimum
center distance. Native values for the reproduction are
[0.6595507508555509, 0.5834060321652554, 0.6595507508555509] nm. Independent
weighted centroids give [0.7720171238073741, 0.674794639416701,
0.7720171238073741] nm.

```python
import molsysmt as msm
molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'],
                     structure_indices=[0, 8, 3])
indices, distances = msm.structure.get_minimum_distances(
    molsys, selection=[0, 2], selection_2=[10, 25],
    structure_indices=[2, 0, 2], center_of_atoms=True,
    center_of_atoms_2=True, weights=[1., 1.], weights_2=[1., 3.], pbc=False,
)
```

## How

[get_minimum_distances.py](../../../molsysmt/structure/get_minimum_distances.py)
passes weights_2=weights to get_distances. This replaces the caller's second
weights rather than forwarding them. Independent NumPy average calculations on
both coordinate populations expose the wrong second centroid.

## Why

Different populations can intentionally use different weights, including masses
or numeric weighting. Silently changing one endpoint changes the scientific
observable. Different population sizes may expose a validation error instead of
a wrong value; both outcomes need coverage.

## What was refuted

The reproduction uses the same source and explicit structures in both calculations,
with PBC disabled and values converted to nm. It imports no Viewer. The maximum
helper forwards its second weights independently in the reviewed source.

## Acceptance criteria

Correct the native forwarding and guard actual scientific values, source indices,
independent endpoint weights/domains and unchanged caller inputs. The maintainer
explicitly requests a pytest contract matrix covering get_distances, get_neighbors,
get_minimum_distances and get_maximum_distances: native forms/H5MSM, population
sizes/order, two sources, repeated/nonconsecutive structures, PBC/units, eager/
heavy paths, supported output metadata, empties/errors and selection/weight
combinations. Use independent references, not only parity with a shared defective
implementation. The detailed request is in the owning issue comments and applies
to both uibcdf/molsysmt#444 and uibcdf/molsysmt#445.

## Scope and exclusions

No addon algorithm, scientific fix or hidden route/parameter substitution is
introduced here. Closed #441 repaired chunked scalar endpoint populations;
this report records a separate wrapper-level scientific delegation defect.
Existing artifact coordinates and publication pauses remain unchanged.

## Provenance

Observed on Linux, Python 3.14.7 in molsyssuite@uibcdf_3.14, source
bc21428312b6945c9c8926611721713c5ca3fbd2. Bundled pentalanine's H5MSM 0.4
warning is retained. This is source evidence, not installed-artifact qualification.


## Resolution and qualification — 2026-10-24

The maintainer-authorized review fixes the provider implementation and keeps
consumer receiving and release qualification separate. The final combined
selection passes **686 Python tests in 23.77 s**, using pytest-receptor and
12 workers, with zero failures or skips. It covers all five distance-family
functions, common weighted geometry and native sequence/alignment codecs.
The two new guard modules contribute 486 parametrized cases: 444 for the
five scientific tools and 42 for sequence codecs. They include independent
second-center models over an inherited atom population.
The unrelated marked AlphaFold network alignment is excluded explicitly;
the existing real PDB 5XJH neighbor regression passes with network access.
The 75 recorded warnings are legacy H5MSM reads, deliberately small-budget
memory-pressure warnings and unavailable-GPU selector fallbacks. None is
silently converted into actual GPU qualification.

Six public docstring doctests and ten Rust neighbor unit tests pass. The
extension is rebuilt in the existing development environment without new
dependencies. Both new guide/recipe pages' Python examples execute. Common
Core modules 13 and 16 and the five existing structural tutorials are forced
through fresh execution; all seven pass. Their frozen examples/plots remain.
Full-repository Ruff lint/format, signature/docstring checks and fourteen fast
release checks pass. Hosted exact-source checks are recorded at issue closure;
none of this qualifies a new installed artifact or authorizes publication.

### Family repairs and reusable owners

Minimum distances forward independent second-endpoint weights. Extrema share a
private slab reducer, assigning every local index and retiring internally owned
disk handles, including errors. The missing per-target minimum indices are now
assigned. Numeric weight shape validation remains in the common weighted-
geometry owner; grouped weight flattening remains in the grouping consumer.

Neighbors forward the second molecular source and infer self identity only for
an implicit same-source population. They exclude physical self entries rather
than dropping the first zero distance, retaining distinct coincident atoms.
Both scalar and Rust cell-list routes break distance ties by local target index.
Paired row sorting preserves query/target roles. Unsupported flags/formats reject;
zero counts, empty populations and count limits have explicit contracts.

Dictionary distances encode positionally paired structure lists without
manufacturing a structure Cartesian product or overwriting earlier secondary
observations of a repeated primary structure. Eager and chunked distances reject
incompatible structure lengths before the Rust kernel. Periodic-box validation
reuses the periodic owner; no second chemical or coordinate store is introduced.

Contacts resolve the second structure list using an explicit None test, retain
it when the atom population is implicit, and derive atom labels from resolved
selections. Dense self maps include their diagonal; only an implicit same-
structure self pair list uses the upper triangle. Explicit structure endpoints
retain all directed entries. Empty maps/pair lists have defined shapes, and
resident boolean output has a numeric budget guard. CPU distance intermediates
are retired. Coordinate preparation still uses RAM; this is not an out-of-core
contact-map implementation.

### Contract-to-test inventory

All new scientific comparisons use literal coordinates or independent NumPy
centroids, norms, reductions and finite lattice-image enumeration. Source
parity supplements those references rather than replacing them.

| Contract / route | Guard examples |
| --- | --- |
| Native MolSys, Structures and H5MSM; population order, repeats and unequal sizes | test_flat_populations_and_structure_axes |
| Independent systems with unequal atom/structure inventories | test_two_native_sources_can_have_different_atom_and_structure_inventories |
| Distinct weights, mixed raw/center endpoints, zero individual weights | test_independent_weighted_centers; test_endpoint_parameters_remain_independent_for_mixed_centers |
| Nested groups, masses and invalid weight shape/sum/sign/finiteness | test_nested_centers_and_masses; test_invalid_center_weights |
| Min/max indices, all supported entity flags, paired reductions and ties | test_extrema_indices_values_and_first_occurrence_ties |
| Nearest count, threshold, self/coincident identity, count bounds and repeats | test_neighbor_membership_indices_units_and_routes; test_repeated_self_selection_excludes_physical_self_occurrences |
| Raw/atom-labeled pairs, mutual/unique filters and directed roles | test_pair_filters_preserve_directed_endpoint_roles; test_unsupported_neighbor_combinations_reject |
| Contact Cartesian/paired maps, independent structures, atom labels and empties | test_contact_maps_keep_both_structure_axes; test_contact_pair_indices_preserve_selected_atom_roles |
| Inclusive zero/nonzero cutoffs and invalid values | test_contact_cutoff_is_inclusive_and_self_map_contains_diagonal; test_neighbor_threshold_must_be_finite_and_nonnegative |
| Orthogonal/triclinic MIC, missing/singular boxes and application units | test_flat_populations_and_structure_axes; test_application_units_preserve_physical_magnitudes |
| Structured output and repeated structure-pair labels | test_dictionary_values_keep_positional_second_structure_correspondence |
| Eager/auto/forced scalar chunks, distinct secondary blocks and persistent units | tests/structure/get_distances/test_heavy_endpoints.py |
| Numeric output budgets, internal file retirement and unsupported disk dictionary | test_automatic_disk_distance_intermediates_are_retired; test_contact_output_budget_and_disk_intermediate_lifecycle |
| Shape-defined empty axes and errors for undefined extrema | test_empty_distance_axes_have_defined_shapes; test_empty_extremum_is_an_explicit_error |

### Coverage limits

The CPU MolSysMT/Rust routes are qualified by this bounded matrix and the
existing regression selection. Actual GPU kernels are not qualified; the
unavailable selectors exercise CPU fallback only. Centers use supplied positions,
so wrapped participants must be made whole before physical center-based periodic
interpretation. get_contacts does not gain a molecular_system_2 argument.
Neighbor CSR covers the supported flat-atom threshold route; unsupported
combinations remain explicit errors. Resident outputs and coordinate workspace
are not a process-RSS cap. No large-scale performance claim follows from these
small deterministic scientific fixtures. The tests now run in the ordinary
source smoke and matching local tier, as well as the full suite.
