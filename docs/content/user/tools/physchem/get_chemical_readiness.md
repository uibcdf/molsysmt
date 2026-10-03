(Tutorial_Chemical_Readiness)=
# Getting chemical readiness

*Inspecting available chemical fields before choosing a preparation operation.*

Use `msm.physchem.get_chemical_readiness()` to inspect one chemical state and
one structure, when coordinates exist. The experimental tool accepts supported
forms, including incomplete native systems. It returns a detached dictionary
and leaves the source unchanged. Missing information is reported rather than
filled with neutral charges or guessed bond orders.

:::{versionadded} 1.0.0
:::

:::{admonition} API documentation
:class: dropdown

{func}`molsysmt.physchem.get_chemical_readiness`
:::

## Inspecting stored chemistry

```python
import molsysmt as msm

molsys = msm.systems['caffeine']['caffeine.sdf']
report = msm.physchem.get_chemical_readiness(molsys)
assert report['fields']['formal_charge']['status'] == 'present'
assert len(report['explicit_hydrogen_atom_indices']) == 10
assert 'valence' in report['unassessed_checks']
```

:::{admonition} Demo Systems Catalog
:class: dropdown

See {ref}`user-foundations-entrance-demo-systems` for the bundled datasets.
:::

The report uses schema `molsysmt.chemical_readiness@1` and method
`stored_field_audit`. It contains source atom and bond indices, the resolved
state and structure indices, and software version. Fields cover chemical
element `atom_type`, atom IDs, isotope, formal charge, aromatic flags, radical
and hydrogen counts, stereo labels, bond IDs/types/orders, supported covalent
multiplicities and finite coordinates. Formal charge is expressed in elementary
charge units. Coordinate values in this report are booleans indicating finite
positions; the underlying lengths are read explicitly in nm through PyUnitWizard.

## Reading coverage and evidence

Every field has `indices`, `values`, `present_indices`, `missing_indices`,
`unsupported_indices`, `conflict_indices` and `origin` arrays. Unknown values
are `None`; source indices have dtype `int64`. The field summary has one of
these statuses:

| Status | Meaning |
| --- | --- |
| `present` | Every assessed entry has a stored, supported value without a detected conflict. |
| `partial` | Some entries are missing. |
| `missing` | Every assessed entry is missing. |
| `unsupported` | At least one stored entry is outside this audit's supported encoding. |
| `conflict` | At least one limited consistency check failed. |
| `empty` | The assessed index axis has no entries. |

Conflicts take precedence over unsupported values, which take precedence over
missing coverage. Inspect the individual index arrays to see coexisting findings.
Consistency checks identify repeated atom IDs, invalid/self/duplicate bond
endpoints and nonfinite coordinates. Repeated IDs flag ambiguous identity by
ID; atoms still retain their distinct source indices.

Stored bond `evidence` identifies declared `explicit` or `inferred`
relationships. Other origins are `unassessed`. Edge evidence does not establish
how an order, aromatic flag or atom property was assigned. The stored state
provenance index is retained as a pointer, without authenticating its content.

`covalent_multiplicity` accepts stored conventional orders 1, 2 and 3, or a
declared aromatic bond. Dative relationships are excluded from that field and
remain visible in `bond_type`. This does not validate valence or independently
perceive aromaticity. A missing or `unspecified` stereo label does not prove
that an atom or bond cannot have a stereochemical configuration.

## Selecting atoms and a structure

```python
report = msm.physchem.get_chemical_readiness(molsys, selection=[16, 14, 14])
assert report['atom_indices'].tolist() == [14, 16]
```

Selections are deduplicated and sorted by source index. The report includes
all bonds incident to selected atoms, including bonds to external atoms.
`connectivity['crossing_bond_indices']` identifies that boundary; a subset is
not treated as an isolated ligand. Connectivity integrity checks examine the
whole selected state's stored bond table, without constructing a pair matrix.
An empty atom selection returns typed empty arrays, including a `(0, 2)`
bonded-pair array. Stored connectivity completeness is reported as declared.

For multiple structures, choose one with `structure_indices=[index]`.
Repeated copies of that index are deduplicated; multiple distinct indices
raise. A topology or chemical-state input without structures is assessable,
with missing coordinates. Coordinate-only inputs are also assessable, with
missing chemical fields. Complementary items use the existing public
composition and selection rules. Rich atom selections use `syntax` as usual.

For H5MSM 0.5, numeric atom/structure selections load chemical layers and read
only the selected coordinate frame and atom rows. Combining independent layers
requires their declared identity atom-axis associations. Remap incompatible
layers first. Rich string selections use the general public selection machinery
and do not carry the same bounded-reading guarantee.

## Choosing a chemical state

The default `chemical_state='reference'` inspects the reference state.
`chemical_state=index` selects an explicit state. `chemical_state='structure'`
uses the chosen structure's state association, including the implicit sole-state
association where applicable. `None` means `'reference'`.

An ambiguous reference yields `chemical_state_status='ambiguous'`; an absent
structure association yields `'unassociated'`. Both leave state fields missing
instead of silently choosing the first state. A source without chemical states
reports `'unavailable'`. Invalid explicit state indices raise. Resolved reports
use `'resolved'` and retain the state index.

## Choosing what to do next

There is no universal `ready` flag. Review `unassessed_checks` and decide what
the next operation requires. Stored availability does not certify valence,
protonation, aromaticity, stereogenicity, conformer quality, a charge model or
docking readiness. Explicit H atoms are counted separately from stored virtual
and implicit H counts; those counts do not predict how many atoms to add.

A prepared PDBQT can be inspected without discarding its torsion tree, but its
partial graph and mechanical charges do not supply missing formal charges or
covalent multiplicities. Unsupported SDF encodings still raise the parser's
diagnostic; readiness inspection is not a parser fallback. Native inspection
needs neither RDKit nor Ackredit. Conversions from other forms retain their
existing dependency requirements.

:::{seealso}
:class: dropdown

**Related Tools & References**

- {ref}`cookbook-native-sdf` for inspecting an SDF before preparation.
- {ref}`Tutorial_Get_CIP_stereochemistry` for explicit stereochemical analysis.
:::
