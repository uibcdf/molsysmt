# Native interface contacts and SASA: molecular-owner contract

**Role:** normative, bounded molecular-operation contract under
uibcdf/molsysmt#734. **Reviewed:** 2026-11-12.
MolSysSuite #195 coordinates the shared review; BindingMT #112 owns its
binding profiles and TopoMT #197 owns optional topographic enrichment.

This contract supplies existing operations, checked facts and remaining caller
preconditions. It introduces no public API, scientific default, provider floor,
universal correspondence record or release prerequisite. BindingMT's composed
and installed receiving remains its own work.

## Admitted operation scope

The initial profile uses two resolved, unique, nonempty, disjoint atom
populations A and B, one explicit Cartesian structure and fixed coordinates.
The surface environment is exactly A union B. The caller admits the chemical
state, present hydrogen representation, element labels and finite positive
radii. It excludes inter-participant covalent links and unsupported coordinate
or chemical interpretation. This is a profile restriction, not a universal
restriction on MolSysMT's generic geometry tools.

No chemical completion, relaxation, capping, implicit reconstruction or
preparation is performed by these calculations. A wrapped structure must first
have an explicitly admitted coordinate treatment; `pbc=False` does not rebuild
whole molecules. Other environments, covalent interfaces, periodic surface
definitions and radius models require their own agreement.

## Contacts and distances

Use the same source and explicit endpoint/structure axes for both calls:

```python
contacts = msm.structure.get_contacts(
    molsys, selection=A, selection_2=B, structure_indices=[s],
    pairs=False, center_of_atoms=False, center_of_atoms_2=False,
    threshold=cutoff, pbc=False, output_type="pairs", output_indices="atom",
    use_gpu=False, cell_list=False, parallel=False, num_threads=1,
)
distances = msm.structure.get_distances(
    molsys, selection=A, selection_2=B, structure_indices=[s],
    pairs=False, center_of_atoms=False, center_of_atoms_2=False,
    pbc=False, use_gpu=False, parallel=False, num_threads=1,
)
```

`cutoff` is an explicitly chosen finite nonnegative length quantity.
`pairs=False` requests the Cartesian product. `pairs=True` instead compares
corresponding endpoints; it is independent of `output_type="pairs"`, which
only selects a representation. A dense result has shape `(1, len(A), len(B))`;
pair projection returns one list for the selected structure. Atom labels in
pair output are indices in that input system's atom axis, not atom IDs or
automatically original-source indices of a derived context.

The predicate includes equality: `distance <= cutoff`. The tested source
profile also distinguishes the immediately preceding representable cutoff.
No additional geometric tolerance is silently added. The public distance
quantity supplies values; the contact result alone is not a distance/provenance
receipt. Numeric endpoint lists preserve request order. Expressions normally
select in source order. Repeated delivery and unique physical membership are
different consumer concepts.

With source A `[8, 2]` at x `[0, 3]` and B `[30, 10]` at x `[3.5, 1]` nm,
the independent 1-nm control expects pairs `[[8, 10], [2, 30]]` and distances
`[[[3.5, 1], [0.5, 2]]]` nm. This is a synthetic control, not an application
cutoff recommendation. Corresponding-pair mode produces two false entries.
Moving B away gives a completed no-contact result `[[]]`; an empty required
participant is instead invalid for the BindingMT profile.

The Boolean map remains resident even for pair output. Its numerical budget
and output guards are described in [SCALABILITY](SCALABILITY.md). Large inputs
need bounded populations or a separately qualified public neighbor profile;
this contract does not make pair output streaming or add a search kernel.

## Source, local and structure correspondence

Native extraction retains ascending source atom order, not arbitrary requested
order. For the requested atoms `[8, 2, 30, 10]`,
`msm.extract(..., structure_indices=[2])` delivers source atoms
`[2, 8, 10, 30]` and one local structure 0 corresponding to source structure 2.
Retain those known operation maps explicitly.

For local input order `[8, 2, 30, 10]`, apply the complete local permutation
`[1, 0, 3, 2]` with `msm.permute_atoms(..., return_report=True)` after extraction.
Its atom-map report can be combined with the declared extraction map through
`msm.compose_atom_maps`. The public composition checks map schemas, counts and
inverse/available-label consistency. It does not authenticate that two arbitrary
assets represent the same molecule.

Source-sorted footprints `[2, 8]` and `[10, 30]` must retain aligned local
vectors `[1, 0]` and `[3, 2]`. Sorting the local vectors independently would
corrupt correspondence. Keep contributing pairs separately from each unique
footprint. IDs remain labels even when they contain numbers.

Native extraction/permutation retains chemical-state order and the declared
structure association. Query `structure_chemical_state_index` explicitly;
`chemical_state="structure"` with the chosen structure resolves the associated
assignments for a chemical query. Geometry tools have no separate chemical-state
argument and do not validate protonation or biological participant identity.
The source-to-local structure map and associated state remain part of the
consumer's context. Native component restriction/recomputation follows the
[existing extraction contract](forms_and_conversions.md); no chemical
preparation is implied by a subgraph projection.

## Surface contexts and actual radius resource

Construct independent A, B and A-union-B systems with `msm.extract` from the
same admitted source structure. Keep each output's known source/local maps.
Use identical coordinates, radius model, probe and sampling policy for all
three. Output selection alone retains every input occluder:

```python
options = dict(
    engine="MolSysMT", element="atom", structure_indices=[0], pbc=False,
    probe_radius="0.14 nm", n_sphere_points=960,
    use_gpu=False, use_cell_list=False, parallel=False, num_threads=1,
)
sasa_A = msm.physchem.get_sasa(molsys_A, **options)
sasa_B = msm.physchem.get_sasa(molsys_B, **options)
sasa_AB = msm.physchem.get_sasa(molsys_AB, **options)
```

Here local structure 0 must be explicitly mapped to the admitted source
structure. The example probe/sampling values identify the received analytical
controls; they do not select BindingMT's scientific defaults.

The native engine uses Rust Shrake–Rupley kernels and the bundled Fibonacci
sphere directions in `molsysmt/lib/structure/sphere_points.py`. It obtains
radii internally through `get_atomic_radius(..., definition="vdw")`, reading
`molsysmt/physchem/atoms/radius.py`, whose declared unit is nm. This is an
element-based table: `atom_type` is an element symbol, distinct from stored
force-field atom types. The resource fingerprint and inspected source are
retained in the receiving receipt. Checked public reference anchors are
H/C/N/O/Cl: `[0.110, 0.170, 0.155, 0.152, 0.175]` nm.

Resource identity and these anchors are not a new verification of every
historical table entry or every chemistry. Some elements have unavailable
entries; dummy types have zero excluded-volume radii. The admitted first profile
requires finite positive physical-atom radii and explicit supported chemistry.
Validate those prerequisites before calculation rather than interpreting missing
coverage as a numerical zero. `get_atomic_radius` returns its table quantity in
nm; SASA converts radii to its working length unit and standardizes output areas.

`get_sasa` has no arbitrary radius-array or ProtOr-selector argument.
`get_atomic_radius(definition="protor")` is a separate reader, not a switch
for this surface calculation. A different required radius model needs a concrete
owner-supported profile. No missing new operation is established for the first
bundled-vdW profile; #728's one-call ProtOr proposal remains separate.

## Losses, numerical meaning and quantities

Align atomic outputs through their known maps before subtracting:

```text
loss_A = SASA_A(A) - SASA_A(A union B)
loss_B = SASA_B(B) - SASA_B(A union B)
total_loss = sum(loss_A) + sum(loss_B)
mean_side_area = total_loss / 2
```

Both sides remain inspectable; equality is not assumed. The mean is an explicit
reporting convention, not another surface measurement. Atomic-to-group reduction
uses actual owner atom/group correspondence. Choosing a positive-loss membership
threshold is a BindingMT profile decision, distinct from a contact cutoff.

SASA returns an area quantity of shape `(n_structures, n_output_elements)` in
the square of the configured standard length unit. Use an explicit target unit
when retrieving values, and check area versus length dimensionality. The bounded
receiving uses nm/ps and pm/fs policies without modifying the application policy.
No portable result/quantity schema is introduced here.

For an isolated carbon with radius 0.17 nm and probe 0.14 nm, the independent
area is `4*pi*0.31**2` nm squared. A one-cap pair at separation 0.31 nm supplies
the spherical-cap loss oracle. The existing tolerance registry allows
0.0101 nm squared per atom at 960 points for its specified carbon fixtures;
sum two side errors for total loss. It is not a universal accuracy, convergence,
rigid-rotation or biological-interface tolerance. Additional geometries,
sampling densities and scientifically meaningful membership thresholds require
their own acceptance. Preserve unexpected negative losses for diagnosis rather
than concealing a context/model mismatch.

A separate two-sphere C/H control has inflated radii 0.31/0.25 nm at separation
0.31 nm. Independent spherical-cap geometry produces distinct side losses, so
doubling one side cannot satisfy that control. Its predeclared fixture budget
is eight maximum-radius sphere-patch areas at 960 points; this adds no universal
error bound or change to the existing equal-carbon tolerance registry.

`get_area_buried` is the Rose group-reference descriptor documented in angstrom
squared, not coordinate-dependent interface burial. `get_surface_area` is the
Collantes ISA lookup with a provisional quantity convention under #473, also
not geometric SASA. Neither replaces the three-context calculation above.

## Checked facts and caller preconditions

| Boundary | Facts supplied or checked | Still owned by the caller/profile |
| --- | --- | --- |
| Geometry | Requested coordinate axes, finite/nonnegative contact cutoff, all-cross versus corresponding pairs, inclusive membership and output labels | Resolved unique/nonempty/disjoint participants, intended source identity and coordinate treatment |
| Declared maps | Known extraction/permutation order, inverse atom maps and explicit structure 2 to local 0; stored assignments and associations survive the received projection | Association of foreign assets, complete participant chemistry, absent inter-participant covalent links and applicability after later edits |
| Native SASA | Actual bundled radius route, fixed-input occlusion, typed areas and selected-output behavior | Admitted element/radius/hydrogen model, environment, probe/density and scientific acceptance |
| Evidence | Actual provider/source/native/runtime identity and tested examples | BindingMT result/outcome/footprint persistence, current-use checks, interpretation and installed receiving |

The synthetic state/bond assignments test transport, not chemically realistic
valences or a biological interface. The received numerical profile is Cartesian
native CPU; periodic, GPU and alternate engine/profile acceptance remain separate.
MDTraj batch-SASA recovery stays under #530. Public arrays/lists are not detached
scientific receipts. The consumer records actual method, parameters, resource,
units, source/state/maps and producer identity. Existing method references and
optional Ackredit client rules apply only to calculations actually performed;
this review qualifies no new attribution or PISA execution.

## Evidence and disposition

[The source receipt](../devtools/data/native_interface_handoff_receiving_734_20261112.json)
owns exact code/native/runtime identities, selected controls, original test-draft
and launcher failures, resource limits and public delivery. The primary contact,
distance, SASA and radius files match inspected `ff25f120` on the reviewed
`501e02b40` source; later changes need fresh scope review.

Meaningful guards are
`tests/structure/get_contacts/test_native_interface_handoff.py` and
`tests/physchem/get_sasa/test_native_interface_handoff.py`. Reused cutoff/unit,
analytic-sphere, native permutation/state and actual course/example controls
are named in the receipt. The finite provider review is sufficient to offer the
existing operations for the restricted first profile. BindingMT still chooses
and accepts its application profile and performs actual composed/saved/installed
receiving; MolSysSuite #195 remains partial until its owning agreements arrive.
