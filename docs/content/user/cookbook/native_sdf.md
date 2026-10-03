(cookbook-native-sdf)=
# Reading and writing native SDF

*Exchanging explicit small-molecule chemistry without installing RDKit.*

You can read a single V2000 or V3000 SDF record into native domains and write
one selected structure back to SDF. This experimental adapter retains source
hydrogens and explicit chemistry. It does not prepare a ligand for docking.

## Reading a molecule

```python
import molsysmt as msm

source = msm.systems['caffeine']['caffeine.sdf']
molsys = msm.convert(source, to_form='molsysmt.MolSys')
assert molsys.topology.n_atoms == 24
assert molsys.topology.n_bonds == 25
```

The ten source hydrogens remain atoms. Formal charges and bond orders belong
to `chemical_states`; coordinates belong to `structures`. SDF declares
coordinates in angstroms. Native structures store nanometers, and writing
converts explicitly back to angstroms regardless of your unit policy.

## Writing and selecting

```python
msm.convert(molsys, to_form='caffeine.sdf', ctfile_version='V3000')
msm.convert(molsys, selection=[0, 2, 4], to_form='selected.sdf')
```

With multiple structures, select exactly one using `structure_indices=[index]`.
Without that selection, output fails. MolSys extraction with topology orders
selected atoms by ascending source index; connectivity and coordinates use the
same map. Output atom/bond serials are newly assigned sequential integers;
they are read back as string IDs. V2000 writes four decimal places in coordinate
fields and supports at most 999 atoms or bonds. Use V3000 for larger tables.

## Preserving coordination

V3000 coordination bonds (type 9) become `bond_type='dative'`. The adapter uses
the first source endpoint as `bond_donor_atom_index` and the second as
`bond_acceptor_atom_index`, matching the RDKit endpoint convention. This preserves
declared orientation; it does not determine whether the atoms are suitable
electronic donors or acceptors. Dative bonds do not merge native covalent
components. Reading does not invent a covalent multiplicity for type 9.

Writing these relationships requires `ctfile_version='V3000'` and explicit
donor/acceptor indices. It follows those roles even if the native table sorts
the endpoints in the opposite order. Native numeric dative orders and custom
component-joining assignments cannot be encoded; conversion reports identify
their loss and strict mode rejects it. `DISP=COORD` and `DISP=DATIVE` source
drawing styles are accepted but lost on native conversion, which reports the
loss. Byte-preserving source copies retain them.

## Inspecting information loss

```python
report = msm.get_conversion_report(molsys, to_form='caffeine_report.sdf')
assert report.to_form == 'file:sdf'
# The report query does not create caffeine_report.sdf.
print(report.outcome, report.is_exhaustive)

output, report = msm.convert(molsys, to_form='caffeine_report.sdf',
                             return_report=True)
print(report.outcome, report.is_exhaustive)
```

SDF cannot retain arbitrary native IDs/names, residue/chain hierarchy, partial
charges, force-field parameters, interaction analyses or extra structural
fields. Reports check chemical capabilities and selected native losses, but
cross-form audits are not exhaustive. `strict=True` rejects detected losses
before writing.

If your source has SD property blocks, ordinary native conversion raises an
error because MolSys has no general storage for them yet. You can explicitly
authorize their loss with `discard_properties=True`; `return_report=True`
lists that loss, and strict mode still rejects it. To preserve source bytes and
properties, use `msm.copy(source, output_filename='source_copy.sdf')`.

An unselected SDF-to-SDF conversion (`selection='all'` and
`structure_indices='all'`) or file copy validates only the single-record
envelope: header/count fields, `M  END` and `$$$$`. It preserves the original
bytes even when their chemistry or legacy version marker is outside the
native parser profile. For this identity operation, `strict=True` and an
exhaustive `exact` report certify byte preservation, not chemical validity
or docking readiness. Native conversion, attribute queries and selected
copies still require supported chemical interpretation. Multiple records
and malformed envelopes remain errors before the destination is opened.

## Enabling stereochemistry explicitly

Ordinary parsing remains native and rejects active stereo flags. To interpret
tetrahedral and double-bond configurations, explicitly request the optional
RDKit provider. All source hydrogen atoms remain on the same atom axis:

```python
molsys = msm.convert('stereo.sdf', to_form='molsysmt.MolSys',
                     stereo_engine='rdkit')
msm.convert(molsys, to_form='stereo_out.sdf', ctfile_version='V3000',
            stereo_engine='rdkit')
```

Assignment is performed on the full graph before atom extraction. Absolute
atom labels are stored in `chemical_states`; double bonds retain the relative
cis/trans relation and explicit reference atoms. Use
{ref}`Tutorial_Get_CIP_stereochemistry` to query absolute E/Z independently.
Writing verifies the encoded configuration by reading the payload back before
opening the destination. Incompatible geometry or unencodable labels raise
instead of overwriting the file. Byte-preserving identity copies need no stereo
provider. Converter options are not validated by the public preflight report.
Native subset extraction can invalidate a center's chemical configuration;
requesting serialization does not repair or guess the missing chemistry.

## Checking chemical atom types

You can check extracted atom types independently of their source form. Atom
types are chemical element symbols, distinct from atom names and force-field
types. Normalization preserves unspecified isotopes and recognizes the source
hydrogen aliases `D` and `T`:

```python
atom_types = msm.get(molsys, element='atom', atom_type=True)
assert msm.element.atom.is_atom_type(atom_types).all()
assert msm.element.atom.normalize_atom_types(['D', 'T', 'C']) == (
    ['H', 'H', 'C'], [2, 3, None]
)
```

The SDF reader uses the same explicit-symbol normalization internally. It
does not infer elements from atom names or AutoDock labels. The public tools
inspect values; they do not modify `molsys`.

:::{warning}
The default native subset rejects active stereo flags/labels. The explicitly
enabled provider interprets supported tetrahedral and double-bond encodings,
including wedges and supported 3D source configurations. Both routes reject
query atoms/bonds,
valence overrides, reaction maps, Sgroups and unsupported radical/bond types.
Explicit V3000 flags with their documented inactive value of zero are accepted;
an unknown field with value zero is still an error. Coordination type 9 is
supported only in V3000, not as a nonstandard V2000 extension.
Writing rejects atom aromaticity that the supplied bond types cannot retain.
It does not sanitize valence, infer hydrogen counts, perceive aromaticity from
Kekule bonds or derive CIP labels from 3D coordinates by default. The optional provider
performs the requested CIP analysis; enhanced stereo and parity-only encodings
without a supported wedge/3D interpretation remain unsupported. Multiple SDF records
are rejected. Keep the original file when it carries unsupported information.
:::

:::{seealso}
:class: dropdown

- {func}`molsysmt.basic.convert` for form conversion and reports.
- {ref}`Tutorial_Get_Conversion_Report` for a query without destination writes.
- {ref}`Tutorial_Atom_Types` for chemical elements and isotope aliases.
- {func}`molsysmt.basic.get` for form-independent attribute queries.
- {ref}`user-foundations-support-forms-files` for supported file forms.
:::
