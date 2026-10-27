(Cookbook_Export_Bulkiness)=
# Exporting reference bulkiness

*Preserving group indices and descriptor units when preparing model features.*

A modeling table needs both the selected source indices and an explicit numerical
scale. {func}`molsysmt.physchem.get_bulkiness` returns area quantities; request
angstrom² explicitly when your model expects the historical Zimmerman numbers.
This reference lookup requires group names, not coordinates.

:::{versionadded} 1.0.0
:::

```python
import molsysmt as msm

molsys = msm.convert(
    msm.systems['pentalanine']['traj_pentalanine.h5msm'],
    to_form='molsysmt.Topology',
)
group_indices = [1, 3, 1]
area = msm.physchem.get_bulkiness(molsys, selection=group_indices)
values = msm.pyunitwizard.get_value(area, to_unit='angstrom**2')
records = [
    {'group_index': index, 'bulkiness_angstrom2': float(value)}
    for index, value in zip(group_indices, values)
]
assert [row['group_index'] for row in records] == [1, 3, 1]
```

The repeated group is intentional and remains repeated. Select only groups with
reference entries: terminal caps, modified names and DUM/X raise rather than
receiving a guessed parent or zero. If you want a peptide average, reduce the
area quantities explicitly with the intended weights. Summing the reference
values does not calculate a molecular surface. Preserve full floating precision
for computation; round only your displayed report.

The descriptor's area interpretation follows Proust et al. (2019), Table 1;
original 1968 derivation/normalization remains unaudited. Numeric agreement with
AAindex/ProtScale is a bounded curation check. The reader is experimental and
its scientific evidence classification is partial. Optional Ackredit records
references without claiming to execute the original generation procedure.

:::{seealso}

- {ref}`Tutorial_Get_bulkiness` for source references, units and empty results.
- {ref}`user-foundations-support-physchem` for related property tools.
- {func}`molsysmt.physchem.get_sasa` for actual coordinate-based solvent exposure.
:::
