(Tutorial_Partial_Charge_Assignment)=
# Getting partial charges

*Calculating a named charge model without changing molecular chemistry.*

The experimental {func}`molsysmt.physchem.get_partial_charges` calculates on
the full selected chemical state and returns a unitful array. A selection
filters that array after calculation; it never caps or parameterizes a fragment
in isolation. To attach a validated full-atom assignment to a detached native
system, use {func}`molsysmt.build.assign_partial_charges`.

:::{versionadded} 1.0.0
:::

:::{admonition} API documentation
:class: dropdown

{func}`molsysmt.physchem.get_partial_charges`
{func}`molsysmt.build.assign_partial_charges`
:::

## Choosing a model

| Method | Required provider | Bounded scientific contract |
| --- | --- | --- |
| `gasteiger_marsili` | RDKit | Twelve iterations of partial equalization on a complete closed-shell organic graph; all H must be indexed atoms. |
| `forcefield` | OpenMM | Read matched force-field template charges on the unchanged atom inventory; name the force field explicitly. |

There is no default method, automatic provider fallback or zero placeholder.
Supported forms supply the necessary information through existing converters;
incomplete chemistry fails explicitly. RDKit sanitation perceives valence and
aromaticity on a detached graph; known conflicting atom aromaticity is rejected.
Neither method uses coordinates to obtain its charges.

Gasteiger-Marsili is the [1980 electronegativity equalization method](https://doi.org/10.1016/0040-4020(80)80168-2),
implemented here with RDKit's `ComputeGasteigerCharges` and
`throwOnParamFailure=True`. The initial domain comprises H/C/N/O/F/P/S/Cl/Br/I.
Metals, radicals, dummy/query atoms, missing formal charges, unsupported bond
orders and partial connectivity are rejected. There is no selenium substitution,
metal removal or hydrogen-charge merging. If the backend finds virtual H,
materialize the declared inventory explicitly first; see
{ref}`Tutorial_Fixed_State_Hydrogens`.

Force-field assignment does not add hydrogens, choose protonation, repair residues
or create ligand templates. Unmatched templates and extra particles/virtual sites
fail. AMBER14 is tested on bundled alanine and villin protein inputs, separately
from small-molecule Gasteiger tests. That evidence does not cover every receptor,
every force field accepted by the resolver, or arbitrary ligands. Matched template
names and source parameter files are retained; protein ff14SB attribution refers
to the parameter set, not to a newly invented charge formula.

## Calculating and inspecting

```python
import molsysmt as msm

molsys = msm.systems['caffeine']['caffeine.sdf']
result = msm.physchem.get_partial_charges(
    molsys, method='gasteiger_marsili', return_report=True)
assert result['partial_charge'].shape == (24,)
assert result['report']['coverage'] == 'complete'
assert abs(result['report']['total_charge']) < 1e-6
```

:::{admonition} Demo Systems Catalog
:class: dropdown

See {ref}`user-foundations-entrance-demo-systems` for the bundled datasets.
:::

The report uses `molsysmt.partial_charge_assignment@1`. It records source atom
indices, the full evaluated atom inventory, state index and state ID, method,
parameters, original software versions, evidence and detached references.
`coverage='complete'` describes the full calculation, including when the requested
output has fewer atoms or is empty. Numeric report totals use elementary charge;
the returned quantity follows the current PyUnitWizard charge-unit policy.

The getter requires a configured standard for charge. If your policy contains only
length and time (for example, `['pm', 'fs']`), it raises `NoStandardsError` rather
than choosing a charge unit for you. Add a charge standard to request quantities,
for example `['pm', 'fs', 'coulomb']`. Native `assign_partial_charges` stores fixed
elementary-charge numbers and works with either policy, without changing it.

The full calculated total must agree within **1e-6 e** with complete stored formal
charges or an explicit `expected_total_charge`. A declaration must also agree with
complete known formal charges. An integer denotes elementary charge; a scalar
quantity can use any charge unit. An unlabelled float is rejected. If the formal
inventory is unknown, supply the total explicitly instead of assuming zero.
Failed coverage, nonfinite values and a total mismatch raise; no renormalization
is applied. Conservation is not a measure of electrostatic accuracy.

```python
subset = msm.physchem.get_partial_charges(
    molsys, method='gasteiger_marsili', selection=[14, 16, 14], return_report=True)
assert subset['report']['atom_indices'].tolist() == [14, 16]
```

Numeric result selections are sorted and deduplicated. Rich selection syntax uses
the source system. `chemical_state='structure'` requires an unambiguous state
association for the requested structures. Charges describe a chemical state, rather
than one observation per structure; changing coordinates does not change these models.

## Storing and exporting

`assign_partial_charges` returns a new native MolSys, keeping all source atoms,
IDs, structures, chemical assignments and named analyses. Mechanical storage
holds one assignment, so this attachment route requires exactly one chemical
state. Use detached calculation results for multi-state inputs. Charges are stored
in `molsys.molecular_mechanics.partial_charge`, as native elementary-charge values,
with `partial_charge_assignment` provenance. This does not assign AutoDock types or
establish that the remaining mechanical parameters match that charge model.
Named analyses retain their original snapshots; analyses depending on changed
mechanical parameters require explicit invalidation/recalculation by the caller.
Native automatic coupling covers geometry and ChemicalStates edits.

Attachment converts and copies the complete native system, including coordinates;
it can materialize a large trajectory. It is not a streaming assignment API.
Detached calculation with numeric atom selections reads H5MSM chemical domains
without loading coordinates. Rich spatial selections use the original system's
coordinates and can require full loading.

Native copies and pickle restoration retain original versions. Atom extraction
preserves retained charge values and their source index map, with `status='projected'`:
it does not recalculate isolated fragments or enforce their isolated formal-charge
total. The original full-system total and scope remain in the report. Joining
separate parameterized systems requires a new joint assignment: strict joins reject
loss of original attribution; intersection joins retain the mechanical values and
clear incompatible attribution with a diagnostic.

Before using a stored assignment, the PDBQT writer checks its bound chemical graph,
ordered values and associated frame state. A raw chemistry or charge edit makes
that check fail. Ordinary coordinate movement preserves graph-based charges.
Explicit replacement through `msm.set(..., partial_charge=...)` or the native
charge property clears the original model attribution; it is a manual assignment.
Raw DataFrame edits bypass that clearing but cannot pass the writer's digest check.
These checks are conservative consistency checks, not authentication.

PDBQT writes a `REMARK MOLSYSMT_PARTIAL_CHARGES` JSON summary for a named assignment,
including producer versions, full source coverage, written atom count, model
parameters and the total before three-decimal export rounding. It retains all H;
no charge redistribution runs. Remarks are available as source text, but native
PDBQT conversion does not restore the full assignment report or chemical graph.
Keep the report separately and inspect conversion losses.

MolecularMechanics remains experimental and is excluded from **H5MSM 0.5**;
its persistence belongs to the planned 0.6 work. Do not describe a 0.5 save as a
charge/provenance round trip. Optional Ackredit failures preserve calculated charges
and detached references, including under strict warning filters.

:::{seealso}
:class: dropdown

- {ref}`cookbook-assigning-partial-charges`
- {ref}`Tutorial_Chemical_Readiness`
- {ref}`cookbook-native-pdbqt`
:::
