(Cookbook_Export_Secondary_Structure_Propensities)=
# Exporting reference propensities

*Joining explicit reference categories to selected source group indices.*

Create named columns for downstream descriptors without confusing reference
propensities with observed secondary structure. The recipe uses a topology and
needs no coordinates. Select standard amino-acid groups explicitly because the
bundled peptide's terminal caps have no reference value.

```python
import molsysmt as msm

molsys = msm.convert(
    msm.systems['pentalanine']['traj_pentalanine.h5msm'],
    to_form='molsysmt.Topology',
)
group_indices = [1, 3, 5]
names = msm.get(molsys, element='group', selection=group_indices, group_name=True)
categories = ['alpha_helix', 'beta_sheet', 'reverse_turn']
columns = {
    category: msm.physchem.get_secondary_structure_propensity(
        molsys, category, selection=group_indices,
        definition='levitt_1978_weighted',
    )
    for category in categories
}
records = [
    dict(group_index=index, group_name=name,
         **{category: float(columns[category][row]) for category in categories})
    for row, (index, name) in enumerate(zip(group_indices, names))
]
```

Each record retains the selected source group index. Store the definition
`levitt_1978_weighted`, category names and dimensionless frequency-ratio meaning
alongside exported columns. Values may exceed one and the three columns do not
sum to one. Do not treat their argmax as a validated secondary-structure
prediction, or sum these values as a molecular observable. An empty selection
yields empty columns and records. No automatic modified-group mapping is used.

:::{admonition} Related tools
:class: dropdown seealso

- {ref}`Tutorial_Get_secondary_structure_propensity` for the source and strict scope.
- {func}`molsysmt.basic.get` for matching source identities.
- {func}`molsysmt.structure.get_secondary_structure` for observed assignments.
:::
