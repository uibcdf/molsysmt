(cookbook-assigning-partial-charges)=
# Assigning charges before a bounded export

*Calculating and retaining a named mechanical charge assignment on prepared chemistry.*

:::{versionadded} 1.0.0
:::

## Calculating a prepared ligand

The bundled caffeine SDF already includes all indexed hydrogens and full
covalent orders. This recipe neither adds hydrogens nor changes protonation.

```python
import molsysmt as msm

molsys = msm.build.assign_partial_charges(
    msm.systems['caffeine']['caffeine.sdf'], method='gasteiger_marsili')
report = molsys.molecular_mechanics.partial_charge_assignment
assert report['coverage'] == 'complete'
assert report['parameters']['iterations'] == 12
assert abs(report['total_charge']) < report['total_charge_tolerance']
```

:::{admonition} Demo Systems Catalog
:class: dropdown

See {ref}`user-foundations-entrance-demo-systems` for the bundled datasets.
:::

The native partial-charge array uses elementary charge. Formal charges remain
in ChemicalStates; the total check does not establish electrostatic accuracy.
Save the report with the result for provenance. H5MSM 0.5 does not persist the
experimental mechanical domain; full mechanical persistence is planned for 0.6.

## Querying a subset

```python
selected = msm.physchem.get_partial_charges(
    molsys, method='gasteiger_marsili', selection=[14, 16], return_report=True)
assert selected['report']['atom_indices'].tolist() == [14, 16]
assert selected['report']['n_atoms'] == 24
```

The full graph is calculated before filtering. Extraction instead retains
the previous numerical charges as a projection, with original source indices.
Neither operation treats a fragment as a newly parameterized isolated molecule.

## Checking a receptor

For an already hydrogenated conventional protein, choose an explicit force field
and declare the expected total if formal charges are absent:

```python
receptor = msm.build.assign_partial_charges(
    msm.systems['chicken villin HP35']['1vii.pdb'], method='forcefield',
    forcefield='AMBER14', expected_total_charge=2)
assert receptor.molecular_mechanics.partial_charge_assignment['coverage'] == 'complete'
```

The +2 e declaration applies to this bundled structure and its supplied H inventory;
it is not a default for another receptor. Model/template matching fails clearly
for unsupported or unprepared chemistry. The calculator does not generate H,
repair residues or substitute a ligand charge scheme for receptor parameters.

Before PDBQT export, independently assign chemically valid AutoDock labels and
choose an explicit torsion tree where required. Charges alone do not establish
docking readiness. The writer checks stored assignment consistency and records
a compact provenance remark plus its three-decimal charge rounding. Reading
the resulting PDBQT does not recover the full chemical state or assignment report.

:::{seealso}
:class: dropdown

- {ref}`Tutorial_Partial_Charge_Assignment`
- {ref}`Tutorial_Assign_Partial_Charges`
- {ref}`Tutorial_Chemical_Readiness`
- {ref}`cookbook-native-pdbqt`
:::
