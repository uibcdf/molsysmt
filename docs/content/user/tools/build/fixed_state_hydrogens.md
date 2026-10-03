(Tutorial_Fixed_State_Hydrogens)=
# Adding hydrogens to a fixed chemical state

*Materializing a prepared hydrogen inventory while preserving the source pose.*

Use {func}`molsysmt.build.add_missing_hydrogens` with
`mode='fixed_chemical_state'`, `pH=None` and `engine='RDKit'` when you have already
chosen the ligand's chemistry. This experimental mode returns a new native
`MolSys`, regardless of the supported input form. Set `return_report=True` to
receive `{'molecular_system': ..., 'report': ...}`. RDKit is optional and loaded
only when this engine is requested. An unavailable engine raises; no fallback runs.

:::{admonition} API documentation

- {func}`molsysmt.build.add_missing_hydrogens`
- {func}`molsysmt.physchem.get_hydrogen_inventory`
- {func}`molsysmt.build.add_terminal_atoms`
:::

:::{versionadded} 1.0.0
:::

## Choosing chemistry before geometry

Supply one isolated connected ligand, one chemical state and one finite coordinate
frame. Explicitly extract other states/frames first; selecting a frame alone does
not authorize their removal. Required assignments are element symbols (`atom_type`),
complete covalent connectivity, supported bond orders, atom/bond aromaticity,
formal charges, zero unpaired electrons and stored implicit/explicit H counts.
This slice supports H, C, N, O, F, P, S, Cl, Br and I. It rejects metals, radicals,
query chemistry and virtual isotopic additions. Existing isotopic atoms are retained.

The {ref}`inventory tool <Tutorial_Hydrogen_Inventory>` separates existing indexed
H atoms from virtual H annotations. Unknown counts are unresolved, not zero.
Sanitation that changes the inventory or declared chemistry causes an error.
Existing H are not removed or repositioned, including an excessive or conflicting
input that must instead be rejected. Absolute R/S and E/Z assignments, when
present, must agree with the supplied pose; unsupported descriptors need explicit
normalization before this operation.

## Requesting placement and reviewing the result

After preparing `molsys`, call:

```python
result = msm.build.add_missing_hydrogens(
    molsys, mode='fixed_chemical_state', pH=None, engine='RDKit',
    chemical_state='reference', structure_indices=[0], return_report=True,
)
molsys_with_h = result['molecular_system']
report = result['report']
```

The `molsysmt.hydrogen_addition@1` report retains the state/frame indices, state ID,
chemical readiness, per-parent inventory, generated IDs, original producer/engine
versions, method, parameters, references and portable scientific attribution.
`atom_correspondence` maps original to output indices, shape `(n_original_atoms, 2)`;
`parent_hydrogen_pairs` maps existing parents to appended H, shape `(n_added_H, 2)`.
The latter is empty with shape `(0, 2)` when no addition is needed.
The report's units are explicit; native coordinate storage is in nm.
Stored virtual H counts become zero after their atoms have been materialized.
Original atom indices, IDs, isotope assignments, memberships, coordinate values,
box, frame/state links and existing bond chemistry are retained on a detached copy.

This method is `local_hydrogen_placement`, provided by
[RDKit AddHs(addCoords=True)](https://www.rdkit.org/docs/source/rdkit.Chem.rdmolops.html#rdkit.Chem.rdmolops.AddHs).
Only the new coordinates come from that engine. Existing positions are copied
from the source rather than roundtripped through its angstrom protocol.

## Understanding validity and limits

This operation does not select pH, protomers, tautomers or heavy-atom conformers,
and does not optimize an energy or receptor-facing OH/NH orientation. H positions
are generated local geometry, not experimentally observed coordinates. Separate
refinement can be needed before a directional pharmacophore or docking analysis.

Supply an already compact periodic ligand. A bond requiring another periodic
image is rejected; reconstruct explicitly with `msm.pbc.wrap_to_mic()` first.
The source coordinates and box remain unchanged by H addition.

With `attribute_policy='intersection'`, unsupported atom-aligned attributes
(velocities, B-factors and occupancies), system observables and force-field
parameters are dropped with a diagnostic and named in the report. New values are
not fabricated. `attribute_policy='strict'` rejects such inputs. Sparse alternate
locations for old atoms remain attached to their unchanged indices.
Named interactions retain provenance but become **unevaluated** on an expanded
output: adding an H can change interactions even if the old coordinates did not
move. Recalculate explicitly. A zero-addition copy retains its analyses and
attributes. Failure leaves the source unchanged.

## Saving and retaining provenance

Save `molsys_with_h` using the public H5MSM 0.5 conversion. It preserves the
expanded chemical/coordinate domains and invalidated named analyses. Retain the
detached report separately; it is not implicitly attached or serialized as a
preparation-history layer. A state's provenance index is retained when supplied,
but it does not replace the caller's template/input provenance records.
The report contains NumPy arrays; convert those fields explicitly when using a
JSON writer rather than assuming the entire dictionary is directly serializable.

The existing default `mode='pH'`, `pH=7.4`, `engine='OpenMM'` retains the legacy
residue-oriented behavior. RDKit and report/state options require the explicit
fixed-state mode. Neither mode predicts environment-dependent pKa.

:::{seealso}

- {ref}`Tutorial_Chemical_Templates` — preparing assignments without adding atoms.
- {ref}`Cookbook_Applying_Chemical_Templates` — pinned EST preparation and checks.
- {ref}`Tutorial_Add_Terminal_Atoms` — attaching declared atoms without an engine.
:::
