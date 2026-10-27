(Cookbook_TPSA_Descriptors)=
# Exporting molecular TPSA

*Joining molecular descriptor values to source indices with explicit units.*

A descriptor table needs both chemical identity and the exact model variant.
Use a complete graph and request provenance. No molecular preparation occurs.

```python
import molsysmt as msm
from rdkit import Chem

molsys = msm.convert(Chem.MolFromSmiles('CCO.COC'), to_form='molsysmt.MolSys')
result = msm.physchem.get_tpsa(molsys, selection=[1, 0], return_report=True)
values = msm.pyunitwizard.get_value(result['tpsa'], to_unit='angstrom**2')
records = [
    {'molecule_index': int(index), 'tpsa_angstrom2': float(value)}
    for index, value in zip(result['report']['molecule_indices'], values)
]
```

Store the declared `angstrom**2` column unit, method, polar-element choice and
report with these records. The source atom membership uses a flat array plus
offsets and remains aligned with the selected molecule order. Repeated molecule
indices repeat rows; empty selections produce empty records. A unit conversion
for export does not change the model definition. The output is not a permeability
measurement or a geometric SASA table. Metadata alone has no area values; keep
the quantity and report together. No new persistence format is defined here.

:::{seealso}
:class: dropdown

- {ref}`Tutorial_Get_tpsa` for required chemistry, variants and units.
- {func}`molsysmt.physchem.get_sasa` for geometric solvent exposure.
:::
