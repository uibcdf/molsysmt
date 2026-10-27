(Cookbook_Molecular_Descriptors)=
# Exporting paired molecular descriptors

*Joining polar surface descriptors and lipophilicity scores to source molecules.*

You can build a ligand descriptor table while retaining the exact molecular
state. Here both tools examine the same complete molecules in the same order.
TPSA has area units; the Wildman–Crippen score is dimensionless.

```python
import molsysmt as msm
from rdkit import Chem

molsys = msm.convert(Chem.MolFromSmiles('CCO.c1ccccc1'), to_form='molsysmt.MolSys')
selection = [1, 0]
polar = msm.physchem.get_tpsa(molsys, selection=selection, return_report=True)
lipophilic = msm.physchem.get_lipophilicity(
    molsys, selection=selection, return_report=True,
)
area_values = msm.pyunitwizard.get_value(polar['tpsa'], to_unit='angstrom**2')
records = [
    {'molecule_index': int(index), 'tpsa_angstrom2': float(area),
     'wildman_crippen_score': float(score)}
    for index, area, score in zip(
        polar['report']['molecule_indices'], area_values,
        lipophilic['lipophilicity'],
    )
]
```

Retain both original reports with the table and its declared column units. The
reports identify source atom membership, state/digest, model options, producer
versions and original scientific references. Repeated selections repeat rows;
empty selections produce an empty table. No JSON/H5MSM report codec or automatic
analysis attachment is defined by this recipe. A saved report alone lacks the
corresponding values, so keep each result/report pair together.

Do not neutralize or sum molecules to make a score look like a physical logP.
For charged graphs the returned number remains the supplied-state model score,
with no pH-dependent logD or experimental accuracy guarantee. These descriptors
also do not measure a conformation's solvent exposure or predict permeability.

:::{seealso}
:class: dropdown

- {ref}`Tutorial_Get_tpsa` for polar-element scope and required chemistry.
- {ref}`Tutorial_Get_lipophilicity` for charged sites and provenance.
:::
